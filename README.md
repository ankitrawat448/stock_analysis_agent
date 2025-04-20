
# 📊 Stock Analysis Dashboard (AI-Powered)

This Streamlit app lets you analyze company stock data using interactive charts and financial insights. It includes a clean interface with two powerful AI agents to expand in the future.

---

## 🚀 Features

- 📈 **Candlestick Chart**  
  View the stock's price action over multiple timeframes (`1mo`, `3mo`, `6mo`, `1y`, `2y`).

- 📄 **Company Overview**  
  Get key financial metrics like Market Cap, Beta, EPS, Forward P/E, and a business summary.

- 🤖 **AI Agent Architecture**  
  - `web_agent`: Prepared for web search/news summarization  
  - `finance_agent`: Designed for financial insight & stock explanation tasks

- 🔁 **Auto Reload on Save**  
  Built-in dev experience enhancement with hot-reload on code changes.

---

## 🧠 Built With

- [Streamlit](https://streamlit.io) – Interactive web UI
- [yfinance](https://pypi.org/project/yfinance/) – Stock data retrieval
- [plotly](https://plotly.com/python/) – Dynamic financial charting
- [Phi](https://github.com/phi-tools/phi) – AI agents and tools framework
- [Groq](https://console.groq.com) – High-speed model inference (LLaMA 3 support)

---

## 🔧 Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/stock-dashboard-ai.git
cd stock-dashboard-ai
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure secrets**

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

4. **Run the app**

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
app.py                  # Main Streamlit app
README.md               # Project documentation
requirements.txt        # Python dependencies
.streamlit/
└── secrets.toml        # API keys (Groq, etc.)
```

---

## 📌 Future Enhancements

- News summarization from web or NewsAPI
- AI-generated stock outlook and analysis
- Export charts as PDF/CSV
- Sentiment classification for recent news
- Add user authentication for tracking portfolios

---



