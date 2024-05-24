# Projeto Integrador I: Sistema de Gerenciamento para Salão de Beleza

Este projeto foi desenvolvido como parte da disciplina DRP04-Projeto Integrador em Computação I-Turma 003 na UNIVESP. O sistema de gerenciamento para salão de beleza permite a administração eficiente de clientes, profissionais e serviços, oferecendo uma interface amigável para agendamento e gestão.

## Funcionalidades

- **Cadastro de clientes**: Permite registrar novos clientes com informações detalhadas.
- **Gestão de Profissionais**: Adicionar, atualizar ou remover informações de profissionais.
- **Administração de Serviços**: Criar, modificar e excluir serviços oferecidos.
- **Agendamento de Serviços**: Interface para agendamento fácil de serviços pelos clientes.
- **Autenticação de Usuários**: Suporte para login seguro e recuperação de senha.

## Tecnologias Utilizadas

- **Backend**: Python 3.11 com Flask
- **Database**: PostgreSQL 16
- **Frontend**: HTML, CSS, JavaScript
- **Outras**: Flask-Migrate para migrações de banco de dados, Flask-Mail para envio de e-mails, bcrypt para hashing de senhas.
- **Controle de Versão**: Git e Github
- **Deployment**: Heroku

## Instalação e Configuração

1. **Clonar o Repositório**:
   ```bash
   git clone [URL do repositório]
   ```
2. **Configurar Ambiente Virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurações do Banco de Dados**:
   - Certifique-se de que o PostgreSQL está instalado e operacional.
   - Crie um banco de dados chamado `pi_salao_anc`.
   - Configure as variáveis de ambiente necessárias para conexão.
   
5. **Inicializar e Migrar Banco de Dados**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Executar a Aplicação**:
   ```bash
   python run.py
   ```

   Acessar via navegador: `http://127.0.0.1:5000`

## Contribuições

Este projeto faz parte de uma iniciativa acadêmica e está fechado para contribuições externas. No entanto, é uma excelente base para estudos e adaptações em projetos similares.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
