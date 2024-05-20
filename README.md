# Projeto PI Salão de Beleza

Este é o repositório do projeto PI Salão de Beleza. O objetivo deste projeto é desenvolver um sistema de gerenciamento para um salão de beleza.
Projeto desenvolvido para a disciplina de Projeto Integrador I da UNIVESP no Primeiro Semestre de 2024.

## Funcionalidades

- Cadastro de clientes
- CRUD de Profissionais
- CRUD de Serviços
- Agendamento de serviços
- Funcionalidades de login / recuperação de senha 

## Tecnologias utilizadas

- Python 3.11
- Flask
- PostgreSQL 16
- HTML
- CSS
- JavaScript

## Como executar o projeto

1. Clone este repositório em sua máquina local.
2. Crie um virtual enviroment: python -m venv venv
2. Instale as dependências do projeto: pip install -r ./requirements.txt
3. Certifique que possua o postgreSQL intalado localmente.
4. Crie um database chamado pi_salao_anc
5. Execute dentro da pasta do projeto: 
    flask db init 
    flask db migrate
    flask db upgrade
5. Execute: python run.py
6. Acesse via browser: http://127.0.0.1:5000

## Contribuição

O projeto está fechado e não serão aceitos PRs.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).