import ast

from .constants import OPTIONAL


base = """
class Example(TypedDict, total=False):
    foo: str
"""


def required_element(name, type):
    target = ast.Name(id=name)
    annotation = ast.Name(id=type)
    return ast.AnnAssign(target=target, annotation=annotation, simple=1)


def optional_element(name, type):
    target = ast.Name(id=name)
    annotation = ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id=type))
    return ast.AnnAssign(target=target, annotation=annotation, simple=1)


class GenerateTypedDict:
    def __init__(self, name):
        self.name = name
        tree = ast.parse(base)
        self.dict = tree.body[0]
        self.dict.body = []
        self.tree = tree
        tree.body[0].name = name
        self.tree = tree

    def dump(self):
        print(ast.dump(self.tree))

    def get_code(self):
        return ast.unparse(self.tree)

    def __add_element(self, element):
        self.dict.body.append(element)

    def add_optional_element(self, name, type):
        self.__add_element(optional_element(name, type))

    def add_required_element(self, name, type):
        self.__add_element(required_element(name, type))
