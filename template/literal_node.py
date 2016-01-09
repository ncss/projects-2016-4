from template.node import Node


class LiteralNode(Node):
    def __init__(self, token):
        self.token = token

    def eval(self, context):
        return self.token
