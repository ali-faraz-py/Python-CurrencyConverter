# 💱 Professional Currency Converter

A modern, desktop-based Currency Converter built with **Python**, **PyQt5**, and **Matplotlib**. This app provides real-time exchange rates via the ExchangeRate-API and visualizes currency trends with dynamic charts.



## ✨ Features
* **Real-Time Data:** Fetches the latest exchange rates for over 160+ currencies using REST API.
* **Interactive Charting:** Displays a 7-day trend line using Matplotlib to visualize currency volatility.
* **Smart History:** Automatically logs your recent conversions for quick reference.
* **Earthy UI Design:** A custom-styled interface using CSS (QSS) for a modern look and feel.
* **Currency Swap:** A one-click button to invert your "From" and "To" selections.

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ali-faraz-py/Python-CurrencyConverter.git](https://github.com/ali-faraz-py/Python-CurrencyConverter.git)
   cd CurrencyConverter


Install dependencies:

```bash
pip install -r requirements.txt
```


## 📂 Project Structure
```text
CurrencyConverter/
├── CurrencyConverter.py     
├── CurrencyConverter.css   
├── requirements.txt      
└── README.md    
```

🛠️ Built With
PyQt5 - For the desktop window and widgets.

Requests - To handle API calls to the exchange rate server.

Matplotlib - To render the 7-day trend graphs.

ExchangeRate-API - The source for real-time global currency data.

🧠 Behind the Logic: The Random Walk
Because historical data often requires a paid API subscription, I implemented a Random Walk Algorithm to simulate market movement:

The Seed: The logic starts with the real-time rate fetched from the API.

The Simulation: It calculates 7 days of data by applying a random variance (up to ±2%) to each previous day's rate.

The Anchor: To ensure accuracy, the final data point is always locked to the actual current rate.

👤 Author
Syed Ali Faraz - https://github.com/ali-faraz-py

If this project helped you understand PyQt5 or Matplotlib, please give it a ⭐!