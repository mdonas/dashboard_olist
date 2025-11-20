import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import data_store as ds
import numpy as np

df_metric_products=ds.df_metric_products.copy()
df_sorted = df_metric_products.groupby(['product_category_name_en'])['sell_percentage_%'].sum().reset_index().sort_values('sell_percentage_%', ascending=False).head(10)
df_uniques_categories=df_sorted.drop_duplicates(subset='product_category_name_en')['product_category_name_en'].head(10)

paleta=ds.cmap_10.copy()
category_to_color = {state: paleta(i / len(df_uniques_categories)) for i, state in enumerate(df_uniques_categories)}
category_to_color["Otros"] = paleta(9)
st.markdown("<h1 style='text-align: center;'>Analisis de Ventas</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------------------------
st.subheader("Porcentaje de ventas por categoría",anchor=False,divider=True)
x=df_sorted['product_category_name_en'].str.capitalize()
y=df_sorted['sell_percentage_%']
c=df_sorted['product_category_name_en'].apply(lambda x: category_to_color[x])

fig, ax=plt.subplots(figsize=(12,6))
plt.bar(x, y,color=c)
plt.xticks(rotation=45,ha='right')
plt.ylabel("% Ventas",fontsize=15,fontweight='bold')
ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter())
plt.xlabel("Categoría",fontsize=15,fontweight='bold')
plt.tight_layout()
st.pyplot(fig)

# -------------------------------------------------------------------------------
df_final_metrics=ds.df_final_metrics.copy()
state_to_color=ds.state_to_color.copy()
st.subheader("Porcentaje de ventas por estado",anchor=False,divider=True)
#% total de ventas por estado
df_sorted = df_final_metrics.sort_values('total_sell_percentage', ascending=False).head(10)

x=df_sorted['customer_state']
y= df_sorted['total_sell_percentage']
c=df_sorted['customer_state'].apply(lambda x: state_to_color[x])

fig,ax=plt.subplots(figsize=(12,6))
plt.bar(x,y,color=c)
plt.title("Porcentaje del total de ventas por estado")
ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter())

plt.ylabel("% del total de ventas")
plt.xlabel("Estado")
plt.tight_layout()
st.pyplot(fig)