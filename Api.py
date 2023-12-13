from flask import Flask, request, render_template
import os
import csv
import subprocess  # Adicionado o módulo subprocess
import time
import pywhatkit
from pynput.keyboard import Key, Controller
import pandas as pd
import pyautogui

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return "Nenhum arquivo CSV enviado", 400

    csv_file = request.files['csv_file']

    if csv_file.filename == '':
        return "Nome de arquivo vazio", 400


    if csv_file and allowed_file(csv_file.filename):
        filename = "uploads//Table.csv"
        csv_filename = os.path.join(filename)

        csv_file.save(filename)

        try:
            with open(csv_filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                data = {"data": [], "columns": []}

                # Lê as colunas do arquivo CSV
                data["columns"] = next(csv_reader)

                # Lê os dados do arquivo CSV
                for row in csv_reader:
                    data["data"].append(row)

                return render_template("table.html", data=data)
        except Exception as e:
            return f"Erro ao processar o arquivo CSV: {str(e)}", 400
    else:
        return "Tipo de arquivo não suportado. Por favor, envie um arquivo CSV válido.", 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/Enviar', methods=['GET'])
def enviar():
    import pandas as pd
    import pywhatkit
    import pyautogui
    from pynput.keyboard import Controller, Key
    import time

    df = pd.read_csv('uploads/Table.csv')

    numero_array = df['Telefone'].to_numpy()
    msg_array = df['Mensagem'].to_numpy()

    phone_numbers = numero_array  
    messages = msg_array

    def send_whatsapp_message(phone_numbers, messages):
        for i, phone_number in enumerate(phone_numbers):
            try:
                # Converta o número de telefone para string antes de passá-lo para a função
                phone_str = str(phone_number)
                msg_str = messages[i]

                pywhatkit.sendwhatmsg_instantly(
                    phone_no=phone_str,
                    message=msg_str,
                    tab_close=False
                )
                time.sleep(10) # Ajuste o atraso conforme necessário
                print("Before pressing Enter")
                pyautogui.click(clicks=1)
                pyautogui.press('enter')
                print(f"Message sent to {phone_str}!")
            except Exception as e:
                print(f"Error sending message to {phone_str}: {str(e)}")
            time.sleep(5)
            pyautogui.hotkey('ctrl', 'w')  # Isso pressiona as teclas Ctrl + W para fechar a guia

    send_whatsapp_message(phone_numbers, messages)

    return 'ok'  # Retorna uma resposta válida

if __name__ == '__main__':
    app.run(debug=True)