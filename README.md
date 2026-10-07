# Controle de Estoque

Aplicação web em Flask para controle de estoque, com autenticação, perfis de acesso, cadastro de produtos, registro de entradas e saídas e alertas de estoque mínimo.

Projeto desenvolvido na disciplina Development with Python, do curso de Análise e Desenvolvimento de Sistemas da UniFECAF.

## Funcionalidades

- Login com senha armazenada em hash (Werkzeug)
- Perfis Administrador e Comum, com rotas restritas por perfil
- CRUD completo de produtos
- Registro de entradas e saídas, com bloqueio de saída acima do saldo
- Alerta de produtos abaixo da quantidade mínima
- Histórico de movimentações com usuário, data e observação
- Painel com totais e últimas movimentações

## Tecnologias

- Python 3.10+
- Flask
- SQLite
- Bootstrap 5

## Como executar

```bash
git clone https://github.com/guitoos/controle-estoque-flask.git
cd controle-estoque-flask
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse `http://localhost:5000`. O banco `estoque.db` é criado automaticamente no primeiro acesso.

Usuário inicial: `admin`. A senha vem da variável de ambiente `ADMIN_PASSWORD` (padrão `admin123`, apenas para testes locais).

## Variáveis de ambiente

| Variável | Uso | Padrão |
| --- | --- | --- |
| `SECRET_KEY` | Chave de sessão do Flask | valor de desenvolvimento |
| `ADMIN_PASSWORD` | Senha do administrador criado no primeiro acesso | `admin123` |
| `ESTOQUE_DB` | Caminho do banco SQLite | `estoque.db` |
| `FLASK_DEBUG` | `1` ativa o modo debug | desativado |

## Estrutura

```
controle-estoque-flask/
├── app.py                # Rotas e regras da aplicação
├── requirements.txt
├── models/
│   ├── database.py       # Conexão e criação das tabelas
│   ├── usuario.py        # Autenticação e usuários
│   ├── produto.py        # Operações de produtos
│   └── movimentacao.py   # Entradas, saídas e histórico
└── templates/            # Páginas HTML (Jinja2 + Bootstrap)
```

## Autor

Guilherme Oliveira · [LinkedIn](https://www.linkedin.com/in/guilhermeoss)
