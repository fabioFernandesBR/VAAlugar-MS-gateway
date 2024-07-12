# VAAlugar-MS-gateway
Repositório do projeto de Microsserviço (MS) que faz a gestão de todas as requisições do Front End e coordena a troca de informações entre outros microsserviços e APIs externas.


# Esquema simplificado do fluxo de informações entre Front End, Gateway e microsserviços / APIs externas.

https://docs.google.com/presentation/d/12pvJZ2fYTtoTkcfPAXlJNbkrVcwEYzRnLBjh1y9hf24/edit#slide=id.p
https://docs.google.com/presentation/d/e/2PACX-1vSfXcUSCZe_cCqlOBbNcvensXv6ysZqD_DIomZqSeXOKBunEWQ1YBIncFwzXu0T-Old4Ghmxlx8FQyX/pub?start=true&loop=false&delayms=60000

## 1. Pesquisa por canoas:
  1.1 Front End informa local e tipo de canoa desejados, ambos opcionais, fazendo uma chamada POST à rota /consultacanoas. Local é string, tipo de canoa é lista de strings.Veja na seção abaixo como fazer a requisição.
  1.2 Gateway faz uma chamada do tipo GraphQL para o MS VAAlugar-MS-canoas, na porta 5002.
  1.3 VAAlugar-MS-canoas retorna, para o gateway, 0, 1 ou mais canoas.
  1.4 Gateway retorna ao Front End a lista de canoas disponíveis.

### Como fazer a requisição POST à rota /consultacanoas:
A chamada é um JSON com a seguinte estrutura:
{
    "local": "string",
    "tipos": [lista de strings]
}

Exemplos:
{
    "local": "Rio de Janeiro",
    "tipos": ["OC2", "OC4"]
}

retorna:
{
  "canoas": [
    {
      "bairro": "Recreio",
      "estado": "RJ",
      "idcanoa": 1,
      "mediaAvaliacoes": 5,
      "municipio": "Rio de Janeiro",
      "nome": "E Ala E",
      "qtdeAvaliacoes": 10,
      "referencia": "Posto 12 Pedra do Pontal",
      "tipo": "OC2"
    },
    {
      "bairro": "Guaratiba",
      "estado": "RJ",
      "idcanoa": 4,
      "mediaAvaliacoes": 4.7,
      "municipio": "Rio de Janeiro",
      "nome": "Aia Ka La",
      "qtdeAvaliacoes": 9,
      "referencia": "Restinga da Marambaia",
      "tipo": "OC4"
    },
    {
      "bairro": "Recreio",
      "estado": "RJ",
      "idcanoa": 13,
      "mediaAvaliacoes": 5,
      "municipio": "Rio de Janeiro",
      "nome": "I Ka Moana",
      "qtdeAvaliacoes": 1,
      "referencia": "Posto 12 Pedra do Pontal Praia da Macumba",
      "tipo": "OC4"
    }
  ]
}



e a chamada:
{
    "local": "Sao Paulo",
    "tipos": ["OC1", "OC2"]
}

retorna: 

{
  "canoas": []
}

os parâmetros de chamada são opcionais, de modo que os seguintes exemplos são válidos:
{
    "local": "Pedra do Pontal"
}

{
    "tipos": ["OC6"]
}

{
} ==> retorna todas as canoas cadastradas no banco de dados.

## 2. Consulta da previsão do tempo
  2.1 Front End informa a o município e o estado onde está a canoa escolhida, fazendo uma chamada à rota /consultaprevisão. Veja na seção abaixo como fazer a requisição.
  2.2 Gateway faz uma consulta ao site do CPTEC/INPE, buscando por município. Exemplo: http://servicos.cptec.inpe.br/XML/listaCidades?city=rio de janeiro. O retorno é um dicionário de localidade, e o gateway deverá extrair o código do município, usando a informação do estado para tomar decisão.
  2.3 Em seguida Gateway consulta o site do CPTEC/INPE para obter a previsão do tempo para os próximos 7 dias, usando o código da localidade, identificado no passo anterior.
  2.4 Gateway retorna ao Front End a previsão do tempo para o próximos 7 dias.

### Como fazer a requisição POST à rota /consultaprevisao:
A chamada é um JSON com a seguinte estrutura:
{
  "estado": "string",
  "local": "string"
}
onde local é o município onde está a canoa escolhia, e estado é a unidade da federação onde está o município.

Exemplos:
{
  "estado": "RJ",
  "local": "Rio de Janeiro"
}

retorna:
{
  "cidade": "Rio de Janeiro",
  "estado": "RJ",
  "previsao": [
    {
      "dia": "2024-07-08",
      "iuv": 5,
      "maxima": 27,
      "minima": 20,
      "tempo": "Parcialmente Nublado"
    },
    {
      "dia": "2024-07-09",
      "iuv": 5,
      "maxima": 25,
      "minima": 19,
      "tempo": "Parcialmente Nublado"
    },
    {
      "dia": "2024-07-10",
      "iuv": 5,
      "maxima": 32,
      "minima": 21,
      "tempo": "Parcialmente Nublado"
    },
    {
      "dia": "2024-07-11",
      "iuv": 5,
      "maxima": 25,
      "minima": 20,
      "tempo": "Parcialmente Nublado"
    },
    {
      "dia": "2024-07-12",
      "iuv": 5,
      "maxima": 27,
      "minima": 19,
      "tempo": "Parcialmente Nublado"
    },
    {
      "dia": "2024-07-13",
      "iuv": 5,
      "maxima": 25,
      "minima": 20,
      "tempo": "Parcialmente Nublado"
    }
  ]
}


## 3. Confirmação da Reserva
  3.1 Front End informa a canoa escolhida, o usuario (representado por seu número de telefone) e um texto referente à data da locação, fazendo uma chamada POST à rota /confirmareserva. Veja na seção abaixo como fazer a requisição.
  3.2 Gateway faz uma chamada POST ao microsserviço de gestão de reservas (VAAlugar-MS-reservas), na rota /reserva, que deverá estar rodando na porta 5001.
  3.3 O VAAlugar-MS-reservas registra a reserva no banco de dados e retorna confirmação.
  3.4 Gateway retorna ao Front End a confirmação da reserva.

### Como fazer a requisição POST à rota /confirmareserva:
A chamada é um JSON com a seguinte estrutura:
{
  "canoa": 13,
  "data": "31/10/2024",
  "usuario": 21994497881
}
a resposta é do tipo:
{
  "canoa": 13,
  "data": "31/10/2024",
  "id_reserva": 18,
  "usuario": 21994497881
}

## 4. Listagem de Reservas
  4.1 Front End informa um usuario (representado por seu número de telefone), fazendo uma chamada POST à rota /listarreservas. Veja na seção abaixo como fazer a requisição.
  4.2 Gateway faz uma chamada GET ao microsserviço de gestão de reservas (VAAlugar-MS-reservas), na rota /reservas-usuario, que deverá estar rodando na porta 5001. 
  O retorno será uma lista de todas as reservas já feitas pelo usuário.
  4.3 Gateway faz uma chamada GraphQL ao microsserviço de gestão de avaliações (VAAlugar-MS-avaliacoes), que deverá estar rodando na porta 5003, na rota /graphql.
  O retorno será uma lista de todas as avaliações já feitas pelo usuário.
  4.4 O VAAlugar-MS-reservas vai combinar estes 2 retornos, montando um JSON único contendo, para o usuário informado, todas as reservas já feitas e as respectivas avaliações, se realizadas.
  4.5 Gateway retorna ao Front End o JSON com todas as reservas e avaliações relacionadas ao usuário informado.


## 5. Registrar avaliação
  5.1 Front End informa um usuario (representado por seu número de telefone),  um número de reserva, um número de canoa, uma nota (número entre 0 e 10) e um comentário sobre a experiência da locação da canoa, fazendo uma chamada POST à rota /avaliar. Veja na seção abaixo como fazer a requisição.
  5.2 Gateway faz uma chamada POST ao microsserviço de gestão de avaliações (VAAlugar-MS-avaliacoes), que deverá estar rodando na porta 5003, na rota /criar.
  5.3 VAAlugar-MS-avaliacoes registra as informações no banco de dados.
  5.4 VAAlugar-MS-avaliacoes também conta o número de avaliações já registradas para a canoa informada e a médias dessas notas (essa funcionalidade já está implementada no microsserviço)
  5.5 VAAlugar-MS-avaliacoes retorna a confirmação das informações persistidas no banco junto com a contagem e média de avaliações.
  5.6 Gateway recebe estas informações e faz uma chamada PATCH para o microsserviço VAAlugar-MS-gerir_canoas_2, que estará rodando na porta 5002, informando id_canoa, nova_média e nova_quantidade. O VAAlugar-MS-gerir_canoas_2 vai atualizar as informações da canoa.
  5.6 Gateway retorna as informações recebidas no passo 5.5 ao Front End.



