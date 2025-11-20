import streamlit as st
st.set_page_config(page_title='Dashboard Interactivo EDA',page_icon='./olist.png',layout='centered')


st.markdown('<div class="custom-container">', unsafe_allow_html=True)
pages = {
    "Inicio":[
        st.Page("./home.py",title='Inicio')
    ],
    "Estado": [
        st.Page("./estados/user_state.py", title="Clientes por estado"),
        st.Page("./estados/user_state_city.py", title="Clientes por estado y ciudad"),
    ],
    "Pedidos": [
        st.Page("./pedidos/customer_order.py", title="Clientes por pedido"),
        st.Page("./pedidos/delayed_orders.py", title="Pedidos retrasados"),
        st.Page("./pedidos/map_delayed_orders_state.py", title="Mapa de porcentaje de pedidos retrasados por estado"),

    ],
    'Reseñas':[
        st.Page("./reviews/review_state.py", title="Reseñas por estado"),
    ],
    'Ventas':[
        st.Page("./ventas/top_category.py",title='Categorías dominantes'),
        st.Page("./ventas/sales_category.py",title="Ventas por categoría"),
        st.Page("./ventas/map_sales_state.py", title="Mapa de ventas por estado")
    ]
}
pg = st.navigation(pages,position='top')
pg.run()
