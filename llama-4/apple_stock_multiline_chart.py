"""
Llama-4 sometimes generates fake data even though I said not to.
Even though I the prompt was for the past year, it did only 1 week.
"""
import pandas as pd
import plotly.express as px

# This looks fake.
# data = {
#     'Date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01', '2022-06-01', '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01', '2022-11-01', '2022-12-01'],
#     'Open': [100, 120, 110, 130, 140, 150, 160, 170, 180, 190, 200, 210],
#     'High': [110, 130, 120, 140, 150, 160, 170, 180, 190, 200, 210, 220],
#     'Low': [90, 110, 100, 120, 130, 140, 150, 160, 170, 180, 190, 200],
#     'Close': [105, 125, 115, 135, 145, 155, 165, 175, 185, 195, 205, 215]
# }

# This one looks ok.
data = {
    'Date': ['2023-09-16', '2023-09-17', '2023-09-18', '2023-09-19', '2023-09-20', 
             '2023-09-21', '2023-09-22', '2023-09-23', '2023-09-24', '2023-09-25'],
    'Open': [182.94, 183.35, 182.81, 183.45, 183.88, 
             183.29, 182.95, 183.11, 183.58, 183.92],
    'High': [184.38, 184.59, 184.09, 184.59, 184.95, 
             184.39, 184.09, 184.25, 184.69, 185.03],
    'Low': [182.35, 182.69, 182.35, 182.95, 183.39, 
            182.85, 182.59, 182.69, 183.09, 183.45],
    'Close': [183.88, 184.25, 183.92, 184.38, 184.69, 
              184.09, 183.81, 183.95, 184.45, 184.88]
}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Plotting all the lines (Open, High, Low, Close)
fig = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title='Apple Stock Price (2023-09-16 to 2023-09-25)')

fig.update_layout(xaxis_title='Date', yaxis_title='Stock Price (USD)')
fig.show()
