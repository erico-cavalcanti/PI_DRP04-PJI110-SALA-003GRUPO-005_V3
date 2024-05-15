from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Cliente

class RegistrationForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
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
