"""
Uses yfinance to get the Apple stock price over the past year. But...
It generated a standalone Python script with a main() function and fig.show(), which is incompatible with the Dash app.
The app expects the code to directly produce a Plotly figure object (fig) that can be returned and rendered in the UI, not displayed immediately.
"""
import plotly.express as px
import yfinance as yf


def main():
    try:
        apple_stock = yf.Ticker("AAPL")
        hist = apple_stock.history(period="1y")
        fig = px.line(hist, x=hist.index, y='Close', title='Apple Stock Price Over the Past Year')
        fig.show()
    except Exception as e:
        fig = px.bar(x=["No data found"], y=[0], title='No data found')
        fig.update_layout(title_text="No data found", title_x=0.5)
        fig.show()


if __name__ == "__main__":
    main()
