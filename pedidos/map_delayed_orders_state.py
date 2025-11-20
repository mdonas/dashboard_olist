import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
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

gdf_late['centroid'] = gdf_late.centroid
fig,ax = plt.subplots(figsize=(8,12))
fig.patch.set_facecolor('aliceblue')
ax.set_axis_off()
for x, y, label,state in zip(gdf_late.centroid.x, gdf_late.centroid.y, gdf_late.orders_late_percent.round(2),gdf_late['id']):
    if state == "GO":      # ← el estado que quieres mover
        y = y - 0.8  
    elif state=="DF":
        y=y+0.5
    ax.annotate(label, xy=(x-1, y), xytext=(0, 0), textcoords="offset points", size=9,color="white", weight='bold',
                path_effects=[pe.withStroke(linewidth=2, foreground="black")])

gdf_late.plot('orders_late_percent',
        legend=True, 
        legend_kwds={"orientation": "horizontal",},
        edgecolor='black',
        linewidth=0.4,
        ax=ax)
st.pyplot(fig)