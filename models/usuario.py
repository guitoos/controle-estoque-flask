# ============================================================
# usuario.py — Operações de usuários
# ============================================================
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from models.database import get_connection


def autenticar(login, senha):
    """Retorna o usuário (dict) se login e senha estiverem corretos; senão, None."""
    conn = get_connection()
    row = conn.execute(
        "SELECT id, nome, login, senha_hash, perfil FROM usuarios WHERE login = ?", (login,)
    ).fetchone()
    conn.close()
    if row and check_password_hash(row["senha_hash"], senha):
        return {"id": row["id"], "nome": row["nome"], "perfil": row["perfil"]}
    return None


def criar_usuario(nome, login, senha, perfil):
    """Cria um usuário. Retorna False se o login já existir."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, login, senha_hash, perfil) VALUES (?, ?, ?, ?)",
            (nome, login, generate_password_hash(senha), perfil),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def listar_usuarios():
    conn = get_connection()
    rows = conn.execute("SELECT id, nome, login, perfil FROM usuarios ORDER BY nome").fetchall()
    conn.close()
    return [dict(r) for r in rows]
