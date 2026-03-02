from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

ARQUIVO = "usuarios.json"


def carregar_usuarios():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)


def salvar_usuarios(lista):
    with open(ARQUIVO, "w") as f:
        json.dump(lista, f, indent=4)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        idade = request.form["idade"]
        senha = request.form["senha"]

        if int(idade) < 18:
            flash("Usuário deve ser maior de idade.", "erro")
            return render_template("cadastro.html")

        usuarios = carregar_usuarios()

        for usuario in usuarios:
            if usuario["cpf"] == cpf:
                flash("CPF já cadastrado.", "erro")
                return render_template("cadastro.html")

        senha_hash = generate_password_hash(senha)

        novo_usuario = {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "idade": idade,
            "senha": senha_hash
        }

        usuarios.append(novo_usuario)
        salvar_usuarios(usuarios)

        flash("Cadastro realizado com sucesso!", "sucesso")
        return redirect("/listar")

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf = request.form["cpf"]
        senha_digitada = request.form["senha"]

        usuarios = carregar_usuarios()

        for usuario in usuarios:
            if usuario["cpf"] == cpf and check_password_hash(usuario["senha"], senha_digitada):
                flash("Login realizado com sucesso", "sucesso")
                return redirect("/listar")

        flash("CPF ou senha incorretos", "erro")

    return render_template("login.html")


@app.route("/listar")
def listar():
    usuarios = carregar_usuarios()
    total = len(usuarios)
    return render_template("listar.html", usuarios=usuarios, total=total)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)