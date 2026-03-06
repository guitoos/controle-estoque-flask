# Sistema de Controle de Estoque
**Aluno:** Guilherme Oliveira Silva Santos | **RA:** 143422
**Disciplina:** Development with Python | **UniFECAF**

## Como Executar

1. Instale as dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Execute a aplicacao:
   ```
   python app.py
   ```

3. Acesse no navegador: `http://localhost:5000`

## Login Padrao
- **Login:** admin
- **Senha:** admin123

## Estrutura do Projeto
```
estoque_app/
├── app.py              # Aplicacao principal Flask
├── requirements.txt    # Dependencias Python
├── estoque.db          # Banco de dados SQLite (criado automaticamente)
├── models/
│   ├── database.py     # Conexao e inicializacao do banco
│   ├── usuario.py      # Operacoes de usuarios
│   ├── produto.py      # Operacoes de produtos
│   └── movimentacao.py # Registro de movimentacoes
└── templates/
    ├── base.html        # Layout base com menu lateral
    ├── login.html       # Tela de login
    ├── dashboard.html   # Painel principal
    ├── produtos.html    # Listagem de produtos
    ├── produto_form.html # Formulario cadastro/edicao
    ├── movimentacao.html # Registro entrada/saida
    ├── historico.html   # Historico de movimentacoes
    ├── usuarios.html    # Listagem de usuarios
    └── usuario_form.html # Formulario novo usuario

## Funcionalidades
- Login e sessao de usuario
- Perfis: Administrador e Comum
- Senha criptografada com hash (werkzeug)
- CRUD completo de produtos
- Registro de entrada e saida de estoque
- Alertas de estoque abaixo do minimo
- Historico de movimentacoes
- Validacoes de campos numericos
