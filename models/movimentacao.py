# ============================================================
# movimentacao.py — Registro de entradas e saídas de estoque
# ============================================================
from models.database import get_connection


def registrar_movimentacao(produto_id, usuario_id, tipo, quantidade, observacao=""):
    """Registra a movimentação e atualiza o saldo do produto na mesma transação."""
    delta = quantidade if tipo == "entrada" else -quantidade
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (delta, produto_id)
        )
        conn.execute(
            "INSERT INTO movimentacoes (produto_id, usuario_id, tipo, quantidade, observacao) "
            "VALUES (?, ?, ?, ?, ?)",
            (produto_id, usuario_id, tipo, quantidade, observacao),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def listar_movimentacoes(limite=None):
    sql = (
        "SELECT m.id, m.tipo, m.quantidade, m.observacao, m.data_hora, "
        "p.nome AS produto, u.nome AS usuario "
        "FROM movimentacoes m "
        "JOIN produtos p ON p.id = m.produto_id "
        "JOIN usuarios u ON u.id = m.usuario_id "
        "ORDER BY m.data_hora DESC, m.id DESC"
    )
    params = ()
    if limite:
        sql += " LIMIT ?"
        params = (limite,)
    conn = get_connection()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]
