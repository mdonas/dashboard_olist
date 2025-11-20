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
gdf2 = gdf_late.copy()
gdf_late['centroid'] = gdf_late.centroid
fig,ax = plt.subplots(figsize=(8,12))
fig.patch.set_facecolor('aliceblue')
ax.set_axis_off()
for x, y, label,state in zip(gdf_late.centroid.x, gdf_late.centroid.y, gdf_late.orders_late_percent.round(2),gdf_late['id']):
    label = f"{label}%"  
    if state == "GO":      # ← el estado que quieres mover
        y = y - 0.8  
    elif state=="DF":
        y=y+0.5
    ax.annotate(label, xy=(x-1, y), xytext=(0, 0), textcoords="offset points", size=9,color="white", weight='bold',
                path_effects=[pe.withStroke(linewidth=2, foreground="black")])

mapa=gdf_late.plot('orders_late_percent',
        legend=True, 
        legend_kwds={"orientation": "horizontal",},
        edgecolor='black',
        linewidth=0.4,
        ax=ax)
gdf2.rename(columns={'id':'Estado','name':'Ciudad','orders_late':'Numero pedidos retrasados',
                     'orders_late_percent':'Porcentaje de pedidos retrasado','delay_days':'Dias de retraso promedio '},inplace=True)
m = gdf2.explore(
    "Porcentaje de pedidos retrasado",
    legend=False
)

cbar = mapa.get_figure().axes[-1]   # último axis = colorbar
cbar.set_title('Porcentaje de envíos con retraso', fontsize=10)
cbar.set_xticklabels([f"{t:.1f}%" for t in cbar.get_xticks()])
# st.pyplot(fig)

st_folium(m, width=700, height=500)