import pandas as pd
import os, math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

working_dir = os.getcwd()+'/'
files = pd.Series(os.listdir(working_dir))

input_files = files[files.str.contains('.csv')]
input_files = working_dir+input_files

dataframes = input_files.apply(pd.read_csv).tolist()

join_index = 1
final_dataframe = dataframes[0]

while join_index < len(dataframes):
    final_dataframe = final_dataframe.merge(right=dataframes[join_index],how='outer',on='Date',suffixes=("",'.'+str(join_index)))

    join_index += 1

#ad revenue to viewer count
final_dataframe['Ad plus turbo'] = final_dataframe['Ad Revenue']+final_dataframe['Turbo Revenue']
final_dataframe['Date'] = pd.to_datetime(final_dataframe['Date'])

sns.set(font_scale=1)

final_dataframe_v1 = final_dataframe.drop(
    labels=final_dataframe.columns[(final_dataframe==0).all()],
    axis=1
)
not_columns = final_dataframe_v1.filter(like='.')+final_dataframe_v1[['Ad Revenue','Turbo Revenue']]
final_dataframe_v2 = final_dataframe_v1.drop(
    labels=not_columns,
    axis=1
)

print(final_dataframe_v2.columns)

final_dataframe_v2.to_csv('Twitch_Analytics_cleaned_up.csv',index=False)

figsize = [final_dataframe_v2.shape[1]]*2

plt.figure(figsize=figsize)
plt.title(label="Statistic Correlation on Twitch 2023")
sns.heatmap(
    final_dataframe_v2.corr().round(decimals=2),
    annot = True
).get_figure().savefig('twitch_corr_2023.png',bbox_inches='tight')

#next we sort, and find the values with actual correlations
#real question: what correlates best with ad revenue?

plt.clf()

ads = final_dataframe_v2.corr()
ads['Ad plus turbo'].plot(kind='bar').get_figure().savefig('ad_corr_2023.png')

what_affects_ads_revenue = pd.DataFrame({
    'Positive':ads['Ad plus turbo'].sort_values(ascending=False).head(11).index[1:11],
    'Negative':ads['Ad plus turbo'].sort_values(ascending=True).head(10).index
})
what_affects_ads_revenue.to_csv('what_affects_revenue.csv',index=False)
print(what_affects_ads_revenue)