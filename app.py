import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configuración de página con diseño ancho
st.set_page_config(
    page_title="Peralta Archery - Control de Inventario",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual moderno y limpio
st.markdown("""
    <style>
    .main-header {
        font-size: 26px;
        font-weight: 700;
        color: #1f4e78;
    }
    .sub-slogan {
        font-size: 14px;
        color: #595959;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENCABEZADO Y LOGOTIPO CORPORATIVO (Esquina Superior Derecha)
# ---------------------------------------------------------
col_title, col_logo = st.columns([4, 1])

with col_title:
    st.markdown('<p class="main-header">🎯 Peralta Archery Community / Shop</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-slogan">"Precisión, Sostenibilidad y Acceso al Deporte" | ODS: [3] Salud y Bienestar | [4] Educación | [12] Producción Responsable</p>', unsafe_allow_html=True)

with col_logo:
    st.image("https://images.unsplash.com/photo-1511882150382-421056c89033?w=160", width=110, caption="Peralta Archery")

st.markdown("---")

# ---------------------------------------------------------
# INICIALIZACIÓN DE LA BASE DE DATOS DE INVENTARIO
# ---------------------------------------------------------
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {
            "ID": "XS-001", "Empresa": "XS Wings", "Artículo": "Plumas Spin Wings", 
            "Tipo/Clase": "Fluorescente", "Color": "Naranja Neón", "Tamaño": "50mm", 
            "Cantidad": 35, "Fecha Compra": "2026-01-15", "Fecha Venta": "Pendiente", 
            "Tipo Cliente": "N/A", "Rotación (Días)": 0
        },
        {
            "ID": "TAT-002", "Empresa": "TATHLUM", "Artículo": "V-Bar Mount AKT-SP102", 
            "Tipo/Clase": "Aluminio CNC", "Color": "Negro Metálico", "Tamaño": "Estándar", 
            "Cantidad": 8, "Fecha Compra": "2026-02-01", "Fecha Venta": "2026-02-20", 
            "Tipo Cliente": "Club de Arquería", "Rotación (Días)": 19
        },
        {
            "ID": "DEC-003", "Empresa": "DECUT", "Artículo": "Rainbow F2 Scope", 
            "Tipo/Clase": "Óptica 8X", "Color": "Negro / Nivel Verde", "Tamaño": "30mm", 
            "Cantidad": 2, "Fecha Compra": "2026-03-01", "Fecha Venta": "2026-03-15", 
            "Tipo Cliente": "Competidor Elite", "Rotación (Días)": 14
        },
        {
            "ID": "SVB-004", "Empresa": "SvBONY", "Artículo": "Telémetro Láser Óptico", 
            "Tipo/Clase": "600m Outdoor", "Color": "Negro", "Tamaño": "Portátil", 
            "Cantidad": 4, "Fecha Compra": "2026-04-10", "Fecha Venta": "Pendiente", 
            "Tipo Cliente": "N/A", "Rotación (Días)": 0
        }
    ])

# Lista oficial de Empresas / Proveedores solicitada
empresas_oficiales = ["XS Wings", "BICASTER", "ACCMOS", "NIKA", "SvBONY", "TATHLUM", "SPG", "DECUT", "AMEYXGS"]

# ---------------------------------------------------------
# BARRA LATERAL (PANEL DE CONTROL Y NAVEGACIÓN)
# ---------------------------------------------------------
st.sidebar.header("⚙️ Gestión y Módulos")
modulo = st.sidebar.selectbox(
    "Seleccione una Operación:",
    ["📊 Ver Inventario y Métricas", "📦 Ingresar Nueva Compra (Stock)", "🛒 Registrar Venta y Salida", "🏢 Administrar Marcas y Catálogo"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtrado Rápido")
empresa_filtro = st.sidebar.selectbox("Filtrar por Empresa / Marca:", ["Todas"] + empresas_oficiales)

# ---------------------------------------------------------
# MÓDULO 1: VER INVENTARIO Y MÉTRICAS
# ---------------------------------------------------------
if modulo == "📊 Ver Inventario y Métricas":
    st.subheader(f"Inventario General de Mercancía - Vista: [{empresa_filtro}]")
    
    df = st.session_state.inventario.copy()
    if empresa_filtro != "Todas":
        df = df[df["Empresa"] == empresa_filtro]
        
    # Alerta visual de stock bajo (< 3 unidades)
    articulos_bajos = df[df["Cantidad"] <= 3]
    if not articulos_bajos.empty:
        st.warning(f"⚠️ **Alerta de Stock Crítico:** Hay {len(articulos_bajos)} referencia(s) con 3 unidades o menos en existencia.")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Métricas clave
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Referencias", len(df))
        c2.metric("Unidades Totales en Stock", int(df["Cantidad"].sum()))
        c3.metric("Marcas Representadas", df["Empresa"].nunique())
        stock_critico = len(df[df["Cantidad"] <= 3])
        c4.metric("Ítems en Stock Crítico", stock_critico)
        
        st.markdown("---")
        st.subheader("📈 Análisis Gráfico de Existencias y Rotación")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("**Stock Actual por Artículo**")
            st.bar_chart(df.set_index("Artículo")["Cantidad"])
        with col_g2:
            st.markdown("**Rotación de Inventario (Días hasta venta)**")
            df_vendidos = df[df["Rotación (Días)"] > 0]
            if not df_vendidos.empty:
                st.bar_chart(df_vendidos.set_index("Artículo")["Rotación (Días)"])

# ---------------------------------------------------------
# MÓDULO 2: INGRESAR NUEVA COMPRA (STOCK)
# ---------------------------------------------------------
elif modulo == "📦 Ingresar Nueva Compra (Stock)":
    st.subheader("📦 Registrar Entrada de Nueva Mercancía (Importación)")
    
    with st.form("form_compra"):
        col1, col2, col3 = st.columns(3)
        id_articulo = col1.text_input("Código / ID del Artículo")
        empresa_prov = col2.selectbox("Empresa / Proveedor", empresas_oficiales)
        nombre_item = col3.text_input("Nombre del Artículo / Ítem")
        
        col4, col5, col6 = st.columns(3)
        tipo_clase = col4.text_input("Tipo o Clase (Ej. Fluorescente, CNC)")
        color_item = col5.text_input("Color")
        tamano_item = col6.text_input("Tamaño / Especificación")
        
        col7, col8 = st.columns(2)
        cantidad_ing = col7.number_input("Cantidad Ingresada", min_value=1, value=10)
        fecha_compra = col8.date_input("Fecha de Compra", value=datetime.today())
        
        submitted_compra = st.form_submit_button("📥 Guardar e Ingresar al Inventario")
        
        if submitted_compra and id_articulo and nombre_item:
            nuevo_registro = {
                "ID": id_articulo, "Empresa": empresa_prov, "Artículo": nombre_item,
                "Tipo/Clase": tipo_clase if tipo_clase else "Estándar",
                "Color": color_item if color_item else "Único",
                "Tamaño": tamano_item if tamano_item else "Único",
                "Cantidad": int(cantidad_ing), "Fecha Compra": str(fecha_compra),
                "Fecha Venta": "Pendiente", "Tipo Cliente": "N/A", "Rotación (Días)": 0
            }
            st.session_state.inventario = pd.concat([st.session_state.inventario, pd.DataFrame([nuevo_registro])], ignore_index=True)
            st.success(f"¡Éxito! Se han ingresado {cantidad_ing} unidades de '{nombre_item}' al inventario.")

# ---------------------------------------------------------
# MÓDULO 3: REGISTRAR VENTA Y SALIDA
# ---------------------------------------------------------
elif modulo == "🛒 Registrar Venta y Salida":
    st.subheader("🛒 Registrar Salida por Venta / Despacho a Cliente")
    
    df_inv = st.session_state.inventario
    if df_inv.empty or df_inv["Cantidad"].sum() == 0:
        st.warning("No hay artículos con stock disponible.")
    else:
        with st.form("form_venta"):
            ids_disponibles = df_inv[df_inv["Cantidad"] > 0]["ID"].tolist()
            id_venta = st.selectbox("Seleccione el ID del Artículo", ids_disponibles)
            
            item_info = df_inv[df_inv["ID"] == id_venta].iloc[0]
            st.info(f"**Artículo:** {item_info['Artículo']} | **Marca:** {item_info['Empresa']} | **Stock Disponible:** {item_info['Cantidad']}")
            
            col_v1, col_v2 = st.columns(2)
            cantidad_venta = col_v1.number_input("Cantidad Vendida", min_value=1, max_value=int(item_info['Cantidad']), value=1)
            fecha_venta = col_v2.date_input("Fecha de Venta", value=datetime.today())
            tipo_cliente = st.selectbox("Tipo de Cliente", ["Club de Arquería", "Competidor Elite", "Principiante / Aficionado", "Tienda Deportiva", "Entrenador"])
            
            submitted_venta = st.form_submit_button("🛒 Procesar Venta y Actualizar Stock")
            
            if submitted_venta:
                idx = st.session_state.inventario[st.session_state.inventario["ID"] == id_venta].index[0]
                stock_actual = st.session_state.inventario.at[idx, "Cantidad"]
                
                if stock_actual >= cantidad_venta:
                    st.session_state.inventario.at[idx, "Cantidad"] = stock_actual - cantidad_venta
                    st.session_state.inventario.at[idx, "Fecha Venta"] = str(fecha_venta)
                    st.session_state.inventario.at[idx, "Tipo Cliente"] = tipo_cliente
                    
                    # Calcular rotación
                    f_compra = datetime.strptime(st.session_state.inventario.at[idx, "Fecha Compra"], "%Y-%m-%d").date()
                    dias_rotacion = (fecha_venta - f_compra).days
                    st.session_state.inventario.at[idx, "Rotación (Días)"] = max(0, dias_rotacion)
                    
                    st.success(f"¡Venta registrada! Stock actualizado automáticamente. Quedan {stock_actual - cantidad_venta} unidades.")

# ---------------------------------------------------------
# MÓDULO 4: ADMINISTRAR MARCAS Y CATÁLOGO
# ---------------------------------------------------------
elif modulo == "🏢 Administrar Marcas y Catálogo":
    st.subheader("🏢 Gestión de Proveedores / Marcas Oficiales")
    cols = st.columns(3)
    for i, marca in enumerate(empresas_oficiales):
        with cols[i % 3]:
            st.success(f"🏷️ **{marca}**")