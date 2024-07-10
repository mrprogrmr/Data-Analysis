#!/usr/bin/env python
# coding: utf-8

# In[20]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install requests')
# !mamba install bs4
# !mamba install html5lib
get_ipython().system('pip install lxml')
get_ipython().system('pip install plotly')
get_ipython().system('pip install yfinance')
get_ipython().system('pip install nbformat')


# In[21]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[22]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# # Question 1: Use yfinance to Extract Stock Data

# In[23]:


tesla = yf.Ticker("TSLA")


# In[24]:


tesla_share_price = tesla.history(period='max')


# In[25]:


tesla_share_price.reset_index(inplace=True)


# # Question 2: Use Webscraping to Extract Tesla Revenue Data

# In[44]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text
print(html_data)


# In[45]:


soup = BeautifulSoup(html_data, 'html5lib')


# In[46]:


all_tables = soup.find_all('table')


# In[47]:


read_html_pd = pd.read_html(url)
tesla_revenue = read_html_pd[1]
tesla_revenue.head()


# In[49]:


tesla_revenue.rename(columns={"Tesla Quarterly Revenue (Millions of US $)":"Date", "Tesla Quarterly Revenue (Millions of US $).1":"Revenue"}, inplace=True)
tesla_revenue.head()


# In[61]:


tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace('$', "")
tesla_revenue.tail(5)


# In[52]:


tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',', "")
tesla_revenue.head()


# In[54]:


tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue


# In[55]:


tesla_revenue.tail(5)


# # GME

# In[56]:


gme = yf.Ticker('GME')
gme_share_price = gme.history(period='max')
gme_share_price.reset_index(inplace=True)


# In[58]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text


# In[59]:


soup = BeautifulSoup(html_data, 'html5lib')


# In[60]:


read_html_pd = pd.read_html(url)
gme_revenue = read_html_pd[1]
gme_revenue.head()


# In[62]:


gme_revenue.rename(columns={"GameStop Quarterly Revenue (Millions of US $)":"Date", "GameStop Quarterly Revenue (Millions of US $).1":"Revenue"}, inplace=True)
gme_revenue.head()


# In[63]:


gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace('$', "")
gme_revenue.tail(5)


# In[64]:


gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue


# In[65]:


gme_revenue.tail(5)


# In[66]:


gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(',', "")


# In[67]:


gme_revenue.tail()


# In[70]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[74]:


make_graph(tesla_share_price, tesla_revenue, 'tesla')


# In[75]:


make_graph(gme_share_price, gme_revenue, 'gme')


# In[ ]:




