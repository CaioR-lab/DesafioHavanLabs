import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime
import json

#Variáveis
datafile = 'data.json'
mainTaxa = float(0.1)

# Retira os valores da API do Banco Central Europeu
link = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
xml = requests.get(link)
sp = soup(xml.content, 'html.parser')
allcr = sp.findAll('cube')
# Salva os valores em um dicionário
valores = {
    'eur': 1
}

for a in allcr:
    try:
        currency, rate = a['currency'].lower(), float(a['rate'])
        valores[currency] = rate
    except:
        pass
#Funções
def transaction(arg1):
    # Valor para conversão
    inputValorini = 0
    while not inputValorini:
        try:
            inputValorini = float(input('---\nInsira o valor que deseja converter: ').replace(',', '.').strip())
        except:
            print('Valor inválido.\nApenas valores numéricos\nEx.: 10, 20, 12.10')
    # Moeda para conversão
    while 1:
        print('Suas opções são:', list(valores))
        inputMoedaini = input('Insira a moeda a ser convertida: ').lower().strip()
        if inputMoedaini not in valores:
            print('Moeda inválida.')
        else:
            break
    # Moeda final
    while 1:
        inputMoedafin = input('Insira a moeda para qual deseja converter: ').lower().strip()
        if inputMoedafin not in valores:
            print('Moeda inválida.')
        elif inputMoedafin == inputMoedaini:
            print('Moeda de conversão é igual à moeda base.')
        else:
            break

    # Calculo da taxa e valores
    taxa = float(inputValorini * mainTaxa)
    valortaxado = inputValorini - taxa
    valorFinal = (valortaxado / valores[inputMoedaini]) * valores[inputMoedafin]
    # Resumo operação
    print('---')
    if arg1: print('Transação efetuada no nome de {}'.format(arg1))
    print(inputMoedaini.upper(), '{:,.2f} convertido para {} {:,.2f}'.format(inputValorini, inputMoedafin.upper(), valorFinal))
    print('Uma taxa de 10% do valor base ({:,.2f}) foi aplicada.'.format(taxa))
    print('---')

    output = {
        'data': datetime.now().strftime('%d/%m/%Y'),
        'valorI': {inputValorini: inputMoedaini},
        'taxa': taxa,
        'valorF': {valorFinal: inputMoedafin}
    }
    return output
# Fonções nome e data, seleciona nome do usuario e confirma
def get_name():
    done = 0
    while not done:
        userName = input('---\nInsira o nome do cliente: ').strip().title()
        ask = ''
        while ask != 'y' and ask != 'n':
            ask = input('O Nome do cliente é {}\nCerto? [y/n] '.format(userName)).strip().lower()
            if ask == 'y':
                done = 1
                return userName
            elif ask != 'n' and ask != 'y':
                print('\n---Resposta inválida, responda com Y ou N')

def load_file():
    with open(datafile, 'r', encoding='utf-8') as f:
        old_data = json.loads(f.read())
        return old_data

def save_file(new_data):
    with open(datafile, 'w+', encoding='utf-8') as f:
        json.dump(new_data, f)

def get_date(text):
    while 1:
        uInput = input(text).strip()
        try:
            date = datetime.strptime(uInput, '%d/%m/%Y')
            print('-')
            return date
        except: print('Data inválida')

# Interface, menu
textoini = '''*Casa de câmbio muito dinheiro*
---
0 para finalizar o programa
1 para efetuar uma transação
2 para simular uma conversão
3 para buscar por transações efetuadas
4 para mudar a taxa das transações (10% por padrão)
---'''

search_text = '''---
    1 para pesquisar em um intervalo de tempo específico
    2 para pesquisar um nome
    3 para ver todos
-'''
print(textoini)
while 1:
    userInput = str(input('5 para exibir o menu novamente >>> ').strip().lower())
    if userInput == '0': break
    elif userInput == '1':
        print('Iniciando transação...')

        userName = get_name()
        tr = transaction(userName)

        try: data = load_file()
        except: data = {}

        try: data[userName][datetime.now().strftime('%H-%M-%S')] = tr
        except:
            data[userName] = {
                datetime.now().strftime('%H-%M'): tr
            }
        save_file(data)
    elif userInput == '2':
        print('Iniciando SIMULAÇÃO...')
        transaction(0)
    elif userInput == '3':
        try: all_data = load_file()
        except:
            print('Erro ao carregar os dados.\nVerifique se existem dados para serem lidos.')
            all_data = {}
        print(search_text)
        userInput = str(input('>>> ').strip().lower())

        if userInput == '1': # por data
            result = {}
            print('Escreva no formato DD/MM/AAAA')
            dateIni = get_date('Insira a data inicial: ')
            dateFin = get_date('Insira a data final: ')

            for n in list(all_data):
                for t in list(all_data[n]):
                    if dateIni <= datetime.strptime(all_data[n][t]['data'], '%d/%m/%Y') <= dateFin:
                        name = n
                        valorI = '{:,.2f}'.format(float(list(all_data[n][t]['valorI'])[0]))
                        moedaI = str(all_data[n][t]['valorI'][list(all_data[n][t]['valorI'])[0]]).upper()
                        valorF = '{:.2f}'.format(float(list(all_data[n][t]['valorF'])[0]))
                        moedaF = str(all_data[n][t]['valorF'][list(all_data[n][t]['valorF'])[0]]).upper()

                        val = '{} {} para {} {}'.format(valorI, moedaI, valorF, moedaF)

                        result[t] = [name, val, all_data[n][t]['data']]
            if result:
                for a in sorted(result): print(result[a][0], '- {} -'.format(result[a][1]), result[a][2])
            else:
                print('Busca não obteve resultados')

        elif userInput == '2': # por nome
            search = input('---\nInsira o nome do cliente: ').strip().title()
            for n in list(all_data):
                if n == search:
                    print('Transações de', n)
                    for t in list(all_data[n]):
                        data = all_data[n][t]['data']

                        valorI = '{:,.2f}'.format(float(list(all_data[n][t]['valorI'])[0]))
                        moedaI = str(all_data[n][t]['valorI'][list(all_data[n][t]['valorI'])[0]]).upper()
                        valorF = '{:.2f}'.format(float(list(all_data[n][t]['valorF'])[0]))
                        moedaF = str(all_data[n][t]['valorF'][list(all_data[n][t]['valorF'])[0]]).upper()

                        print(data, '- {} {} para {} {}'.format(valorI, moedaI, valorF, moedaF))
        elif userInput == '3':
            print('---\nListando nomes:')
            for n in list(all_data):
                print(n)
        else: print('Comando inválido')
    elif userInput == '4':
        try: userInput = float(input('-\n Insira o novo valor desejado para a taxa das transações [0-100]: ').strip().replace(',','.'))
        except: print('-\nValor inválido')
        mainTaxa = userInput/100
        print('\n Nota taxa definida para {}% do valor base'.format(mainTaxa*100))
    elif userInput == '5':
        print(textoini)
    else: print('Comando inválido')