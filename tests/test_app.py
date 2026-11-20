import app as modulo


def test_index():
    modulo.init_db()
    cliente = modulo.app.test_client()
    assert cliente.get("/").status_code == 200
