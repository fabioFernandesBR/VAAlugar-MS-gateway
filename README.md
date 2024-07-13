# VAAlugar-MS-gateway
Repositório do projeto de Microsserviço (MS) que faz a gestão de todas as requisições de algum Front End e coordena a troca de informações entre outros microsserviços e APIs externas.

## Breve descrição do Projeto VA'Alugar:
Um AirBNB para aluguel de canoas havaianas.
O usuário pesquisa e reserva canoas disponíveis para locação nas praias, lagos, lagoas e rios. O usuário poderá fazer avaliação da canoa, postando uma nota e um texto.
O proprietário da canoa aumenta sua renda por meio da locação.
Nesta versão temos um serviço de previsão do tempo para os próximos 7 dias.

# Esquema do fluxo de informações entre Front End, Gateway e microsserviços / APIs externas.

## Arquitetura:
https://docs.google.com/presentation/d/e/2PACX-1vSfXcUSCZe_cCqlOBbNcvensXv6ysZqD_DIomZqSeXOKBunEWQ1YBIncFwzXu0T-Old4Ghmxlx8FQyX/pub?start=true&loop=false&delayms=60000

## Em quais portas os MS rodam:
- GATEWAY: 5001
- CANOAS: 5002
- RESERVAS: 5003
- AVALIACOES: 5004

## 1. Pesquisa por canoas:
1.1. Front End informa local e tipo de canoa desejados, ambos opcionais, fazendo uma chamada POST à rota /consultacanoas. Local é string, tipo de canoa é lista de strings.Veja na seção abaixo como fazer a requisição.

1.2. Gateway faz uma chamada do tipo GraphQL para o MS VAAlugar-MS-canoas.

1.3. VAAlugar-MS-canoas retorna, para o gateway, 0, 1 ou mais canoas.

1.4. Gateway retorna ao Front End a lista de canoas disponíveis.

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

Os parâmetros de chamada são opcionais, de modo que os seguintes exemplos são válidos:

{
    "local": "Pedra do Pontal"
}

{
    "tipos": ["OC6"]
}

{
} ==> retorna todas as canoas cadastradas no banco de dados.

## 2. Consulta da previsão do tempo
2.1. Front End informa a o município e o estado onde está a canoa escolhida, fazendo uma chamada à rota /consultaprevisão. Veja na seção abaixo como fazer a requisição.

2.2. Gateway faz uma consulta ao site do CPTEC/INPE, buscando por município. Exemplo: http://servicos.cptec.inpe.br/XML/listaCidades?city=rio de janeiro. O retorno é um dicionário de localidade, e o gateway deverá extrair o código do município, usando a informação do estado para tomar decisão.

2.3. Em seguida Gateway consulta o site do CPTEC/INPE para obter a previsão do tempo para os próximos 7 dias, usando o código da localidade, identificado no passo anterior.

2.4. Gateway retorna ao Front End a previsão do tempo para o próximos 7 dias.

### Como fazer a requisição POST à rota /consultaprevisao:
A chamada é um JSON com a seguinte estrutura:

{
  "estado": "string",
  "local": "string"
}

onde local é o município onde está a canoa escolhia, e estado é a unidade da federação onde está o município. Usar a sigla do Estado, como por exemplo, "RJ", "ES", "MG", "BA".


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
3.1. Front End informa a canoa escolhida, o usuario (representado por seu número de telefone) e um texto referente à data da locação, fazendo uma chamada POST à rota /confirmareserva. Veja na seção abaixo como fazer a requisição.

3.2. Gateway faz uma chamada POST ao microsserviço de gestão de reservas (VAAlugar-MS-reservas), na rota /reserva.

3.3. O VAAlugar-MS-reservas registra a reserva no banco de dados e retorna confirmação.

3.4. Gateway retorna ao Front End a confirmação da reserva.

### Como fazer a requisição POST à rota /confirmareserva:
A chamada é um JSON com a seguinte estrutura:

{
  "canoa": integer,
  "data": "string",
  "usuario": "string"
}

Por exemplo:

{
  "canoa": 13,
  "data": "31/10/2024",
  "usuario": "21994497881"
}

a resposta é do tipo:
{
  "canoa": 13,
  "data": "31/10/2024",
  "id_reserva": 18,
  "usuario": "21994497881"
}

## 4. Listagem de Reservas
4.1. Front End informa um usuario (representado por seu número de telefone, como uma string), fazendo uma chamada POST à rota /listarreservas. Veja na seção abaixo como fazer a requisição.

4.2. Gateway faz uma chamada GET ao microsserviço de gestão de reservas (VAAlugar-MS-reservas), na rota /reservas-usuario. O retorno será uma lista de todas as reservas já feitas pelo usuário.

4.3. Gateway faz uma chamada GraphQL ao microsserviço de gestão de avaliações (VAAlugar-MS-avaliacoes), na rota /graphql. O retorno será uma lista de todas as avaliações já feitas pelo usuário.

4.4. O VAAlugar-MS-reservas vai combinar estes 2 retornos, montando um JSON único contendo, para o usuário informado, todas as reservas já feitas e as respectivas avaliações, se realizadas.

4.5. Gateway retorna ao Front End o JSON com todas as reservas e avaliações relacionadas ao usuário informado.

### Como fazer a requisição POST à rota /listarreservas:
A chamada JSON tem a seguinte estrutura:
{
  "idusuario": "string"
}

Por exemplo,

{
  "idusuario": "21999991111"
}

retorna:

{
  "reservas": [
    {
      "canoa": 1,
      "comentario": null,
      "data": "13/07/24",
      "id-reserva": 20,
      "idpost": null,
      "nota": null,
      "usuario": "21999991111"
    },
    {
      "canoa": 6,
      "comentario": "Excelente! Lindo visual!",
      "data": "14/07/2024",
      "id-reserva": 21,
      "idpost": 22,
      "nota": 10,
      "usuario": "21999991111"
    }
  ]
}

Neste exemplo, a resposta lista 2 canoas, a canoa 1 e a canoa 6. Vemos que este usuário já postou alguma avaliação da canoa 6, com um comentário ("Excelente! Lindo visual!") e uma nota (10), e essa postagem tem um id no banco do serviço de avaliações, idpost = 22. Com relação à canoa 1, sabemos que este usuário não fez nenhuma postagem, porque os atributos comentário, idpost e nota retornam null. O front end poderá oferecer ao usuário tanto a postagem para a canoa 1, quanto a modificação da postagem da canoa 6, e para isso basta realizar o registro de avaliação, ver na seção 5 abaixo. O registro de avaliação não faz distinção, na chamada, entre uma modificação ou uma nova postagem, porém, em caso de modificação, internamente o sistema apenas atualiza a postagem, mantendo o mesmo idpost. Isso evita que um usuário faça várias postagens sobre a mesma reserva.




## 5. Registrar avaliação
5.1. Front End informa um usuario (representado por seu número de telefone, como uma string),  um número de reserva, um número de canoa, uma nota (número entre 0 e 10, mas atualmente não há qualquer tipo de validação do número) e um comentário sobre a experiência da locação da canoa, fazendo uma chamada POST à rota /avaliar. Veja na seção abaixo como fazer a requisição.

5.2. Gateway faz uma chamada POST ao microsserviço de gestão de avaliações (VAAlugar-MS-avaliacoes), na rota /criar.

5.3. VAAlugar-MS-avaliacoes registra as informações no banco de dados.

5.4. VAAlugar-MS-avaliacoes também conta o número de avaliações já registradas para a canoa informada e a médias dessas notas (essa funcionalidade já está implementada no microsserviço)

5.5. VAAlugar-MS-avaliacoes retorna a confirmação das informações persistidas no banco junto com a contagem e média de avaliações.

5.6. Gateway recebe estas informações e faz uma chamada PATCH para o microsserviço VAAlugar-MS-gerir_canoas_2, informando id_canoa, nova_média e nova_quantidade. O VAAlugar-MS-gerir_canoas_2 vai atualizar as informações da canoa. Gateway retorna as informações recebidas no passo 5.5 ao Front End.

### Como fazer a requisição POST à rota /avaliar:
A estrutura da chamada post é a seguinte:
{
  "comentario": "string",
  "id_canoa": 0,
  "id_reserva": 0,
  "nota": 0,
  "usuario": "string"
}

Então por exemplo:
{
  "comentario": "Foi uma excelente experiência! Quero remar outras vezes com esta canoa.",
  "id_canoa": 6,
  "id_reserva": 21,
  "nota": 10,
  "usuario": "21999991111"
}

retorna

{
  "detalhes": {
    "comentario": "Foi uma excelente experiência! Quero remar outras vezes com esta canoa.",
    "id_canoa": 6,
    "id_reserva": 21,
    "nota": "10.0000000000",
    "nova_media": 8.9,
    "nova_quantidade": 2
  },
  "mensagem": "Avaliação registrada com sucesso."
}


## Instalação
Considere as seguintes opções: instalar apenas este microsserviço, diretamente do IDE, como Visual Studio Code; ou instalar todos os microsserviços via Docker Compose.

### Para rodar este MS diretamente do IDE.
No Windows:
1. Faça o clone deste repositório para sua máquina.
2. Crie um ambiente virtual, com o comando "Python -m venv env", diretamente no terminal.
3. Em seguida ative o ambiente virtual, com o comando ".\env\Scripts\activate".
4. Instale as dependências necessárias com o comando "pip install -r requirements.txt".
5. Execute com o comando "flask run --host 0.0.0.0 --port 5002"
Para Mac ou Linux, a lógica é a mesma, mas faça as adaptações necessárias.

Observação: este gateway se comunica com os outros microsserviços, então é necessário que os outros estejam rodando para que você possa vê-lo funcionando. Para isso, siga as instruções descritas abaixo, para fazer a instalação usando o Docker Compose. Mesmo assim, sem usar o Docker Compose, você poderá acessar o serviço de previsão do tempo e ler o schemas de comunicação entre os microsserviços.

### Como executar através do Docker Compose
Para que os microsserviços interajam, é necessário que todos estejam rodando. A forma mais fácil de instalar e executar todos está descrita no link:
https://github.com/fabioFernandesBR/VAAlugar-Docker-Compose/blob/main/README.md

