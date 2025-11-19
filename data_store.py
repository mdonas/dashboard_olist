import matplotlib.pyplot as plt
import pandas as pd

df_customers=pd.read_csv('./csv/customer.csv')
df_customers_unique=pd.read_csv('./csv/customerUnique.csv')
df_merge_late_total=pd.read_csv('./csv/df_merge_late_total.csv',parse_dates=['days_diference_mean'])
df_mean_score=pd.read_csv('./csv/df_mean_score.csv')
df_number_review_state=pd.read_csv('./csv/df_number_review_state.csv')





df_city_state_group = df_customers_unique.groupby(['customer_city','customer_state'], as_index=False).customer_unique_id.count().sort_values('customer_unique_id', ascending=False).reset_index(drop=True)
df_city_state_group= df_city_state_group.rename(columns={'customer_unique_id':'customer_number'})

df_state_group = df_customers_unique.groupby(['customer_state']).customer_unique_id.count().sort_values(ascending=False).reset_index()
df_uniques_states = df_customers.groupby('customer_state').count().sort_values('customer_id', ascending=False).head(19).reset_index()['customer_state']

cmap = plt.cm.tab20
state_to_color = {state: cmap(i / len(df_uniques_states)) for i, state in enumerate(df_uniques_states)}
state_to_color["Otros"] = plt.cm.tab20(19)

