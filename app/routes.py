from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.models import Cliente, Profissional, Servico, Agendamento
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('client_dashboard'))
    form = LoginForm()
    return render_template('home.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        cliente = Cliente(nome_completo=form.nome_completo.data, cpf=form.cpf.data, data_nascimento=form.data_nascimento.data,
                          sexo=form.sexo.data, telefone=form.telefone.data, email=form.email.data, usuario=form.usuario.data,
                          senha=hashed_password, frase_secreta=form.frase_secreta.data, dica_frase_secreta=form.dica_frase_secreta.data)
        db.session.add(cliente)
        db.session.commit()
        flash('Sua conta foi criada! Agora você pode fazer login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(usuario=form.usuario.data).first()
        if cliente and bcrypt.check_password_hash(cliente.senha, form.senha.data):
            login_user(cliente, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login não autorizado. Por favor verifique usuário e senha', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(email=form.email.data).first()
        if cliente:
            flash(f'A dica da frase secreta é: {cliente.dica_frase_secreta}', 'info')
            return redirect(url_for('reset_password'))
        else:
            flash('Nenhuma conta encontrada com esse email', 'warning')
    return render_template('forgot_password.html', title='Forgot Password', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(frase_secreta=form.frase_secreta.data).first()
        if cliente:
            hashed_password = bcrypt.generate_password_hash(form.nova_senha.data).decode('utf-8')
            cliente.senha = hashed_password
            db.session.commit()
            flash('Sua senha foi atualizada!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Frase secreta incorreta', 'danger')
    return render_template('reset_password.html', title='Reset Password', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    # Verificar se é admin
    if current_user.email != os.environ.get('ADMIN_EMAIL'):
        return redirect(url_for('home'))
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    servicos = Servico.query.all()
    agendamentos = Agendamento.query.all()
    return render_template('admin_dashboard.html', clientes=clientes, profissionais=profissionais, servicos=servicos, agendamentos=agendamentos)

@app.route('/client_dashboard')
@login_required
def client_dashboard():
    agendamentos = Agendamento.query.filter_by(cliente_cpf=current_user.cpf).all()
    return render_template('client_dashboard.html', agendamentos=agendamentos)
