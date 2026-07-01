from importar_carteira import normalizar_telefone, linha_para_contato


def test_normaliza_11_digitos_adiciona_55():
    assert normalizar_telefone("(47) 99104-1414") == "5547991041414"


def test_normaliza_ja_com_55_mantem():
    assert normalizar_telefone("5547991041414") == "5547991041414"


def test_linha_vira_contato_farmer():
    linha = {"nome": "João Silva", "telefone": "(47) 99104-1414",
             "email": "Joao@X.com", "assunto": "juridico"}
    c = linha_para_contato(linha)
    assert c["numero"] == "5547991041414"
    assert c["nome"] == "João Silva"
    assert c["area"] == "juridico"
    assert c["estagio"] == "pos_venda"
    assert c["dados"]["email"] == "joao@x.com"


def test_assunto_vazio_default_juridico():
    c = linha_para_contato({"nome": "X", "telefone": "47991041414", "email": "a@b.com", "assunto": ""})
    assert c["area"] == "juridico"
