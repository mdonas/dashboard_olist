import streamlit as st
import matplotlib.pyplot as plt
import data_store as ds

st.markdown("<h1 style='text-align: center;'>Analisis de Ventas</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------------------------
st.subheader("Frecuencia de categorías dominantes",anchor=False,divider=True)

df_final_metrics=ds.df_final_metrics.copy()
#frecuencia categorias dominantes
counts = df_final_metrics['product_category_name_en'].value_counts()
l=counts.index.str.capitalize()
fig=plt.figure(figsize=(6,6))
plt.pie(counts, labels=l, autopct='%1.1f%%')
plt.tight_layout()
st.pyplot(fig)