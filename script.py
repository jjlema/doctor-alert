import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_TO = [email.strip() for email in os.environ["EMAIL_TO"].split(",")]
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
URL_CUPO_MEDICO = "https://tsinternet.sergas.es/TSInternet/ConsultaHorariosMedicos.servlet?CUPO=#id_medico#&orixe=TSI"
IDS_MEDICO = [id.strip() for id in os.environ["IDS_MEDICO"].split(",")]


def is_medico_available(id_medico: str) -> tuple[str,bool]:
    url = URL_CUPO_MEDICO.replace("#id_medico#", id_medico)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    medico = soup.find('input', {'name': 'nomemedico'})['value']
    cupos = [inp['value'] for inp in soup.find_all('input', {'name': 'telfurx'}) if 'value' in inp.attrs]
    return medico, any(cupo == 'ABERTO' for cupo in cupos)


def send_email_notification(medicos:list[str]):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    msg["Subject"] = "Medico disponible"
    texto = "Los siguientes médicos tienen citas disponibles:\n\n" + "\n".join(medicos)
    msg.attach(MIMEText(texto,"plain"))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Cambia si usas otro servicio
            server.starttls()  # Seguridad TLS
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Correo enviado correctamente")
    except Exception as e:
        print("Error al enviar correo")


def main():
    medicos_disponibles = []
    for id_medico in IDS_MEDICO:
        medico, disponible = is_medico_available(id_medico)
        if disponible:
            medicos_disponibles.append(medico)
    if medicos_disponibles:
        send_email_notification(medicos_disponibles)
    else:
        print("No hay médicos disponibles en este momento.")

if __name__ == "__main__":
    main()
