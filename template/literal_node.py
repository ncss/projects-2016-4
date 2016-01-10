from template.node import Node


class LiteralNode(Node):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def eval(self, context):
        return self.token

    def pprint(self):
        return 'LiteralNode({})'.format(self.token[:30])