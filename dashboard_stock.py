# dashboard_stock.py
import os
import streamlit as st
import pandas as pd

CSV_PATH = "stock.csv"

# Data inicial (se usa si no existe CSV)
data = {
    "Artículo": ["Impresora HP 4100", "Impresora Epson L3150", "Cartucho Negro HP", "Cartucho Color Epson"],
    "Cantidad": [5, 2, 15, 8],
    "Ubicación": ["Depósito General", "Depósito General", "Oficina 1", "Oficina 2"]
}

# Cargar desde CSV si existe, sino usar data inicial
if os.path.exists(CSV_PATH):
    df_init = pd.read_csv(CSV_PATH)
else:
    df_init = pd.DataFrame(data)

# Guardar DataFrame en session_state para persistir entre reruns
if "df" not in st.session_state:
    st.session_state.df = df_init.copy()

st.set_page_config(page_title="Dashboard de Stock", layout="wide")

st.title("Dashboard de Stock")
st.write("Visualización y gestión de inventario interno")

# Filtro por ubicación (usa el DataFrame de session_state)
ubicaciones = st.multiselect("Filtrar por ubicación:", options=st.session_state.df["Ubicación"].unique())
if ubicaciones:
    df_mostrar = st.session_state.df[st.session_state.df["Ubicación"].isin(ubicaciones)]
else:
    df_mostrar = st.session_state.df

# Mostrar tabla
st.subheader("Inventario actual")
st.dataframe(df_mostrar, use_container_width=True)

# Agregar nuevo artículo
st.subheader("Agregar nuevo artículo")
with st.form("form_agregar"):
    articulo = st.text_input("Nombre del artículo")
    cantidad = st.number_input("Cantidad", min_value=0, step=1, value=0)
    ubicacion = st.text_input("Ubicación")
    submitted = st.form_submit_button("Agregar")

    if submitted:
        if not articulo or not ubicacion:
            st.error("Completa el nombre y la ubicación.")
        elif cantidad <= 0:
            st.error("La cantidad debe ser mayor a cero.")
        else:
            mask = ((st.session_state.df["Artículo"] == articulo) &
                    (st.session_state.df["Ubicación"] == ubicacion))
            if mask.any():
                st.session_state.df.loc[mask, "Cantidad"] += int(cantidad)
                st.success(f"✅ Cantidad actualizada para {articulo} en {ubicacion}")
            else:
                nuevo = pd.DataFrame({"Artículo": [articulo], "Cantidad": [int(cantidad)], "Ubicación": [ubicacion]})
                st.session_state.df = pd.concat([st.session_state.df, nuevo], ignore_index=True)
                st.success(f"✅ {articulo} agregado correctamente.")
        st.session_state.df.to_csv(CSV_PATH, index=False)

# Botón para guardar manualmente
if st.button("💾 Guardar inventario"):
    st.session_state.df.to_csv(CSV_PATH, index=False)
    st.success(f"Inventario guardado satisfactoriamente")
