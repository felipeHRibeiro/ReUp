from flask import Flask, request, jsonify, render_template
import mysql.connector
from config import MYSQL_CONFIG

app = Flask(__name__)

def conectar_banco():
    return mysql.connector.connect(**MYSQL_CONFIG)

# Rota para a página HTML inicial
@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Erro ao renderizar template: {e}"

# CREATE - Inserir produto
@app.route("/create-produto", methods=["POST"])
def inserir_produto():
    dados = request.get_json() or request.form

    modelo = dados.get("modelo")
    tamanho = dados.get("tamanho")
    marca = dados.get("marca")

    if not modelo or not tamanho or not marca:
        return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "INSERT INTO produtos (modelo, tamanho, marca) VALUES (%s, %s, %s)"
        valores = (modelo, tamanho, marca)

        cursor.execute(sql, valores)
        conexao.commit()

        return jsonify({"mensagem": "Produto inserido com sucesso!"}), 201

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

# READ - Listar produtos
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM produtos"
        cursor.execute(sql)
        resultados = cursor.fetchall()

        return jsonify(resultados)

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

# SEARCH - Buscar produto pelo ID
@app.route("/search/produto/<int:id>", methods=["GET"])
def buscar_produto(id):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM produtos WHERE id = %s"
        cursor.execute(sql, (id,))
        resultado = cursor.fetchone()

        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"mensagem": "Produto não encontrado"}), 404

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

# DELETE - Remover produto pelo ID
@app.route("/delete/produto/<int:id>", methods=["DELETE"])
def remover_produto(id):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(sql, (id,))
        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Produto não encontrado"}), 404

        return jsonify({"mensagem": "Produto removido com sucesso!"}), 200

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
