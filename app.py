from flask import Flask, render_template, request   
import requests, os, uuid, json 
from dotenv import load_dotenv
load_dotenv()  

'''
Importações das bibliotecas que serão utilizadas 
load_dotenv() é a função que carregará os valores do arquivo .env
'''

app = Flask(__name__)

@app.route('/',  methods=['GET']) 
def index():
    return render_template('index.html')
    ''' 
    @app.route indica que a rota será criada no caminho "/",  método utilizado é GET. 
    Flask chama a função index que retorna o modelo html index.html
    '''


@app.route('/', methods = ['POST'])  
def index_post():
    original_text = request.form['text']
    target_language = request.form['language']
    '''
    Indica a rota pelo método POST
    Flask chama a função index_post que começa a seguir pelas etapas:
    1 - lê o texto inserido e o idioma selecionado no formulário
    '''
 
    key = os.environ['KEY']   
    endpoint = os.environ['ENDPOINT'] 
    location = os.environ['LOCATION']  

    '''
    2 - Carrega as variáveis ambientais do Serviço de Tradução, que se encontram no arquivo .env
    '''

    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    constructed_url = endpoint + path + target_language_parameter
    '''
    3- Indica o que será traduzido, criando o caminho para chamar o serviço API, 
    adicionando o parametro de linguagem selecionada e criando a URL inteira. 

    '''

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    ''' 
    4 - Configurações das informações de cabeçalho: 
    Chave para o serviço de Tradução do Azure criada em .env
    Localização do serviço
    Id arbitrária para a tradução
    '''

    body = [{ 'text': original_text }]
    translator_request = requests.request('POST', constructed_url, headers=headers, json=body)
    translator_response = translator_request.json()
    translated_text = translator_response[0]['translations'][0]['text']

    '''
    5 - Criação do requerimento que inclui o texto a ser traduzido
        Chama o serviço de tradução através do método post em requests
        Recupera a resposta JSON do servidos (que inclui o texto traduzido)
        Recupera o texto traduzido 
    '''   

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

    '''
    6 - Chama o render_template, que exibirá a página de results com o texto traduzido, o texto original 
    e a linguagem selecionada 
    '''

if __name__ == '__main__':
   app.run(debug = True)

'''
    Instrução condicional if é satisfeita e o método app.run () será executado. 
    O modo Debug é ativado ao passar o valor TRUE par o parâmetro debug.
'''


