import streamlit as st
import pandas as pd
import openai
from openai import OpenAI

st.title(" Chat con tu CSV usando OpenAI")

# Cargar API Key
api_key = st.sidebar.text_input(" API Key de OpenAI", type="password")
if api_key:
    client = OpenAI(api_key=api_key)

    # Stopwords (opcional para futuras mejoras)
    STOPWORDS = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las',
                 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'es', 'lo',
                 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'fue', 'ha', 'sí',
                 'mi', 'sin', 'sobre', 'este', 'años', 'me', 'qué', 'son', 'todos']

    # Subida de archivo
    archivo = st.file_uploader(" Sube tu archivo CSV", type=["csv"])
    if archivo is not None:
        df = pd.read_csv(archivo)
        st.write(" Vista previa del archivo:")
        st.dataframe(df)

        # Convertir a string
        df_string = df.to_string()

        # Entrada del usuario
        pregunta = st.text_input(" Escribe tu pregunta sobre los datos:")

        if pregunta:
            prompt = f"""
Eres un asistente que ayuda a responder preguntas sobre una tabla de datos.
A continuación tienes la tabla completa convertida a texto. Usa únicamente esta información para responder.

Tabla:
{df_string}

Pregunta: {pregunta}
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",  # O usa "gpt-3.5-turbo"
                    messages=[
                        {"role": "system", "content": "Responde solo usando la información del contexto."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                respuesta = response.choices[0].message.content.strip()
            except Exception as e:
                respuesta = f" Error al consultar OpenAI: {e}"

            st.markdown(f" **Respuesta:** {respuesta}")
    else:
        st.info("📎 Carga un archivo CSV para comenzar.")
else:
    st.warning("🔑 Ingresa tu API key para comenzar.")
