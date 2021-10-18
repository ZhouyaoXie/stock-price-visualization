# stock-price-visualization


[This interactive web app](https://share.streamlit.io/zhouyaoxie/stock-price-visualization/main/app.py) explores stock prices of S&P 500 companies from 2013-02-08 to 2018-02-07. The line plot on the left panel displays the stock price over time; the heatmap on the right panel shows the correlation structure of stock prices. The dataset comes from the [S&P 500 stock data](https://www.kaggle.com/camnugent/sandp500) dataset on Kaggle and is compiled by Cam Nugent.


## Questions

The goal of this visualization is to help users answer the following fundamental questions about stock prices:

- Time series analysis: How does the stock price of a company change over time?
- Comparative analysis: How do the stock prices of different companies compare?
- Correlation analysis: How are the stock prices of a group of companies correlated with each other?

## Design decisions

While designing this data visualization application, my goal is to make it as straightforward, intuitive, and easy-to-use as possible. I chose to use a line plot to display the stock price data over time because line plots are great for showcasing time series data. I used color encodings to differentiate the companies, because color is one of the most straightforward visual cues for human beings. For the correlation analysis, I chose to use a heatmap to represent the correlation between stocks because a heatmap is the most natural way to represent a data matrix. Again, color is used to encode the strength and direction of the correlation, which allows users to notice interesting correlation patterns by just taking a very quick glance of the heatmap.

One design question that I spent some time thinking about is which value to use for the y-axis of the line plot. Currently, the plot shows the stock price, but one alternative way of representing stock price changes is to show the percent change in stock price. In other words, all stocks would start at the same initial value (%change = 0) at the leftmost point, and their percent increase or decrease will be computed. While this approach has the obvious advantage of making it easier to compare the growth trend of different stocks, I eventually decided to go with just showing the stock price because 1) the idea of "stock price" is easier to understand than the idea of "percent change in stock price comparing with the stock price in the start date", and 2) some of the questions that users might ask can only be answered if we know the true price of the stock, so computing the percent change makes us lose some important information.

## Development process

I spent 5 hours developing this application:

- I spent 1 hour researching different visualization ideas, browsing Kaggle datasets and Streamlit applications.
- I spent 0.5 hour learning Streamlit through its documentation.
- I spent 1.5 hour building the foundation of the visualization- the line plot and the heatmap, the select box for companies, and the select box for start and end dates.
- I spent 1.5 hours adding extra functionalities:
  - Four "explore" checkboxes that show max/min variance stocks and fastest/slowest growth stocks.
  - An expandable box that shows the full dataframe and allows users to download the data in two formats (wide and long).
- I spent 0.5 hours writing introduction and documentation.
