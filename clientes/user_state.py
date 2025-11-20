import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import data_store as ds

df_customers_unique=ds.df_customers_unique.copy()
state_to_color=ds.state_to_color.copy()
st.markdown("<h1 style='text-align: center;'>Analisis de Clientes</h1>", unsafe_allow_html=True)
st.subheader('Distribución de clientes por estado',anchor=False,divider=True)

df_state_group = ds.df_state_group.head(10).copy()

top5 = df_state_group.head(5)
df_state_group_top5 = df_state_group.head(5)
others = df_state_group.iloc[5:].sum()
row_others = pd.DataFrame({
    'customer_state': ['Otros'],
    'customer_unique_id': [others['customer_unique_id']]
})
df_state_group_top5 = pd.concat([top5, row_others], ignore_index=True)

fig, ax = plt.subplots(figsize=(6,7))

x = df_state_group_top5['customer_state'].values
y = df_state_group_top5['customer_unique_id'].values
c = df_state_group_top5['customer_state'].apply(lambda x: state_to_color[x])
c[1]='tomato'
c[3]='gold'
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}%\n({v:d})'.format(pct, v=val)
    return my_format

wedges,texts,autotexts=ax.pie(y, labels=x, colors=c,autopct=autopct_format(y),textprops={'fontsize': 8,'color':'white'})
# ---> Estilo etiquetas exteriores (nombres)
for t in texts:
    t.set_color("black")


st.pyplot(fig,use_container_width=True)