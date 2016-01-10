from template.node import Node
from template import render


class IncludeNode(Node):
    def __init__(self, reference):
        super().__init__()
        self.reference = reference

    def eval(self, context):
        readFile = render(self.reference, context)
        return readFile

    def pprint(self):
        return 'IncludeNode({})'.format(self.reference)
