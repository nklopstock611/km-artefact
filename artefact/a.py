import streamlit as st
import pandas as pd

# Inicializar el DataFrame en el estado de sesión si no existe
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'Nombre': ['Alice', 'Bob', 'Charlie'],
        'Edad': [25, 30, 35],
        'Seleccionado': [False, False, False]
    })

# Función para manejar el clic del botón
def select_row(index):
    st.session_state.df.at[index, 'Seleccionado'] = not st.session_state.df.at[index, 'Seleccionado']

# Mostrar el DataFrame y botones
for index, row in st.session_state.df.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(row)
    with col2:
        btn_label = "Deseleccionar" if row['Seleccionado'] else "Seleccionar"
        if st.button(btn_label, key=f"button_{index}"):
            select_row(index)

st.write("DataFrame actualizado:")
st.dataframe(st.session_state.df)
