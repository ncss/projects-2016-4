from template.node import Node


class ExprNode(Node):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, context):
        return eval(self.expression, context)