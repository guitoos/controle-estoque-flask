# ============================================================
# database.py — Conexão e inicialização do banco SQLite
# ============================================================
import os
import sqlite3

from werkzeug.security import generate_password_hash

DB_PATH = os.environ.get(
    "ESTOQUE_DB",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "estoque.db"),
)


def get_connection():
    """Abre uma conexão com o banco, retornando linhas como dicionários."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Cria as tabelas (se não existirem) e o usuário administrador inicial."""
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            perfil TEXT NOT NULL CHECK (perfil IN ('admin', 'comum'))
        );

        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
            qtd_minima INTEGER NOT NULL DEFAULT 0 CHECK (qtd_minima >= 0),
            preco REAL NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL REFERENCES produtos(id) ON DELETE CASCADE,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
            tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
            quantidade INTEGER NOT NULL CHECK (quantidade > 0),
            observacao TEXT,
            data_hora TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        """
    )

    existe_admin = cur.execute("SELECT 1 FROM usuarios WHERE perfil = 'admin' LIMIT 1").fetchone()
    if not existe_admin:
        senha_inicial = os.environ.get("ADMIN_PASSWORD", "admin123")
        cur.execute(
            "INSERT INTO usuarios (nome, login, senha_hash, perfil) VALUES (?, ?, ?, ?)",
            ("Administrador", "admin", generate_password_hash(senha_inicial), "admin"),
        )

    conn.commit()
    conn.close()
