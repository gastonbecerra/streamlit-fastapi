import streamlit as st
import requests

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
doi = st.text_input("Ingrese un DOI:")

if st.button("Consultar") and doi:
    result = get_crossref_data(doi)
    if result:
        with st.form("doi_form"):
            st.write("### Información obtenida")
            title = st.text_input("Título", result['title'])
            authors = st.text_input("Autores", result['authors'])
            journal = st.text_input("Revista", result['journal'])
            year = st.text_input("Año", str(result['year']))
            url = st.text_input("URL", result['url'])
            read = st.checkbox("Leído", value=result["read"])
            submitted = st.form_submit_button("Guardar en la API")
            if submitted:
                result["title"] = title
                result["authors"] = authors
                result["journal"] = journal
                result["year"] = int(year) if year.isdigit() else result["year"]
                result["url"] = url
                result["read"] = read
                response = send_to_api(result)
                st.write(response)