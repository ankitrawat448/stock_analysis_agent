import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from phi.agent.agent import Agent
from phi.model.groq import Groq
from phi.tools.googlesearch import GoogleSearch
from phi.tools.yfinance import YFinanceTools

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

COMMON_STOCKS = {
    'NVIDIA': 'NVDA', 'APPLE': 'AAPL', 'GOOGLE': 'GOOGL', 'MICROSOFT': 'MSFT',
    'TESLA': 'TSLA', 'AMAZON': 'AMZN', 'META': 'META', 'NETFLIX': 'NFLX',
    'TCS': 'TCS.NS', 'RELIANCE': 'RELIANCE.NS', 'INFOSYS': 'INFY.NS',
    'WIPRO': 'WIPRO.NS', 'HDFC': 'HDFCBANK.NS', 'TATAMOTORS': 'TATAMOTORS.NS',
    'ICICIBANK': 'ICICIBANK.NS', 'SBIN': 'SBIN.NS'
}

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.markdown("""<style>
.stApp { max-width: 1400px; margin: 0 auto; }
.card {
    background: linear-gradient(135deg, #f6f8fa 0%, #ffffff 100%);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border: 1px solid #e1e4e8;
}
.metric-value { font-size: 24px; font-weight: bold; color: #0366d6; }
.metric-label { font-size: 14px; color: #586069; text-transform: uppercase; }
.chart-container {
    background: white;
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid #e1e4e8;
}
</style>""", unsafe_allow_html=True)

def initialize_agents():
    if not st.session_state.get("agents_initialized", False):
        try:
            st.session_state.web_agent = Agent(
                name="Web Agent",
                role="Search the web for recent company news",
                model=Groq(api_key=GROQ_API_KEY, model="llama3-70b-8192"),
                tools=[GoogleSearch(fixed_max_results=5)]
            )
            st.session_state.finance_agent = Agent(
                name="Finance Agent",
                role="Fetch financial insights",
                model=Groq(api_key=GROQ_API_KEY, model="llama3-70b-8192"),
                tools=[YFinanceTools()]
            )
            st.session_state.agents_initialized = True
        except Exception as e:
            st.error(f"Agent Initialization Error: {e}")

@st.cache_data
def get_stock_data(symbol, period):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period=period)
        return info, hist
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None, None

def create_price_chart(hist_data, symbol):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist_data.index,
        open=hist_data['Open'], high=hist_data['High'],
        low=hist_data['Low'], close=hist_data['Close'],
        name='OHLC'
    ))
    fig.update_layout(
        title=f'{symbol} Price Chart',
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        height=500
    )
    return fig

def display_metrics(info):
    def fmt(val, currency=False):
        if val is None:
            return "N/A"
        if currency:
            return f"${val:,.2f}"
        if isinstance(val, (int, float)):
            if abs(val) > 1e9:
                return f"{val/1e9:.2f} B"
            elif abs(val) > 1e6:
                return f"{val/1e6:.2f} M"
            return f"{val:.2f}"
        return val

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='card'><div class='metric-value'>{fmt(info.get('currentPrice'), currency=True)}</div><div class='metric-label'>Current Price</div></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><div class='metric-value'>{fmt(info.get('marketCap'))}</div><div class='metric-label'>Market Cap</div></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><div class='metric-value'>{fmt(info.get('beta'))}</div><div class='metric-label'>Beta</div></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    col4.markdown(f"<div class='card'><div class='metric-value'>{fmt(info.get('forwardPE'))}</div><div class='metric-label'>Forward P/E</div></div>", unsafe_allow_html=True)
    col5.markdown(f"<div class='card'><div class='metric-value'>{fmt(info.get('trailingEps'))}</div><div class='metric-label'>EPS</div></div>", unsafe_allow_html=True)
    col6.markdown(f"<div class='card'><div class='metric-value'>{str(info.get('recommendationKey')).replace('_', ' ').title()}</div><div class='metric-label'>Recommendation</div></div>", unsafe_allow_html=True)

def main():
    st.title("📊 Stock Dashboard")

    col1, col2 = st.columns([2, 1])
    with col1:
        stock_choice = st.selectbox("Select Company", options=list(COMMON_STOCKS.keys()) + ["Other"])
    with col2:
        time_period = st.selectbox("Select Time Period", options=["1mo", "3mo", "6mo", "1y", "2y"], index=3)

    stock_input = ""
    if stock_choice == "Other":
        stock_input = st.text_input("Enter Stock Symbol (e.g., NVDA, TSLA)")
    else:
        stock_input = COMMON_STOCKS.get(stock_choice)

    if st.button("Analyze"):
        if not stock_input:
            st.error("Please enter a valid stock symbol.")
            return

        initialize_agents()

        with st.spinner("Fetching data..."):
            info, hist = get_stock_data(stock_input, time_period)

            if info and hist is not None and not hist.empty:
                tabs = st.tabs(["📈 Chart", "📄 Company Overview"])

                with tabs[0]:
                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    st.plotly_chart(create_price_chart(hist, stock_input), use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with tabs[1]:
                    display_metrics(info)

    if 'longBusinessSummary' in info:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Company Overview")
        st.write(info['longBusinessSummary'])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### AI Summary")
    try:
        summary = st.session_state.web_agent.run(
            f"Summarize the latest relevant company news about {stock_input} from the last 7 days."
        )
        st.write(summary)
    except Exception as e:
        st.error(f"Agent summary error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### AI Summary")
    try:
        summary = st.session_state.web_agent.run(
            f"Summarize the latest relevant company news about {stock_input} from the last 7 days."
        )
        st.write(summary)
    except Exception as e:
        st.error(f"Agent summary error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("No historical data found for this symbol.")
if __name__ == "__main__":
    import os
    os.environ['STREAMLIT_SERVER_RUN_ON_SAVE'] = 'true'
    main()
