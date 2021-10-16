import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import datetime
import math

st.set_page_config(layout="wide")


path = "X:/Master/2021Fall/05839/assignment-2-ZhouyaoXie/sp_stock_data/all_stocks_5yr.csv"

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df[['Name', 'date', 'close']]

data_load_state = st.markdown('*Loading data...*')
df = load_data(path)
data_load_state.markdown('*Loading graphics...*')

"This interactive web app explores stock price changes of S&P 500 companies from 2013-02-08 to 2018-02-07. \
The line plot on the left panel displays time series data, while the heatmap on the right panel shows \
the correlation structure of stock prices. Start by selecting a few companies to explore  \
from the sidebar!"

col1, col2 = st.columns(2)

# select companies
select = st.sidebar.multiselect('Select companies to display:', df.Name.unique())
default_stock_lst = ['AAPL', 'MSFT', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA', 'NVDA', 'BRK.B', 'JPM']
stock_lst = select if select else default_stock_lst
# select start date
start_date = st.sidebar.date_input("Start date:", datetime.date(2013,2,8), 
                        min_value = datetime.date(2013,2,8), 
                        max_value = datetime.date(2018,2,7))
# select end date
end_date = st.sidebar.date_input("Start date:", datetime.date(2018,2,7), 
                        min_value = start_date + datetime.timedelta(1), 
                        max_value = datetime.date(2018,2,7))

# prepare input dataframe
df_display = df.loc[df['Name'].isin(stock_lst)]
df_display = df_display.loc[(df_display['date'] >= start_date) & (df_display['date'] <= end_date)]
wide_df = pd.pivot_table(df_display, columns = 'Name', values = 'close', index = 'date')

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

