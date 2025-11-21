import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib as mpl
from streamlit_folium import st_folium
import pandas as pd
import data_store as ds

df_late_state=ds.df_late_state.copy()
gdf=ds.gdf.copy()

st.markdown("<h1 style='text-align: center;'>Analisis de Pedidos</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------------------------
st.subheader("Porcentaje de pedidos retrasados por estado",anchor=False,divider=True)
#renombrar columnas para merge
df_late_state = df_late_state.rename(columns={'customer_state':'id','late_orders_respect_total_%':'orders_late_percent'})

gdf_late = pd.merge(
    gdf,
    df_late_state,
    on='id',
    how='inner'
)

gdf_late.rename(columns={'id':'Estado','name':'Ciudad','orders_late':'Numero pedidos retrasados',
                     'orders_late_percent':'Porcentaje de pedidos retrasado','delay_days':'Dias de retraso promedio '},inplace=True)
m = gdf_late.explore(
    "Porcentaje de pedidos retrasado",
    legend=False
)

st_folium(m, width=700, height=500)