import streamlit as st
import data_store as ds


df_customers=ds.df_customers.copy()
df_orders=ds.df_orders.copy()
df_products=ds.df_products.copy()

col1, col2, = st.columns([1,2])

with col1:
    st.image("./public/olist2.png",width=100)

with col2:
    st.title('Dashboard Analítico - Olist')
    st.write("Análisis exploratorio de datos de ventas, clientes, pedidos y productos.")

st.header("Indicadores Principales")
col1, col2= st.columns(2)
col3, col4= st.columns(2)
col1.metric("Total Clientes", df_customers["customer_unique_id"].nunique(), border=True)
col2.metric("Total Pedidos", len(df_orders),border=True)
col3.metric("Total Productos", df_products["product_id"].nunique(),border=True)
col4.metric("Categorías de Productos", df_products["product_category_name_pt"].nunique(),border=True)
 