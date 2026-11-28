# Catálogo de comentários bíblicos

**Navegação** · [Rodar](#rodar) · [Uso](#uso) · [Fontes e exemplos](#fontes-e-exemplos) · [Código e estudo](docs/ENGENHARIA_REVERSA.md)

Encontre edições e obras de referência por livro bíblico e tipo de material.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Mantenha a cobertura editorial no JSON e indique o livro procurado. Use `*` em uma obra que cobre todos os livros do seu escopo, informe os livros individualmente para coberturas parciais e use URLs das editoras.

## Fontes e exemplos

Os exemplos incluem referências bíblicas, perguntas e anotações de demonstração. Consulte o texto e o contexto em uma [tradução publicada pela Sociedade Bíblica do Brasil](https://www.sbb.org.br/traducoes-da-biblia). Para aprofundar, o catálogo da [Nova Bíblia de Estudo Almeida](https://www.sbb.org.br/nova-almeida/biblias-de-estudo/biblia-de-estudo-almeida) e o do [Comentário Bíblico Pentecostal do Novo Testamento, CPAD](https://www.cpad.com.br/comentario-biblico-pentecostal-novo-testamento-/p) ajudam a identificar edições. Registre as páginas verificadas na sua própria consulta.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar o catálogo de obras por livro. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```

## Código e roteiro de estudo

Como indexar uma obra que cobre vários livros sem repeti-la nos resultados? O [guia de engenharia reversa](docs/ENGENHARIA_REVERSA.md) reúne o mapa dos módulos e uma pergunta técnica baseada no projeto.

Mantido por [João Junior](https://github.com/juniordev830).
