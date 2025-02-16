import streamlit as st
import requests
import json

def get_crossref_data(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()["message"]
        return {
            "doi": doi,
            "title": data.get("title", ["Desconocido"])[0],
            "authors": ", ".join([author.get("given", "") + " " + author.get("family", "") for author in data.get("author", [])]),
            "journal": data.get("container-title", ["Desconocida"])[0],
            "year": data.get("published-print", {}).get("date-parts", [["Desconocido"]])[0][0],
            "url": data.get("URL", "Desconocido"),
            "read": False
        }
    else:
        return None

def send_to_api(record):
    api_url = "http://127.0.0.1:8000/guardar_doi"
    response = requests.post(api_url, json=record)
    return response.json()

st.title("Consulta de DOI en CrossRef")
st.write("https://doi.org/10.24215/16696581e726")
st.write("http://dx.doi.org/10.22201/fcpys.2448492xe.2024.250.80821")
doi = st.text_input("Ingrese un DOI:")

if "submission_data" not in st.session_state:
    st.session_state.submission_data = None
if "api_response" not in st.session_state:
    st.session_state.api_response = None

if st.button("Consultar") and doi:
    result = get_crossref_data(doi)
    if result:
        st.session_state.submission_data = result

if st.session_state.submission_data:
    st.write("### Información obtenida")
    st.session_state.submission_data["title"] = st.text_input("Título", st.session_state.submission_data["title"])
    st.session_state.submission_data["authors"] = st.text_input("Autores", st.session_state.submission_data["authors"])
    st.session_state.submission_data["journal"] = st.text_input("Revista", st.session_state.submission_data["journal"])
    st.session_state.submission_data["year"] = st.text_input("Año", str(st.session_state.submission_data["year"]))
    st.session_state.submission_data["url"] = st.text_input("URL", st.session_state.submission_data["url"])
    st.session_state.submission_data["read"] = st.checkbox("Leído", value=st.session_state.submission_data["read"])
    
    if st.button("Confirmar envío"):
        st.session_state.api_response = send_to_api(st.session_state.submission_data)
        st.session_state.submission_data = None

if st.session_state.api_response:
    st.write("### Respuesta de la API:")
    st.json(st.session_state.api_response)
