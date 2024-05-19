from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ClienteForm, ProfissionalForm, ServicoForm, AgendamentoForm
from app.models import Cliente, Profissional, Servico, Agendamento
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os
from datetime import date

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        if current_user.email == 'salaoanc@gmail.com':
            return redirect(url_for('admin_dashboard'))
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
        cliente = Cliente(
            nome_completo=form.nome_completo.data, 
            cpf=form.cpf.data, 
            data_nascimento=form.data_nascimento.data,
            sexo=form.sexo.data, 
            telefone=form.telefone.data,
            email=form.email.data, 
            usuario=form.usuario.data,
            senha=hashed_password,
            frase_secreta=form.frase_secreta.data,
            dica_frase_secreta=form.dica_frase_secreta.data)
        db.session.add(cliente)
        db.session.commit()
        flash('Sua conta foi criada! Agora você pode fazer login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.email == 'salaoanc@gmail.com':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('client_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(usuario=form.usuario.data).first()
        if cliente and bcrypt.check_password_hash(cliente.senha, form.senha.data):
            login_user(cliente, remember=True)
            next_page = request.args.get('next')
            if cliente.email == 'salaoanc@gmail.com':
                return redirect(url_for('admin_dashboard'))
            return redirect(next_page) if next_page else redirect(url_for('client_dashboard'))
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
    if current_user.email != 'salaoanc@gmail.com':
        return redirect(url_for('home'))
    clientes = Cliente.query.all()
    profissionais = Profissional.query.all()
    servicos = Servico.query.all()
    agendamentos = Agendamento.query.all()
    return render_template('admin_dashboard.html', clientes=clientes, profissionais=profissionais, servicos=servicos, agendamentos=agendamentos)

@app.route('/client_dashboard')
@login_required
def client_dashboard():
    agendamentos_abertos = Agendamento.query.filter(
        Agendamento.cliente_cpf == current_user.cpf,
        Agendamento.data_agendamento >= date.today()
    ).all()
    agendamentos_concluidos = Agendamento.query.filter(
        Agendamento.cliente_cpf == current_user.cpf,
        Agendamento.data_agendamento < date.today()
    ).all()
    return render_template('client_dashboard.html', 
                           agendamentos_abertos=agendamentos_abertos, 
                           agendamentos_concluidos=agendamentos_concluidos)

@app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    form = AgendamentoForm()
    if form.validate_on_submit():
        agendamento = Agendamento(
            cliente_cpf=current_user.cpf,
            telefone_cliente=current_user.telefone,
            servico_id=form.servico.data,
            especialidade=Servico.query.get(form.servico.data).especialidade,
            profissional_cpf=form.profissional.data,
            data_agendamento=form.data_agendamento.data,
            hora_agendamento=form.hora_agendamento.data,
            valor=Servico.query.get(form.servico.data).valor
        )
        db.session.add(agendamento)
        db.session.commit()
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('client_dashboard'))
    return render_template('create_agendamento.html', title='Agendar Serviço', form=form)

# Renomeando endpoint para evitar conflito
@app.route('/editar_agendamento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    if agendamento.cliente_cpf != current_user.cpf:
        flash('Você não tem permissão para editar este agendamento.', 'danger')
        return redirect(url_for('client_dashboard'))
    form = AgendamentoForm()
    if form.validate_on_submit():
        agendamento.servico_id = form.servico.data
        agendamento.especialidade = Servico.query.get(form.servico.data).especialidade
        agendamento.profissional_cpf = form.profissional.data
        agendamento.data_agendamento = form.data_agendamento.data
        agendamento.hora_agendamento = form.hora_agendamento.data
        agendamento.valor = Servico.query.get(form.servico.data).valor
        db.session.commit()
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('client_dashboard'))
    elif request.method == 'GET':
        form.servico.data = agendamento.servico_id
        form.profissional.data = agendamento.profissional_cpf
        form.data_agendamento.data = agendamento.data_agendamento
        form.hora_agendamento.data = agendamento.hora_agendamento
    return render_template('edit_agendamento.html', title='Editar Agendamento', form=form)

# Renomeando endpoint para evitar conflito
@app.route('/excluir_agendamento/<int:id>', methods=['POST'])
@login_required
def excluir_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    if agendamento.cliente_cpf != current_user.cpf:
        flash('Você não tem permissão para deletar este agendamento.', 'danger')
        return redirect(url_for('client_dashboard'))
    db.session.delete(agendamento)
    db.session.commit()
    flash('Agendamento cancelado com sucesso!', 'success')
    return redirect(url_for('client_dashboard'))

@app.route('/edit_cliente/<cpf>', methods=['GET', 'POST'])
@login_required
def edit_cliente(cpf):
    cliente = Cliente.query.get_or_404(cpf)
    form = ClienteForm()
    if form.validate_on_submit():
        cliente.nome_completo = form.nome_completo.data
        cliente.data_nascimento = form.data_nascimento.data
        cliente.sexo = form.sexo.data
        cliente.telefone = form.telefone.data
        cliente.email = form.email.data
        cliente.usuario = form.usuario.data
        cliente.senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        cliente.frase_secreta = form.frase_secreta.data
        cliente.dica_frase_secreta = form.dica_frase_secreta.data
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    elif request.method == 'GET':
        form.cpf.data = cliente.cpf
        form.nome_completo.data = cliente.nome_completo
        form.data_nascimento.data = cliente.data_nascimento
        form.sexo.data = cliente.sexo
        form.telefone.data = cliente.telefone
        form.email.data = cliente.email
        form.usuario.data = cliente.usuario
        form.frase_secreta.data = cliente.frase_secreta
        form.dica_frase_secreta.data = cliente.dica_frase_secreta
    return render_template('edit_cliente.html', form=form, cliente=cliente)

@app.route('/delete_cliente/<cpf>', methods=['POST'])
@login_required
def delete_cliente(cpf):
    cliente = Cliente.query.get_or_404(cpf)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente deletado com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/profissionais/novo', methods=['GET', 'POST'])
@login_required
def create_profissional():
    form = ProfissionalForm()
    if form.validate_on_submit():
        if Profissional.query.get(form.cpf.data):
            flash('Profissional com esse CPF já existe.', 'danger')
        else:
            profissional = Profissional(
                cpf=form.cpf.data,
                nome_completo=form.nome_completo.data,
                telefone=form.telefone.data,
                email=form.email.data,
                especialidade=form.especialidade.data
            )
            db.session.add(profissional)
            db.session.commit()
            flash('Profissional criado com sucesso!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('create_profissional.html', title='Novo Profissional', form=form)

@app.route('/profissionais/<cpf>/editar', methods=['GET', 'POST'])
@login_required
def edit_profissional(cpf):
    profissional = Profissional.query.get_or_404(cpf)
    form = ProfissionalForm()
    if form.validate_on_submit():
        profissional.nome_completo = form.nome_completo.data
        profissional.telefone = form.telefone.data
        profissional.email = form.email.data
        profissional.especialidade = form.especialidade.data
        try:
            db.session.commit()
            flash('Profissional atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar profissional: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))
    elif request.method == 'GET':
        form.cpf.data = profissional.cpf
        form.nome_completo.data = profissional.nome_completo
        form.telefone.data = profissional.telefone
        form.email.data = profissional.email
        form.especialidade.data = profissional.especialidade
    return render_template('edit_profissional.html', title='Editar Profissional', form=form, profissional=profissional)

@app.route('/profissionais/<cpf>/excluir', methods=['POST'])
@login_required
def delete_profissional(cpf):
    profissional = Profissional.query.get_or_404(cpf)
    db.session.delete(profissional)
    db.session.commit()
    flash('Profissional excluído com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/servicos/novo', methods=['GET', 'POST'])
@login_required
def create_servico():
    form = ServicoForm()
    if form.validate_on_submit():
        if Servico.query.filter_by(nome_servico=form.nome_servico.data, especialidade=form.especialidade.data).first():
            flash('Serviço com esse nome e especialidade já existe.', 'danger')
        else:
            servico = Servico(
                nome_servico=form.nome_servico.data,
                especialidade=form.especialidade.data,
                duracao_estimada=form.duracao_estimada.data,
                valor=form.valor.data
            )
            db.session.add(servico)
            db.session.commit()
            flash('Serviço criado com sucesso!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('create_servico.html', title='Novo Serviço', form=form)

@app.route('/servicos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def edit_servico(id):
    servico = Servico.query.get_or_404(id)
    form = ServicoForm()
    if form.validate_on_submit():
        servico.nome_servico = form.nome_servico.data
        servico.especialidade = form.especialidade.data
        servico.duracao_estimada = form.duracao_estimada.data
        servico.valor = form.valor.data
        try:
            db.session.commit()
            flash('Serviço atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar serviço: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))
    elif request.method == 'GET':
        form.nome_servico.data = servico.nome_servico
        form.especialidade.data = servico.especialidade
        form.duracao_estimada.data = servico.duracao_estimada
        form.valor.data = servico.valor
    return render_template('edit_servico.html', title='Editar Serviço', form=form, servico=servico)

@app.route('/servicos/<int:id>/excluir', methods=['POST'])
@login_required
def delete_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    flash('Serviço excluído com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

# Renomeando endpoint para evitar conflito
@app.route('/agendamentos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def admin_edit_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    form = AgendamentoForm()
    if form.validate_on_submit():
        agendamento.cliente_cpf = form.cliente_cpf.data
        agendamento.telefone_cliente = form.telefone_cliente.data
        agendamento.servico_id = form.servico_id.data
        agendamento.especialidade = form.especialidade.data
        agendamento.profissional_cpf = form.profissional_cpf.data
        agendamento.data_agendamento = form.data_agendamento.data
        agendamento.hora_agendamento = form.hora_agendamento.data
        agendamento.valor = form.valor.data
        db.session.commit()
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    elif request.method == 'GET':
        form.cliente_cpf.data = agendamento.cliente_cpf
        form.telefone_cliente.data = agendamento.telefone_cliente
        form.servico_id.data = agendamento.servico_id
        form.especialidade.data = agendamento.especialidade
        form.profissional_cpf.data = agendamento.profissional_cpf
        form.data_agendamento.data = agendamento.data_agendamento
        form.hora_agendamento.data = agendamento.hora_agendamento
        form.valor.data = agendamento.valor
    return render_template('create_agendamento.html', title='Editar Agendamento', form=form)



# Renomeando endpoint para evitar conflito
@app.route('/agendamentos/<int:id>/excluir', methods=['POST'])
@login_required
def admin_delete_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()
    flash('Agendamento excluído com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))
