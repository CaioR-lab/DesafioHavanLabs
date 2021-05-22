## Conversor de moeda: 
## Casa de Cambio Muito Dinheiro
Esse script em Python converte valores de moedas, cria banco de dados e realiza buscas.
## Instruções: 
Essas instruções criarão uma cópia  do projeto funcional em sua maquina local pra desenvolvimento e testes.

### Pré-requisitos: 

* [Python](https://www.python.org) versão 3.8.8 (testado)
* BS4 lib
* Requests lib

### Preparando:

Faça uma cópia do diretório do projeto.
```
git clone https://github.com/CaioR-lab/DesafioHavanLabs.git
```
Crie um ambiente virtual em Python e ative.

Instale os requerimentos.

```
pip install requests
```
```
pip install bs4
```
## Executando testes:
Tem uma `data.json`que pode ser usada pra testar o programa.
Se o seu terminal se parece com isso:
```
├── 1
├── 2
├── 3
├── 4
├── 5
```
Não existem mensagens de erros e a função busca mostra os dados cadastrados em colunas, então tudo está funcionando corretamente.

## Documentação: 
A Base de dados contendo o valor de câmbio é feita sobre a API do [Banco Central Europeu](https://www.ecb.europa.eu/home), encontrada na variável:
`link = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml''` 
Portanto se por algum motivo a API não se encontrar mais nesse domínio, você pode facilmente altera-la, se compatível.

O script gera um arquivo banco de dados`datafile = 'data.json'` onde ficam armazenadas as transações efetuadas.

### Como utilizar: 
Selecione uma das opções do terminal para ter acesso aos próximos passos.
```
├── 1
│   ├── 1.nova opção
│   ├── 2.nova opção
├── 2
├── 3
├── 4
├── 5
```
Caso realize uma transação, os dados serão salvos automaticamente no banco de dados.
Para ter acesso aos dados utilize a opção busca no terminal.

