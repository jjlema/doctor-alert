import requests
from bs4 import BeautifulSoup


URL_CUPO_MEDICO = "https://tsinternet.sergas.es/TSInternet/ConsultaHorariosMedicos.servlet?CUPO=#id_medico#&orixe=TSI"
IDS_CUPO = ["36342462", "36342866", "36341957", "36341452"]


for id_medico in IDS_CUPO:
    url = URL_CUPO_MEDICO.replace("#id_medico#", id_medico)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    medico = soup.find('input', {'name': 'nomemedico'})['value']
    cupo = [inp['value'] for inp in soup.find_all('input', {'name': 'telfurx'}) if 'value' in inp.attrs]
    print(f'Médico: {medico}, Cupo: {cupo}')
