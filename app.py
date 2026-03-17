import pandas as pd
import streamlit as st
import plotly.express as px

#********* CARGA DE LOS DATOS *********
ruta = 'https://github.com/juliandariogiraldoocampo/ia_taltech/raw/refs/heads/main/aeropuerto/operaciones_aereas_acumuladas.csv'
df = pd.read_csv(ruta)

###############################################################################
#                             ANÁLISIS Y PROCESAMIENTO                        #
###############################################################################

# ESTADISTICOS DE LA COLUMNA 'TIPO_VUELO'
df_tipo_vuelo = df['TIPO_VUELO'].value_counts().reset_index()
df_tipo_vuelo.columns = ['TIPO_VUELO', 'count']
estadisticos = df_tipo_vuelo['count'].describe()
maximo = estadisticos['max']
minimo = estadisticos['min']
media = estadisticos['mean']

# TOP 5 AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES
df_top5_ops_aeropuerto = df['AEROPUERTO_OPERACION'].value_counts().reset_index().head(5)
df_top5_ops_aeropuerto.columns = ['AEROPUERTO_OPERACION', 'count']

# TOP 10 RUTAS CON MAYOR NÚMERO DE OPERACIONES
df['RUTA'] = df['ORIGEN'] + ' ▶ ' + df['DESTINO']
df_top10_rutas = df['RUTA'].value_counts().reset_index().head(10)
df_top10_rutas.columns = ['RUTA', 'CANTIDAD']


###############################################################################
#                      CONFIGURACIÓN GENERAL DE LA APLICACIÓN                 #
###############################################################################

# Configuración de la página
st.set_page_config(
    page_title='Operaciones Acumuladas',
    layout='centered',
    initial_sidebar_state='collapsed'
)

# # Ajuste del ancho máximo del contenedor principal a 1200 píxeles
st.markdown(
    '''
    <style>
        .block-container {
            max-width: 1200px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

paleta_barras = px.colors.qualitative.Antique
# Opciones de Paletas de colores: 'Plotly', 'D3', 'G10', 'T10', 'Alphabet', 'Dark24', 'Light24', 'Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Antique', 'Bold', 'Prism'
# https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express

###############################################################################
#                                   VISUALIZACION                             #
###############################################################################

#imagen usando el ancho del contenedor " use_container_width"
st.image('encabezado.png', use_container_width=True)
# st.title('Datos Operaciones')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Mínimo', f'{minimo:.0f}', border=True)
with col2:
    st.metric('Media', f'{media:.0f}', border=True)
with col3:
    st.metric('Máximo', f'{maximo:.0f}', border=True)

with st.expander('Ver Matriz de Datos'):
    st.dataframe(df)

with st.expander('Top 5 Aeropuertos con Mayor Número de Operaciones'):
    st.dataframe(df_top5_ops_aeropuerto)

# DISEÑO DE 2 COLUMNAS PARA LAS GRÁFICAS DE BARRAS
with st.container(border=True):
    col4, col5 = st.columns(2)
    with col4:
        #___________________________________________________________________________
        # ANÁLISIS AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES
        fig_barras = px.bar(
            df_top5_ops_aeropuerto,
            x='AEROPUERTO_OPERACION',
            y='count',
            title='Top 5 Aeropuertos con Mayor Número de Operaciones',
            labels={
                'AEROPUERTO_OPERACION': 'Aeropuerto',
                'count': 'Número de Operaciones'
            },
            color='AEROPUERTO_OPERACION',
            color_discrete_sequence=paleta_barras
        )
        fig_barras.update_layout(showlegend=False)
        # Mostrar la gráfica de barras
        st.plotly_chart(fig_barras, use_container_width=True)

    with col5:
        # ANÁLISIS DE RUTAS
        df_top10_rutas = df_top10_rutas.sort_values('CANTIDAD', ascending=True)
        fig_rutas = px.bar(
            df_top10_rutas,
            x='CANTIDAD',
            y='RUTA',
            title='Top 10 Rutas con Mayor Número de Operaciones',
            color='CANTIDAD',
            color_continuous_scale='tealgrn'
        )
        fig_rutas.update_coloraxes(showscale=False)
        # Mostrar la gráfica de barras
        st.plotly_chart(fig_rutas, use_container_width=True)