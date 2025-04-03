# AIChartBuilder
AI-powered chart building

---

**AI Chart Builder** lets you type in a natural language prompt like *"Show a line chart of average patient heart rate over the past 7 days"* and then uses GPT-4 to generate the actual Python code to make that chart. The app runs the code and displays the chart right on the page using Plotly. It's built with Dash and handles errors gracefully, so if something goes wrong, it won't crash — it just tells you what happened.

No more manually scripting visualizations. Just say what you want, and it builds it.

---

## Example Prompts

Here are some example prompts you can use with the Plotly AI/Dash app ([chart_app.py](chart_app.py)) to generate charts:

**Simple Charts**

1. Plot a line chart of the stock prices of Apple over the past year.
2. Create a bar chart of the top 5 countries by GDP.
3. Show a pie chart of the distribution of ages in a population.

**Time Series Charts**

1. Plot the daily closing prices of the S&P 500 index for the past 5 years.
2. Create a chart of the average temperature in New York City over the past 10 years.
3. Show a chart of the number of COVID-19 cases in the United States over the past 6 months.

**Geographic Charts**

1. Plot a map of the world showing the population density of each country.
2. Create a chart of the top 10 cities by population density in the United States.
3. Show a chart of the average temperature in different regions of the world.

**Custom Charts**

1. Plot a scatter plot of the relationship between GDP and population for different countries.
2. Create a chart of the top 5 most popular books on Amazon over the past month.
3. Show a chart of the average commute time in different cities in the United States.

**Fun Charts**

1. Plot a chart of the most popular memes on the internet over the past year.
2. Create a chart of the top 10 most expensive cars in the world.
3. Show a chart of the average height of NBA players over the past 20 years.
