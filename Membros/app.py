# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///igreja.db'
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Membro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    batizado = db.Column(db.Boolean, default=False)
    escolaridade = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Rota principal
@app.route('/')
def index():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    membros = Membro.query.all()
    return render_template('index.html', membros=membros)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        if usuario == 'admin' and senha == '12345':
            session['usuario_logado'] = True
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos!')
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

# Rota para adicionar novo membro
@app.route('/novo', methods=['GET', 'POST'])
def novo_membro():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        nome = request.form['nome']
        data_nasc = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
        telefone = request.form['telefone']
        batizado = True if request.form.get('batizado') else False
        escolaridade = request.form['escolaridade']
        
        novo_membro = Membro(
            nome_completo=nome,
            data_nascimento=data_nasc,
            telefone=telefone,
            batizado=batizado,
            escolaridade=escolaridade
        )
        
        db.session.add(novo_membro)
        db.session.commit()
        flash('Membro cadastrado com sucesso!')
        return redirect(url_for('index'))
        
    return render_template('novo_membro.html')

if __name__ == '__main__':
    app.run(debug=True)




