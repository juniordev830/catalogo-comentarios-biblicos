'Encontre edições e obras de referência por livro bíblico e tipo de material.'


from unicodedata import combining, normalize


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def textos(items):
    if not isinstance(items, list):
        raise ValueError("Use uma lista de textos.")
    return [texto(item) for item in items]


def chave(value):
    return "".join(c for c in normalize("NFKD", texto(value).casefold()) if not combining(c))


from urllib.parse import urlsplit


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    if not isinstance(data["obras"], list) or any(not isinstance(item, dict) for item in data["obras"]):
        raise ValueError("O campo obras deve ser uma lista de objetos.")
    livro = chave(data["livro"])
    tipo_informado = data.get("tipo")
    tipo = None if tipo_informado in (None, "") else chave(tipo_informado)
    obras = []
    for item in data["obras"]:
        livros = {chave(nome) for nome in textos(item["livros"])}
        if livro not in livros and "*" not in livros:
            continue
        if tipo is not None and tipo != chave(item["tipo"]):
            continue
        url = urlsplit(texto(item["url"]))
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError("Use a URL HTTPS pública da editora.")
        registro = {k: texto(item[k]) for k in ("titulo", "editora", "tipo", "url")}
        obras.append(registro)
    obras.sort(key=lambda item: chave(item["titulo"]))
    return {"livro": texto(data["livro"]), "obras": obras, "quantidade": len(obras)}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

