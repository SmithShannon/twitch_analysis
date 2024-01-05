import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


import numpy as np

file = os.getcwd()+'/Twitch_Analytics_cleaned_up.csv'

df = pd.read_csv(file)

sns.set(font_scale=2)

plt.figure(figsize=(20,20))
plt.title(label="Top Correlations for Ad Revenue")

sns.heatmap(
    df[['Chat Messages',
    'Live Views',
    'Chatters',
    'Unique Viewers',
    'Minutes Watched',
    'Engaged Viewers',
    'Returning Engaged Viewers',
    'Average Viewers',
    'Minutes Streamed',
    'Ad Breaks (Minutes)']].corr().round(decimals=3),
    annot=True
).get_figure().savefig('positive_heatmap.png',bbox_inches='tight')
