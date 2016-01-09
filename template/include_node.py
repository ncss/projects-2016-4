from template.node import Node
from template import render


class IncludeNode(Node):
    def __init__(self, reference):
        self.reference = reference

    def eval(self, context):
        readFile = render(self.reference, context)
        return readFile