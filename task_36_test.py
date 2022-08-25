# 36

import requests
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

response = requests.get(
    'http://127.0.0.1:5000/shops')

shops_df = pd.read_json(BytesIO(response.content))

response = requests.get(
    'http://127.0.0.1:5000/shop_stats')

shop_stats_df = pd.read_json(BytesIO(response.content))

res_df = shop_stats_df.merge(shops_df, on='shop_code', copy=True)
res_df['p_year'] = res_df['period'] // 100
res_df['p_month'] = res_df['period'] % 100

# оборот
df_17s = res_df.loc[res_df['p_year'] == 2017, ['shop_name', 'sales']] \
    .groupby('shop_name').sum().rename(columns={'sales': 'sales_17'})

df_18s = res_df.loc[res_df['p_year'] == 2018, ['shop_name', 'sales']] \
    .groupby('shop_name').sum().rename(columns={'sales': 'sales_18'})

df_19s = res_df.loc[res_df['p_year'] == 2019, ['shop_name', 'sales']] \
    .groupby('shop_name').sum().rename(columns={'sales': 'sales_19'})

df_fin_s = pd.concat([df_17s, df_18s, df_19s], axis=1).fillna(0)

# наценка
df_17m = res_df.loc[res_df['p_year'] == 2017, ['shop_name', 'markup']] \
    .groupby('shop_name').sum().rename(columns={'sales': 'markup_17'})

df_18m = res_df.loc[res_df['p_year'] == 2018, ['shop_name', 'markup']] \
    .groupby('shop_name').sum().rename(columns={'sales': 'sales_18'})

df_19m = res_df.loc[res_df['p_year'] == 2019, ['shop_name', 'markup']] \
    .groupby('shop_name').sum().rename(columns={'sales': 'markup_19'})

df_fin_m = pd.concat([df_17m, df_18m, df_19m], axis=1).fillna(0)

fig, axes = plt.subplots(figsize=(10, 7), nrows=2, ncols=1)

df_fin_s.plot(ax=axes[0], kind='bar', ylabel='Оборот', sharex=True)
df_fin_m.plot(ax=axes[1], kind='bar', xlabel='', ylabel='Наценка', sharex=True)

axes[0].ticklabel_format(style='plain', axis='y', useLocale=True)
axes[1].ticklabel_format(style='plain', axis='y', useLocale=True)

axes[0].legend(['2017', '2018', '2019'])
axes[1].legend(['2017', '2018', '2019'])

axes[0].yaxis.set_major_formatter(tkr.StrMethodFormatter('{x:,.0f}'))
axes[1].yaxis.set_major_formatter(tkr.StrMethodFormatter('{x:,.0f}'))

fig.suptitle('Статистика по магазинам')
fig.supxlabel('Магазин')

plt.xticks(rotation=30)

plt.show()
