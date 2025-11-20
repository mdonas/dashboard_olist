import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import data_store as ds
import numpy as np

df_customers=ds.df_customers.copy()
df_customers_unique=ds.df_customers_unique.copy()
st.markdown("<h1 style='text-align: center;'>Analisis de Pedidos</h1>", unsafe_allow_html=True)

st.subheader('Numero de pedidos por ciudad',anchor=False,divider=True)
# ------------------------------------------------------------------------------------------------------
# Calculos tabla

# Recuperamos el df con el numero de usuarios por ciudad y estado
df_city_state_group =ds.df_city_state_group.copy()
# Añadir numero de orders al state,city
df_city_state_group_orders = df_customers.groupby(['customer_city','customer_state'], as_index=False).customer_id.count().sort_values('customer_id', ascending=False).reset_index(drop=True)
df_city_state_group_orders= df_city_state_group_orders.rename(columns={'customer_id':'order_numbers'})

#columna numero pedidos
df_city_customer_orders = df_city_state_group
df_city_customer_orders['order_number'] = df_city_state_group_orders['order_numbers']

#columna porcetaje pedidos
sum_orders = df_city_customer_orders['order_number'].sum()
df_city_customer_orders['order_percentage_%'] = ((df_city_customer_orders['order_number']/sum_orders)*100).round(2)

#columnma ratio pedidos por clientes
df_city_customer_orders['ratio_customer_order'] = (df_city_customer_orders['order_number']/df_city_customer_orders['customer_number']).round(4)
# st.write(df_city_customer_orders)

# ------------------------------------------------------------------------------------------------------
# Gráfico

fig, ax1 = plt.subplots(figsize=(25,16))
ax2 = ax1.twinx()
state_to_color=ds.state_to_color.copy()
# Asiganr datos a los ejes
x = df_city_customer_orders['customer_city'].head(5).str.capitalize().values
y1 = df_city_customer_orders['customer_number'].head(5).values
y2 = df_city_customer_orders['order_number'].head(5).values
y3 = df_city_customer_orders['ratio_customer_order'].head(5).values

#  Asignar colores a los estados
def desaturate(color, factor=0.5):  # 0 = gris, 1 = original
    rgb = mcolors.to_rgb(color)
    gray = sum(rgb)/3
    return tuple(gray + factor * (c - gray) for c in rgb)
colors_pastel = {k: desaturate(v) for k, v in state_to_color.items()}
c = df_city_state_group['customer_state'].head(5).apply(lambda x: state_to_color[x])
c_pastel = df_city_state_group['customer_state'].head(5).apply(lambda x: colors_pastel[x])

# Leyenda
labels_in = [l for l in state_to_color.keys() if l in df_city_state_group['customer_state'].head(5).values]
handles = [plt.Rectangle((0,0),1,1, color=state_to_color[label]) for label in labels_in]
ax1.legend(handles, labels_in,fontsize=26)

# Graficar datos
w, pos = 0.4, np.arange(len(x))
ax1.bar(pos - w/2 , y1, width=w, color = c_pastel)
ax1.bar(pos + w/2, y2, width=w, color = c)
ax2.plot(x, y3, marker='o',color='m',linewidth=4,markersize=15)

# Poner nota encima de la barra
for i in range(len(x)):
    ax1.text(i, y1[i]-100, y1[i], ha='right', va='top', color='white',fontsize=20)
    ax1.text(i, y2[i]+100, y2[i], ha='left', weight='bold',fontsize=20)

# dar formato
# ax1.set_xticks(pos, x)
ax1.tick_params(labelsize=20)
ax2.tick_params(labelsize=20)
ax1.set_ylabel('Clientes / Pedidos',fontsize=20,fontweight='bold')
ax1.set_xlabel('Ciudad',fontsize=20,fontweight='bold')
ax2.set_ylabel('Media pedidos por cliente',fontsize=20,fontweight='bold')
ax2.set_ylim(1.015, 1.05)

st.pyplot(fig)