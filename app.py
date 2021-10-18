import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import math

st.set_page_config(layout="wide")

@st.cache
def load_data():
    path = "https://raw.githubusercontent.com/ZhouyaoXie/stock-price-visualization/main/all_stocks_5yr.csv"
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df[['Name', 'date', 'close','volume']]

data_load_state = st.markdown('*Loading data...*')
df = load_data(path)
data_load_state.markdown('*Loading graphics...*')

st.markdown("This interactive web app explores stock prices of S&P 500 companies from 2013-02-08 to 2018-02-07.\n \
The line plot on the left panel displays the stock price against time; the heatmap on the right panel shows \
the correlation structure of stock prices.\n The dataset comes from the [S&P 500 stock data](https://www.kaggle.com/camnugent/sandp500)\
 dataset on Kaggle and is compiled by Cam Nugent.")
st.markdown("#### Questions \n Some of the questions you could explore with this interactive visualization include:\n\
- Time series analysis: How does the stock price of a company change over time?\n \
- Comparative analysis: How do the stock prices of different companies compare?\n \
- Correlation analysis: How are the stock prices of a group of companies correlated with each other?")
st.markdown("#### Instructions \n The following input fields are provided on the sidebar:\n  \
- Select any number of S&P 500 companies using their ticker symbols from the drop down list.\n \
- Select a start date and end date. The range should be within 2013-02-08 and 2018-02-07.\n \
- Extra explore options:\n\
    - `Show max variance company`: Show the stock with the largest variance over the specified time period.\n \
    - `Show min variance company`: Show the stock with the smallest variance.\n\
    - `Show fastest growth company`: Show the company with the highest growth rate (growth rate calculated as (price at end date - price at start date) / price at start date) over the specified time period.\n \
    - `Show slowest growth company`: Show the company with the slowest growth rate.\n\n\
Start by selecting a few companies to explore from the sidebar!")

col1, col2 = st.columns(2)

st.sidebar.markdown("**About**")
st.sidebar.markdown("Author: Zhouyao Xie")
st.sidebar.markdown("Github: ZhouyaoXie")
st.sidebar.markdown("CMU 05839 interactive Data Science")
st.sidebar.markdown("Instructor: John Stamper")
st.sidebar.markdown("**Input Fields**")
# select companies
select = st.sidebar.multiselect('Select companies to display:', df.Name.unique())
default_stock_lst = ['AAPL', 'MSFT', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'NVDA', 'BRK.B', 'JPM']
stock_lst = select if select else default_stock_lst
# select start date
start_date = st.sidebar.date_input("Start date:", datetime.date(2013,2,8), 
                        min_value = datetime.date(2013,2,8), 
                        max_value = datetime.date(2018,2,7))
# select end date
end_date = st.sidebar.date_input("End date:", datetime.date(2018,2,7), 
                        min_value = start_date + datetime.timedelta(1), 
                        max_value = datetime.date(2018,2,7))
# select explore options
st.sidebar.markdown('Explore:')
max_variance = st.sidebar.checkbox('Show max variance company')
min_variance = st.sidebar.checkbox('Show min variance company')
fastest_growth = st.sidebar.checkbox('Show fastest growth company')
slowest_growth = st.sidebar.checkbox('Show slowest growth company')

# prepare input dataframe
df_display = df.loc[(df['date'] >= start_date) & (df['date'] <= end_date)]
if not max_variance and not min_variance and not fastest_growth and not slowest_growth:
    df_display = df_display.loc[df_display['Name'].isin(stock_lst)]
    wide_df = pd.pivot_table(df_display, columns = 'Name', values = 'close', index = 'date')
else:
    wide_df = pd.pivot_table(df_display, columns = 'Name', values = 'close', index = 'date')
    change_column_names = {}
    if max_variance:
        max_variance_company = wide_df.var(axis = 0).argmax()
        max_variance_company = wide_df.columns[max_variance_company]
        change_column_names[max_variance_company] = max_variance_company + ' (Max Var)'
        if max_variance_company not in stock_lst:
            stock_lst.append(max_variance_company)
    if min_variance:
        min_variance_company = wide_df.var(axis = 0).argmin()
        min_variance_company = wide_df.columns[min_variance_company]
        change_column_names[min_variance_company] = min_variance_company + ' (Min Var)'
        if min_variance_company not in stock_lst:
            stock_lst.append(min_variance_company)
    if fastest_growth:
        fastest_growth_company = ((wide_df.iloc[-1] - wide_df.iloc[0]) / wide_df.iloc[0]).argmax()
        fastest_growth_company = wide_df.columns[fastest_growth_company]
        change_column_names[fastest_growth_company] = fastest_growth_company + ' (Fastest Growth)'
        if fastest_growth_company not in stock_lst:
            stock_lst.append(fastest_growth_company)
    if slowest_growth:
        slowest_growth_company = ((wide_df.iloc[-1] / wide_df.iloc[0]) / wide_df.iloc[0]).argmin()
        slowest_growth_company = wide_df.columns[slowest_growth_company]
        change_column_names[slowest_growth_company] = slowest_growth_company + ' (Slowest Growth)'
        if slowest_growth_company not in stock_lst:
            stock_lst.append(slowest_growth_company)
    df_display = df_display.loc[df_display['Name'].isin(stock_lst)]
    for k, v in change_column_names.items():
        df_display.Name = df_display.Name.str.replace(k, v)
    wide_df = wide_df[stock_lst]
    wide_df.rename(columns = change_column_names, inplace = True)

# creating line plot
fig1 = plt.figure()
sns.set_style('darkgrid')
plot_ = sns.lineplot(data = df_display, x = 'date', y = 'close', hue = 'Name')
plt.xlim(start_date - datetime.timedelta(1), end_date + datetime.timedelta(1))
tick_number = len(plt.xticks()[0])
tick_loc_multiple = tick_number // 20 + 1
plt.legend(fontsize = 'x-small')
plt.xticks(ticks = [plt.xticks()[0][i] for i in range(tick_number) if i % tick_loc_multiple == 0])
plt.xticks(rotation=30, fontsize = 'x-small')
plt.yticks(fontsize = 'x-small')

# creating corr plot
fig2 = plt.figure()
sns.heatmap(wide_df.corr())
plt.xticks(fontsize = 'x-small')
plt.yticks(fontsize = 'x-small')

data_load_state.title('Stock Price of S&P500 Companies')

col1.subheader('Stock Price Changes of Selected Companies ')
col1.pyplot(fig1)
col2.subheader('Correlation Between Stock Prices')
col2.pyplot(fig2)

@st.cache
def convert_df(df):
    return df.to_csv()

with st.expander("Click here to view and download the selected data:"):
    col3, col4 = st.columns(2)
    col3.download_button('Download wide format data', convert_df(wide_df), file_name = 'stock_price_wide.csv')
    col4.download_button('Download long format data', convert_df(df_display), file_name = 'stock_price_long.csv')
    st.dataframe(wide_df)
