import pandas as pd
import matplotlib.pyplot as plt
import data_store as ds
import streamlit as st
import matplotlib.patheffects as pe

df_state_group=ds.df_state_group.copy()
gdf=ds.gdf.copy()

st.markdown("<h1 style='text-align: center;'>Analisis de Ventas</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------------------------
st.subheader("Mapa de ventas por estado",anchor=False,divider=True)

df_state_group.sort_values(by='customer_state').reset_index(drop=True)

# Añadir total pedidos por estado al geoDataframe
gdf['order_number'] = df_state_group.sort_values(by='customer_state')['customer_unique_id'].reset_index(drop=True)
gdf2=gdf.copy()

gdf['centroid'] = gdf.centroid
fig,ax = plt.subplots(figsize=(10,14))
ax.set_axis_off()
for x, y, label in zip(gdf.centroid.x, gdf.centroid.y, gdf.name):
    ax.annotate(label, xy=(x-1.5, y), xytext=(0, 0), textcoords="offset points", size=8, color='white', weight='bold',
                path_effects=[pe.withStroke(linewidth=2, foreground="black")])

 
gdf.plot('order_number',
        cmap='turbo',
        legend=True, 
        legend_kwds={"label": "Total de ventas", "orientation": "horizontal"},
        edgecolor='black',
        linewidth=0.4,
        ax=ax)

st.pyplot(fig)



# -------------------------------------------------------------------------------
fig2,ax2 = plt.subplots(figsize=(10,14))
m=gdf2.explore("order_number", legend=False)
# st_folium(m, width=700, height=500)

