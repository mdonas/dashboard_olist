import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import geopandas as gpd


df_customers=pd.read_csv('./csv/customer.csv')
df_orders=pd.read_csv('./csv/df_orders.csv')
df_products=pd.read_csv('./csv/df_products.csv')
df_customers_unique=pd.read_csv('./csv/customerUnique.csv')
df_merge_late_total=pd.read_csv('./csv/df_merge_late_total.csv',parse_dates=['days_diference_mean'])
df_mean_score=pd.read_csv('./csv/df_mean_score.csv')
df_number_review_state=pd.read_csv('./csv/df_number_review_state.csv')
df_metric_products=pd.read_csv('./csv/df_metric_products.csv')

# Cargar JSON
gdf = gpd.read_file('./public/brazil_geo.json')
gdf = gdf.sort_values('id').reset_index(drop=True)

# -------------------------------------------------------------------------------

df_city_state_group = df_customers_unique.groupby(['customer_city','customer_state'], as_index=False).customer_unique_id.count().sort_values('customer_unique_id', ascending=False).reset_index(drop=True)
df_city_state_group= df_city_state_group.rename(columns={'customer_unique_id':'customer_number'})

df_state_group = df_customers_unique.groupby(['customer_state']).customer_unique_id.count().sort_values(ascending=False).reset_index()
df_uniques_states = df_customers.groupby('customer_state').count().sort_values('customer_id', ascending=False).reset_index()['customer_state']
df_uniques_categories=df_metric_products.drop_duplicates(subset='product_category_name_en')['product_category_name_en'].head(10)
df_state_sum = (
    df_metric_products.groupby('customer_state')
      .agg(
          total_sells=('number_sells', 'sum'),
          total_customers=('number_customers', 'sum'),
          total_sell_percentage=('sell_percentage_%', 'sum'),
          total_ratio=('ratio_customer_buy', 'sum')
      )
      .reset_index()
)
df_late_state = df_merge_late_total.groupby(['customer_state']).agg({'orders_late':'sum',
                                                                     'late_orders_respect_total_%':'mean',
                                                                     'delay_days':'sum'}).reset_index()

df_top_category_state = (df_metric_products.loc[df_metric_products.groupby('customer_state')['number_sells'].idxmax(),['customer_state', 'product_category_name_en']])
df_final_metrics = df_state_sum.merge(df_top_category_state, on='customer_state')
df_final_metrics['total_ratio'] = (df_final_metrics['total_sells']/df_final_metrics['total_customers']).round(2)

# -------------------------------------------------------------------------------

# COlORS
cmap = mpl.colormaps['tab20'].resampled(28)
state_to_color = {state: cmap(i / len(df_uniques_states)) for i, state in enumerate(df_uniques_states)}
state_to_color["Otros"] = cmap(20)

cmap_10 = mpl.colormaps["tab10"]
category_to_color = {state: cmap_10(i / len(df_uniques_categories)) for i, state in enumerate(df_uniques_categories)}
category_to_color["Otros"] = cmap_10(9)

