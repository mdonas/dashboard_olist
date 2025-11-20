import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import data_store as ds

df_customer_unique_with_order_date=pd.read_csv('./csv/df_customer_unique_with_order_date.csv',parse_dates=['order_purchase_timestamp']) 
st.markdown("<h1 style='text-align: center;'>Analisis de Pedidos</h1>", unsafe_allow_html=True)

 # fecha_inicio = ['order_purchase_timestamp'].min().date()
min=df_customer_unique_with_order_date['order_purchase_timestamp'].min().date()
max=df_customer_unique_with_order_date['order_purchase_timestamp'].max().date()

# x=st.slider('Fecha',1/1/2010,1/1/2025)
st.subheader("Filtrar usuarios por fecha",anchor=False)
fechaElegida = st.slider(
    "Fecha",
    min_value=min,
    value=(min,max),
    max_value=max,
    key='slider_fecha'
)
st.button('Reiniciar filtro de fecha',width='stretch',on_click=lambda: st.session_state.update({"slider_fecha": (min, max)}))

# Filtramos la fecha
df_fecha_filtered_unique=(df_customer_unique_with_order_date[
    (df_customer_unique_with_order_date['order_purchase_timestamp'].dt.date >= fechaElegida[0])&
    (df_customer_unique_with_order_date['order_purchase_timestamp'].dt.date <= fechaElegida[1])])

# st.write(df_customers_unique)

#Filtramos para calcular el numero de usuarios
df_city_state_group_u = df_fecha_filtered_unique.groupby(['customer_city','customer_state'], as_index=False).customer_unique_id.count().sort_values('customer_unique_id', ascending=False).reset_index(drop=True)
df_city_state_group_u.rename(columns={'customer_city':'Ciudad','customer_state':'Estado','customer_unique_id': 'Total usuarios distintos'}
                            ,inplace=True)
st.subheader(f"Clientes desde: {fechaElegida[0]}  hasta: {fechaElegida[1]}",anchor=False)
# st.write(df_city_state_group_u.head(10))

# ---------------------------------------------------------------------------------------------------------------
# Gráfico usuarios por ciudad
state_to_color=ds.state_to_color.copy()
fig, ax = plt.subplots(figsize=(17,10))

x = df_city_state_group_u['Ciudad'].head(5).str.capitalize().values
y = df_city_state_group_u['Total usuarios distintos'].head(5).values
c = df_city_state_group_u['Estado'].head(5).apply(lambda x: state_to_color[x])

labels_in = [l for l in state_to_color.keys() if l in df_city_state_group_u['Estado'].head(5).values]
handles = [plt.Rectangle((0,0),1,1, color=state_to_color[label]) for label in labels_in]

ax.bar(x,y, color=c)

# Poner nota encima de la barra
for i in range(len(x)):
    ax.text(i, y[i], y[i], ha='center',va='bottom',fontsize=13,fontweight='bold')

ax.tick_params(labelsize=13)
ax.set_ylabel('Clientes',fontsize=15,fontweight='bold')
ax.set_xlabel('Ciudad',fontsize=15,fontweight='bold')
ax.legend(handles, labels_in,fontsize=15)
st.pyplot(fig)