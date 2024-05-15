from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(user_id)

class Cliente(db.Model, UserMixin):
    __tablename__ = 'tb_cadastro_cliente'
    cpf = db.Column(db.String(11), primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    frase_secreta = db.Column(db.String(100), nullable=False)
    dica_frase_secreta = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.cpf

class Profissional(db.Model):
    __tablename__ = 'tb_cadastro_profissional'
    cpf = db.Column(db.String(11), primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)

class Servico(db.Model):
    __tablename__ = 'tb_cadastro_servico'
    id = db.Column(db.Integer, primary_key=True)
    nome_servico = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    duracao_estimada = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Float, nullable=False)

class Agendamento(db.Model):
    __tablename__ = 'tb_agendamento'
    id = db.Column(db.Integer, primary_key=True)
    cliente_cpf = db.Column(db.String(11), db.ForeignKey('tb_cadastro_cliente.cpf'), nullable=False)
    telefone_cliente = db.Column(db.String(15), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('tb_cadastro_servico.id'), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    profissional_cpf = db.Column(db.String(11), db.ForeignKey('tb_cadastro_profissional.cpf'), nullable=False)
    data_agendamento = db.Column(db.Date, nullable=False)
    hora_agendamento = db.Column(db.Time, nullable=False)
    valor = db.Column(db.Float, nullable=False)
