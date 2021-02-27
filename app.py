from flask import Flask, render_template, request    #importação do flask, render template e request
<<<<<<< HEAD

=======
#clau
>>>>>>> cfb97a313bf04163fd98dfa4847eeb24f036261e
import requests, os, uuid, json #importação das bibliotecas que serão usadas ao realizar o chamado de tradução

from dotenv import load_dotenv
load_dotenv()  #função que carregará os valores do arquivo .env

app = Flask(__name__)

@app.route('/')  #rota inicial 
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])   #rota pelo método post
def index_post():
    # Lê os valores do formulário 
    original_text = request.form['text']
    target_language = request.form['language']

    # carrega os valores do .env
    key = os.environ['KEY']   #valor da chave
    endpoint = os.environ['ENDPOINT']  #valor do endpoint
    location = os.environ['LOCATION']  #valor da localização

    #  Indica o que será traduzido, a versão API (3.0) e a linguagem selecionada
    path = '/translate?api-version=3.0'
    # Adicionada o parametro de linguagem selecionada 
    target_language_parameter = '&to=' + target_language
    # Cria URL inteira
    constructed_url = endpoint + path + target_language_parameter

    # Configuração daas informações no cabeçalho, incluindo a chave de assinatura criada em .env 
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Criação do corpo do requerimento com o texto a ser traduzido 
    body = [{ 'text': original_text }]

    # Faz o chamado, utilizando o método POST 
    translator_request = requests.request('POST', constructed_url, headers=headers, json=body)
    # Recupera a resposta JSON do servidor, que inclui o texto traduzido 
    translator_response = translator_request.json()
    # Recupera o texto traduzido 
    translated_text = translator_response[0]['translations'][0]['text']

    # Chama render_template, pasando o texto traduzido, o texto original e a linguagem selecionada 
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

if __name__ == '__main__':
   app.run(debug = True)
