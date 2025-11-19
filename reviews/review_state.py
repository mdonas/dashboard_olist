import pandas as pd
import matplotlib.pyplot as plt
import data_store as ds
import streamlit as st

df_number_review_state=ds.df_number_review_state.copy()
df_mean_score=ds.df_mean_score.copy()

# -------------------------------------------------------------------------------
# st.header("Número de reviews por estado",anchor=False,divider=True)

#Nº de reviews por estado
# df_sorted = df_number_review_state.sort_values('number_reviews', ascending=False).head(10)

# fig=plt.figure(figsize=(10,6))
# plt.bar(df_sorted['customer_state'], df_sorted['number_reviews'])
# plt.ylabel("Número de reviews",fontweight='bold')
# plt.xlabel("Estado",fontweight='bold')
# plt.tight_layout()
# st.pyplot(fig)

# -------------------------------------------------------------------------------
st.header("Top 10 estados con mayor número de reviews y su puntuación media",anchor=False,divider=True)

state_to_color=ds.state_to_color.copy()

df_sorted = df_number_review_state.sort_values('number_reviews', ascending=False).head(10)
df_mean_score=df_mean_score[df_mean_score['customer_state'].isin(df_sorted['customer_state'])]
df_sorted2 = df_mean_score.sort_values('review_score_mean', ascending=False)
fig2, ax1 = plt.subplots(figsize=(10,6))

x = df_sorted['customer_state'].values
y = df_sorted['number_reviews'].values
c = df_sorted['customer_state'].apply(lambda x: state_to_color[x])

# Barras
ax1.bar(x, y,color=c)
ax1.set_xlabel("Estado",fontweight='bold')
ax1.set_ylabel("Número de reviews",fontweight='bold')

# Línea en segundo eje
ax2 = ax1.twinx()
ax2.plot(df_sorted['customer_state'], df_sorted2['review_score_mean'], marker='o',color='m')
ax2.set_ylabel("Puntuación media",fontweight='bold')

plt.tight_layout()
st.pyplot(fig2)

# -------------------------------------------------------------------------------