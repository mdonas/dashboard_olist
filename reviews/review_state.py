import pandas as pd
import matplotlib.pyplot as plt
import data_store as ds
import streamlit as st

df_number_review_state=ds.df_number_review_state.copy()
df_mean_score=ds.df_mean_score.copy()
st.markdown("<h1 style='text-align: center;'>Analisis de Reseñas</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------------------------

st.header("Top 10 estados con mayor número de reseñas y su puntuación media",anchor=False,divider=True)

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

st.subheader("Distribucion de reseñas por estado",anchor=False,divider=True)

#Nº de reviews por estado
top5 = df_number_review_state.head(5)
df_merge_number_reviews_customers_top5 = df_number_review_state.head(5)
others = df_number_review_state.iloc[5:].sum()

row_others = pd.DataFrame({
    'customer_state': ['Otros'],
    'number_reviews': [others['number_reviews']]
})

df_number_review_state_top_5 = pd.concat([top5, row_others], ignore_index=True)
 
values = df_number_review_state_top_5['number_reviews']
labels = df_number_review_state_top_5['customer_state']
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}%\n({v:d})'.format(pct, v=val)
    return my_format

fig=plt.figure(figsize=(7,7))
plt.pie(
    values,
    labels=labels,
    autopct=autopct_format(values)
)
plt.tight_layout()
st.pyplot(fig)
# -------------------------------------------------------------------------------
