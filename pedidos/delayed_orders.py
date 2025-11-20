import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import pandas as pd
import data_store as ds

# df_merge_late_total=ds.df_merge_late_total.copy()
st.markdown("<h1 style='text-align: center;'>Analisis de Pedidos</h1>", unsafe_allow_html=True)

df_merge_late_total=pd.read_csv('./csv/df_merge_late_total.csv')
df_merge_late_total['days_diference_mean']=pd.to_timedelta(df_merge_late_total['days_diference_mean'])

# --------------------------------------------------------------------------------------------
st.subheader('Retraso promedio en la entrega por ciudad',anchor=False,divider=True)
#dias retraso medio
df_merge_late_total['delay_days'] = df_merge_late_total['days_diference_mean'].dt.total_seconds() / 86400
df_sorted = df_merge_late_total.sort_values('delay_days', ascending=False).head(20)
fig, ax=plt.subplots(figsize=(10,6))
state_to_color=ds.state_to_color.copy()


x = df_sorted['customer_city'].str.capitalize().values
y = df_sorted['delay_days'].values
c = df_sorted['customer_state'].apply(lambda x: state_to_color[x])
# st.write()
labels_in = df_sorted['customer_state'].drop_duplicates().values
handles = [plt.Rectangle((0,0),1,1, color=state_to_color[label]) for label in labels_in]
plt.bar(x,y,color=c)

plt.legend(handles,labels_in,ncols=4)
plt.xticks(rotation=45,ha='right')
plt.ylabel("Días",fontsize=13,fontweight='bold')
plt.xlabel("Ciudad",fontsize=13,fontweight='bold')
plt.tight_layout()
st.pyplot(fig)

# -----------------------------------------------------------------------------------------
st.subheader('Dias que tardan en llegar los pedidos de media',anchor=False,divider=True)
gdf=ds.gdf.copy()
df_delivery_time_state=ds.df_delivery_time_state.copy()
gdf_delivery = pd.merge(
    gdf,
    df_delivery_time_state,
    on='id',
    how='inner'
)
gdf_delivery['delivery_time'] = gdf_delivery['delivery_time'].dt.total_seconds() / 86400

gdf_delivery['centroid'] = gdf_delivery.centroid
fig,ax = plt.subplots(figsize=(10,14))
fig.patch.set_facecolor('aliceblue')
ax.set_axis_off()
for x, y, label,state in zip(gdf_delivery.centroid.x, gdf_delivery.centroid.y, gdf_delivery.delivery_time.round(2),gdf_delivery['id']):
    if state == "GO":      # ← el estado que quieres mover
        y = y - 0.8  
    elif state=="DF":
        y=y+0.5
    ax.annotate(label, xy=(x-1, y), xytext=(0, 0), textcoords="offset points", size=9, color='white', 
                path_effects=[pe.withStroke(linewidth=2, foreground="black")])

gdf_delivery.plot('delivery_time',
        legend=True, 
        legend_kwds={"orientation": "horizontal",},
        edgecolor='lavender',
        linewidth=0.4,
        ax=ax)
st.pyplot(fig)

# -----------------------------------------------------------------------------------------
#diagnostico
st.subheader('Distribucion de diagnostico',anchor=False,divider=True)

diagnosis_counts = df_merge_late_total['diagnosis'].value_counts().reset_index()
diagnosis_counts['diagnosis']=diagnosis_counts['diagnosis'].str.split(':').str[0]
fig2=plt.figure(figsize=(15,10))
plt.pie(diagnosis_counts['count'],labels=diagnosis_counts['diagnosis'], textprops={'fontsize': 20,'fontweight':'bold'} ,autopct=lambda pct: f"{pct:.1f}%", )
st.pyplot(fig2)

# -----------------------------------------------------------------------------------------
