from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, TimeField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Cliente, Profissional, Servico, Agendamento

class RegistrationForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=10, max=11)])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino'), ('N', 'Não Informar')], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    frase_secreta = StringField('Frase Secreta', validators=[DataRequired(), Length(min=5, max=100)])
    dica_frase_secreta = StringField('Dica da Frase Secreta', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Cadastrar')

    def validate_cpf(self, cpf):
        cliente = Cliente.query.filter_by(cpf=cpf.data).first()
        if cliente:
            raise ValidationError('Esse CPF já está cadastrado.')

    def validate_email(self, email):
        cliente = Cliente.query.filter_by(email=email.data).first()
        if cliente:
            raise ValidationError('Esse email já está cadastrado.')

    def validate_usuario(self, usuario):
        cliente = Cliente.query.filter_by(usuario=usuario.data).first()
        if cliente:
            raise ValidationError('Esse usuário já está em uso.')

class LoginForm(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Ver Dica da Frase Secreta')

class ResetPasswordForm(FlaskForm):
    frase_secreta = StringField('Frase Secreta', validators=[DataRequired(), Length(min=5, max=100)])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired()])
    confirmacao_nova_senha = PasswordField('Confirmação da Nova Senha', validators=[DataRequired(), EqualTo('nova_senha')])
    submit = SubmitField('Resetar Senha')

class ClienteForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino'), ('N', 'Não Informar')], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    senha = PasswordField('Senha')
    frase_secreta = StringField('Frase Secreta', validators=[DataRequired(), Length(min=5, max=100)])
    dica_frase_secreta = StringField('Dica da Frase Secreta', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Salvar')

class ProfissionalForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    especialidade = StringField('Especialidade', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Salvar')

class ServicoForm(FlaskForm):
    nome_servico = StringField('Nome do Serviço', validators=[DataRequired(), Length(min=2, max=100)])
    especialidade = StringField('Especialidade', validators=[DataRequired(), Length(min=2, max=100)])
    duracao_estimada = StringField('Duração Estimada', validators=[DataRequired(), Length(min=2, max=20)])
    valor = FloatField('Valor', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class AgendamentoForm(FlaskForm):
    data_agendamento = DateField('Data', validators=[DataRequired()])
    hora_agendamento = TimeField('Hora', validators=[DataRequired()])
    profissional = SelectField('Profissional', coerce=str, validators=[DataRequired()])
    servico = SelectField('Serviço', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Agendar')

    def __init__(self):
        super().__init__()
        self.profissional.choices = [(p.cpf, p.nome_completo) for p in Profissional.query.all()]
        self.servico.choices = [(s.id, s.nome_servico) for s in Servico.query.all()]