import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz

# Configuración de la interfaz móvil
st.set_page_config(page_title="StampCam Pro", layout="centered")
st.title("📸 Estampador Técnico de Faena")

# 1. Configuración de los Datos en Pantalla
st.sidebar.header("📝 Datos del Sello")
ubicacion = st.sidebar.text_input("UBICACIÓN:", "IIFF")
nota = st.sidebar.text_input("NOTA:", "Limpieza de baños")
coordenadas_manuales = st.sidebar.text_input("COORDENADAS (Opcional):", "-26.24232988 -70.10212453")

# Selector de origen de la foto
opcion = st.radio("Selecciona una opción:", ["📷 Tomar Foto en Tiempo Real", "📁 Cargar de la Galería"])

foto_objeto = None

if opcion == "📷 Tomar Foto en Tiempo Real":
    foto_objeto = st.camera_input("Captura la foto para el informe")
else:
    foto_objeto = st.file_uploader("Selecciona una foto existente", type=["jpg", "jpeg", "png"])

# 2. Procesamiento del Estampado Profesional
if foto_objeto is not None:
    imagen = Image.open(foto_objeto).convert("RGB")
    canvas = ImageDraw.Draw(imagen)
    ancho, alto = imagen.size
    
    # Automatizar fecha y hora de Chile
    zona_cl = pytz.timezone('America/Santiago')
    fecha_hora = datetime.now(zona_cl).strftime("%d-%m-%Y %I:%M:%S %p").lower().replace("am", "a. m.").replace("pm", "p. m.")
    
    # Tamaño de letra estándar oficial (2.2%)
    tamano_fuente = int(max(ancho, alto) * 0.022)
    try:
        fuente = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", tamano_fuente)
    except:
        fuente = ImageFont.load_default()
        
    # Líneas de texto tal como las necesitas
    lineas = [
        f"{fecha_hora}",
        f"{coordenadas_manuales}",
        f"UBICACIÓN: {ubicacion}",
        f"NOTA: {nota}"
    ]
    
    margen_derecho = int(ancho * 0.04)   
    margen_inferior = int(alto * 0.04)  
    espaciado_lineas = int(tamano_fuente * 1.25) 
    pos_y_actual = alto - margen_inferior - tamano_fuente

    for linea in reversed(lineas):
        ancho_texto = canvas.textlength(linea, font=fuente)
        pos_x = ancho - ancho_texto - margen_derecho
        canvas.text((pos_x, pos_y_actual), linea, fill=(255, 255, 255), font=fuente)
        pos_y_actual -= espaciado_lineas

    # Mostrar resultado en el celular
    st.image(imagen, caption="Vista Previa de la Foto Oficial", use_container_width=True)
    
    # Botón para descargar directo en el celular
    imagen.save("foto_reporte.jpg", quality=100)
    with open("foto_reporte.jpg", "rb") as file:
        st.download_button(
            label="💾 Descargar Foto Estampada",
            data=file,
            file_name=f"REPORTE_{ubicacion.replace(' ', '_')}.jpg",
            mime="image/jpeg"
        )
