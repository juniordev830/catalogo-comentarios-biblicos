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


def url_editora(value):
    endereco = texto(value)
    try:
        url = urlsplit(endereco)
        url.port  # A leitura da porta valida o formato e o intervalo.
    except ValueError:
        raise ValueError("Use a URL HTTPS pública da editora.") from None
    if (url.scheme != "https" or not url.hostname or url.username is not None
            or url.password is not None or any(char.isspace() for char in endereco)):
        raise ValueError("Use a URL HTTPS pública da editora.")
    return endereco


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
        registro = {k: texto(item[k]) for k in ("titulo", "editora", "tipo")}
        registro["url"] = url_editora(item["url"])
        obras.append(registro)
    obras.sort(key=lambda item: chave(item["titulo"]))
    return {"livro": texto(data["livro"]), "obras": obras, "quantidade": len(obras)}


import argparse
from contextlib import nullcontext
import sys
from relatorio_csv import escrever_csv
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


MAX_JSON_BYTES = 1_000_000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--csv", action="store_true", help="Exportar o catálogo de obras por livro em CSV")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open("rb")
        with entrada as source:
            raw = source.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError("JSON excede o limite de 1 MB.")
        data = json.loads(
            raw.decode("utf-8-sig"),
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, UnicodeError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.csv:
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

