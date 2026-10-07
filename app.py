# ============================================================
# app.py — Aplicação principal Flask
# Sistema de Controle de Estoque
# ============================================================

import os

from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.database import init_db
from models.usuario import autenticar, criar_usuario, listar_usuarios
from models.produto import (
    listar_produtos, buscar_produto, criar_produto,
    atualizar_produto, deletar_produto, produtos_abaixo_minimo
)
from models.movimentacao import registrar_movimentacao, listar_movimentacoes

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')


with app.app_context():
    init_db()


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faca login para continuar.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('perfil') != 'admin':
            flash('Acesso restrito ao Administrador.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        login_val = request.form.get('login', '').strip()
        senha_val = request.form.get('senha', '').strip()
        if not login_val or not senha_val:
            flash('Preencha login e senha.', 'warning')
            return render_template('login.html')
        usuario = autenticar(login_val, senha_val)
        if usuario:
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            session['perfil'] = usuario['perfil']
            flash(f'Bem-vindo(a), {usuario["nome"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login ou senha invalidos.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sessao encerrada.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    produtos = listar_produtos()
    alertas = produtos_abaixo_minimo()
    movs = listar_movimentacoes(limite=5)
    total_produtos = len(produtos)
    total_itens = sum(p['quantidade'] for p in produtos)
    return render_template('dashboard.html', produtos=produtos, alertas=alertas,
                           movimentacoes=movs, total_produtos=total_produtos,
                           total_itens=total_itens)


@app.route('/produtos')
@login_required
def produtos():
    lista = listar_produtos()
    alertas_ids = {p['id'] for p in produtos_abaixo_minimo()}
    return render_template('produtos.html', produtos=lista, alertas_ids=alertas_ids)


@app.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def produto_novo():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', '').strip()
        quantidade = request.form.get('quantidade', '').strip()
        qtd_minima = request.form.get('qtd_minima', '').strip()
        preco = request.form.get('preco', '').strip()
        erros = []
        if not nome:
            erros.append('Nome do produto e obrigatorio.')
        if not quantidade.isdigit():
            erros.append('Quantidade deve ser um numero inteiro.')
        if not qtd_minima.isdigit():
            erros.append('Quantidade minima deve ser um numero inteiro.')
        try:
            float(preco.replace(',', '.'))
        except (ValueError, AttributeError):
            erros.append('Preco deve ser um numero (ex: 10.50).')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('produto_form.html', produto=None, form=request.form)
        criar_produto(nome, categoria, int(quantidade), int(qtd_minima), float(preco.replace(',', '.')))
        flash(f'Produto "{nome}" cadastrado!', 'success')
        return redirect(url_for('produtos'))
    return render_template('produto_form.html', produto=None, form={})


@app.route('/produtos/editar/<int:pid>', methods=['GET', 'POST'])
@login_required
@admin_required
def produto_editar(pid):
    produto = buscar_produto(pid)
    if not produto:
        flash('Produto nao encontrado.', 'warning')
        return redirect(url_for('produtos'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', '').strip()
        quantidade = request.form.get('quantidade', '').strip()
        qtd_minima = request.form.get('qtd_minima', '').strip()
        preco = request.form.get('preco', '').strip()
        erros = []
        if not nome:
            erros.append('Nome e obrigatorio.')
        if not quantidade.isdigit():
            erros.append('Quantidade deve ser numero inteiro.')
        if not qtd_minima.isdigit():
            erros.append('Quantidade minima deve ser numero inteiro.')
        try:
            float(preco.replace(',', '.'))
        except (ValueError, AttributeError):
            erros.append('Preco invalido.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('produto_form.html', produto=produto, form=request.form)
        atualizar_produto(pid, nome, categoria, int(quantidade), int(qtd_minima), float(preco.replace(',', '.')))
        flash('Produto atualizado!', 'success')
        return redirect(url_for('produtos'))
    return render_template('produto_form.html', produto=produto, form=produto)


@app.route('/produtos/deletar/<int:pid>', methods=['POST'])
@login_required
@admin_required
def produto_deletar(pid):
    deletar_produto(pid)
    flash('Produto removido.', 'info')
    return redirect(url_for('produtos'))


@app.route('/movimentacao', methods=['GET', 'POST'])
@login_required
def movimentacao():
    produtos_lista = listar_produtos()
    if request.method == 'POST':
        produto_id = request.form.get('produto_id', '').strip()
        tipo = request.form.get('tipo', '').strip()
        quantidade = request.form.get('quantidade', '').strip()
        observacao = request.form.get('observacao', '').strip()
        erros = []
        if not produto_id.isdigit():
            erros.append('Selecione um produto valido.')
        if tipo not in ('entrada', 'saida'):
            erros.append('Tipo invalido.')
        if not quantidade.isdigit() or int(quantidade) <= 0:
            erros.append('Quantidade deve ser um numero inteiro positivo.')
        if not erros:
            produto = buscar_produto(int(produto_id))
            if tipo == 'saida' and produto['quantidade'] < int(quantidade):
                erros.append(f'Estoque insuficiente. Disponivel: {produto["quantidade"]} unidades.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('movimentacao.html', produtos=produtos_lista)
        registrar_movimentacao(int(produto_id), session['usuario_id'], tipo, int(quantidade), observacao)
        flash(f'{tipo.capitalize()} de {quantidade} unidade(s) registrada!', 'success')
        return redirect(url_for('movimentacao'))
    return render_template('movimentacao.html', produtos=produtos_lista)


@app.route('/historico')
@login_required
def historico():
    movs = listar_movimentacoes()
    return render_template('historico.html', movimentacoes=movs)


@app.route('/usuarios')
@login_required
@admin_required
def usuarios():
    lista = listar_usuarios()
    return render_template('usuarios.html', usuarios=lista)


@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def usuario_novo():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        login_val = request.form.get('login', '').strip()
        senha = request.form.get('senha', '').strip()
        perfil = request.form.get('perfil', 'comum').strip()
        erros = []
        if not nome:
            erros.append('Nome e obrigatorio.')
        if not login_val:
            erros.append('Login e obrigatorio.')
        if len(senha) < 4:
            erros.append('Senha deve ter pelo menos 4 caracteres.')
        if perfil not in ('admin', 'comum'):
            erros.append('Perfil invalido.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('usuario_form.html', form=request.form)
        ok = criar_usuario(nome, login_val, senha, perfil)
        if ok:
            flash(f'Usuario "{nome}" criado!', 'success')
            return redirect(url_for('usuarios'))
        else:
            flash('Login ja existe. Escolha outro.', 'danger')
    return render_template('usuario_form.html', form={})


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', port=5000)
