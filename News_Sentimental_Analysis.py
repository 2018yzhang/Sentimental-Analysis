#!/usr/bin/env python
# coding: utf-8

# In[14]:


import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
nltk.downloader.download('vader_lexicon')


# In[15]:


import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# In[16]:


bitpush_news = pd.read_csv("data - news.csv")
bitpush_news.head()


# In[17]:


vader = SentimentIntensityAnalyzer()
content = bitpush_news['Content']
content = str(content).encode('utf-8')
content_scores = bitpush_news['Content'].apply(lambda content:vader.polarity_scores(content)).tolist()
content_scores_df = pd.DataFrame(content_scores)
content_scores_df


# In[18]:


scored_news = bitpush_news.join(content_scores_df, rsuffix='_right')
scored_news


# In[19]:


title = bitpush_news['Title']
title = str(title).encode('utf-8')
title_scores = bitpush_news['Title'].apply(lambda content:vader.polarity_scores(content)).tolist()
title_scores_df = pd.DataFrame(title_scores)
title_scores_df


# In[20]:


scored_news = scored_news.join(title_scores_df, rsuffix='_right')
scored_news


# In[21]:


def get_status(df):
    if df['compound_right'] < 0:
        df["Total Score"] = df["compound"] * 0.15 + df["compound_right"] * 0.85
        return df["Total Score"]
    elif df['compound_right'] > 0:
        df["Total Score"] = df["compound"] * 0.85 + df["compound_right"] * 0.15
        return df["Total Score"]
    else:
        df["Total Score"] = df["compound"] * 0.5 + df["compound_right"] * 0.5
        return df["Total Score"]

scored_news["Total Score"] = scored_news.apply(get_status, axis = 1)


# In[22]:


scored_news


# In[23]:


scored_news.to_csv("news_analysis.csv",index=False)


# In[ ]:




