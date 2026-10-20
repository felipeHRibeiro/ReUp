[README.md](https://github.com/user-attachments/files/33714662/README.md)
# ReUp

> Um "iFood" para bazares de roupas: o projeto reúne o cadastro e a consulta das peças vendidas em um bazar.

O ReUp nasceu como projeto de uma aula de introdução à computação em nuvem na AWS, com a ideia de colocar a aplicação para rodar na nuvem.

## Status

Protótipo em desenvolvimento. Hoje o projeto implementa o gerenciamento de produtos (cadastrar, listar, buscar e remover peças de roupa), que é a base do catálogo do bazar.

## Funcionalidades

- Cadastrar peças com modelo, tamanho e marca
- Listar todas as peças cadastradas
- Buscar uma peça pelo ID
- Remover uma peça pelo ID

O projeto tem duas interfaces para o mesmo banco de dados:

| Interface | Arquivo | Descrição |
|-----------|---------|-----------|
| Web | `app.py` + `templates/index.html` | API em Flask com uma página HTML para usar pelo navegador |
| Desktop | `Reup.py` | Janela feita com Tkinter para inserir e buscar peças |

## Tecnologias

- Python 3
- Flask (API e servidor web)
- MySQL (banco de dados) com `mysql-connector-python`
- HTML, CSS e JavaScript (página web)
- Tkinter (interface desktop)

## Estrutura do projeto

```
ReUp/
├── app.py              # API Flask
├── config.py           # Credenciais do banco (não deve ir para o GitHub)
├── Reup.py             # Interface desktop (Tkinter)
└── templates/
    └── index.html      # Página web
```

> O Flask procura as páginas HTML dentro da pasta `templates/`. Por isso o `index.html` precisa ficar nela.

## Como rodar

### 1. Pré-requisitos

- Python 3.8 ou superior
- Servidor MySQL em execução

### 2. Instalar as dependências

```bash
pip install flask mysql-connector-python
```

O Tkinter já vem junto com o Python na maioria das instalações.

### 3. Criar o banco de dados

Crie um banco e a tabela que o código espera:

```sql
CREATE DATABASE reup;
USE reup;

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(50) NOT NULL,
    tamanho VARCHAR(10) NOT NULL,
    marca VARCHAR(50) NOT NULL
);
```

### 4. Configurar a conexão

Crie o arquivo `config.py` na raiz do projeto com os dados do seu MySQL:

```python
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "seu_usuario",
    "password": "sua_senha",
    "database": "reup"
}
```

Não envie esse arquivo para o GitHub. Adicione `config.py` ao `.gitignore`.

### 5. Iniciar a aplicação web

```bash
python app.py
```

Abra no navegador: <http://localhost:5000>

## Endpoints da API

| Método | Rota | O que faz |
|--------|------|-----------|
| `GET` | `/` | Abre a página inicial |
| `POST` | `/create-produto` | Cadastra uma peça (JSON com `modelo`, `tamanho` e `marca`) |
| `GET` | `/produtos` | Lista todas as peças |
| `GET` | `/search/produto/<id>` | Busca uma peça pelo ID |
| `DELETE` | `/delete/produto/<id>` | Remove uma peça pelo ID |

Exemplo de cadastro:

```bash
curl -X POST http://localhost:5000/create-produto \
  -H "Content-Type: application/json" \
  -d '{"modelo": "Jaqueta", "tamanho": "M", "marca": "Levi'"'"'s"}'
```

## Nuvem (AWS)

O objetivo da aula era hospedar a aplicação na nuvem da AWS. Para isso, o banco MySQL e a aplicação Flask precisam estar acessíveis um ao outro, e as credenciais devem ficar fora do código (por exemplo, em variáveis de ambiente).

## Autor

Felipe Henrique Ribeiro
