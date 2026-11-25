import unittest
from app import run
class PesquisaCatalogo(unittest.TestCase):
    def test_pesquisa(self):
        data={"livro":"João","pesquisa":"graca","obras":[{"titulo":"Graça","editora":"Editora A","tipo":"Comentário","livros":["João"],"url":"https://example.org/a"},{"titulo":"Outro","editora":"Editora B","tipo":"Comentário","livros":["*"],"url":"https://example.org/b"}]}
        self.assertEqual([x["titulo"] for x in run(data)["obras"]],["Graça"])
        data["pesquisa"]="editora b"
        self.assertEqual(run(data)["quantidade"],1)
        data["pesquisa"]="ausente"
        self.assertEqual(run(data)["obras"],[])
