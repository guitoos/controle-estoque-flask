# ============================================================
# produto.py — Operações de produtos
# ============================================================
from models.database import get_connection


def listar_produtos():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def buscar_produto(pid):
    conn = get_connection()
    row = conn.execute("SELECT * FROM produtos WHERE id = ?", (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None


def criar_produto(nome, categoria, quantidade, qtd_minima, preco):
    conn = get_connection()
    conn.execute(
        "INSERT INTO produtos (nome, categoria, quantidade, qtd_minima, preco) VALUES (?, ?, ?, ?, ?)",
        (nome, categoria, quantidade, qtd_minima, preco),
    )
    conn.commit()
    conn.close()


def atualizar_produto(pid, nome, categoria, quantidade, qtd_minima, preco):
    conn = get_connection()
    conn.execute(
        "UPDATE produtos SET nome = ?, categoria = ?, quantidade = ?, qtd_minima = ?, preco = ? WHERE id = ?",
        (nome, categoria, quantidade, qtd_minima, preco, pid),
    )
    conn.commit()
    conn.close()


def deletar_produto(pid):
    conn = get_connection()
    conn.execute("DELETE FROM produtos WHERE id = ?", (pid,))
    conn.commit()
    conn.close()


def produtos_abaixo_minimo():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM produtos WHERE quantidade < qtd_minima ORDER BY quantidade"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
