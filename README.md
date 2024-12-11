# PyShellData

Este projeto consiste no desenvolvimento de uma API REST em Python que executa scripts Bash para processar dados de entrada em formato de texto.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- Python 3.11.1 ou superior
- Docker (se você for usar Docker)
- Bibliotecas python listadas no arquivo: requirements.txt


## Instalação

1. Instalar Dependências Python:
    Antes de executar o projeto, é necessário instalar as dependências. No terminal, execute o seguinte comando:

   ```bash
    pip install -r requirements.txt
   ```


   Se você não for usar Docker, crie um ambiente virtual:

   ```bash
      python -m venv .venv
      source .venv/bin/activate  # No Windows: .venv\Scripts\activate
      pip install -r requirements.txt
   ```



## Execução via Docker

2. Construir a Imagem Docker

    Na raiz do projeto, execute o comando para construir a imagem do Docker:


    ```bash
        docker build -t pyshelldata .
        docker run -p 5000:5000 pyshelldata
    ```
    A aplicação estará disponível em http://localhost:5000.



## Testes Unitários

Para executar os testes unitários, utilize o seguinte comando no diretório raiz do projeto:

```bash
python -m pytest src/tests/
```


## Endpoints da API

PUT /upload: Cadastrar um novo arquivo.
```bash
   form-data
   file:file_example
```

GET /files: Lista os arquivos.


GET /size/min?file=input
GET /size/max?file=input


GET /size/users?file=input: Lista usarios ordenados
GET /users?file=input&username=sihdtelu: Filtra por nome de usuario
GET /users?file=input&desc=true: Lista por ordem decrescente


GET /between-msgs?file=input&qtd_min=50&qtd_max=200: Lista por intervalo
