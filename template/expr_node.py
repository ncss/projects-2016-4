from template.node import Node


class ExprNode(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def eval(self, context):
        return str(eval(self.expression, context))

    def pprint(self):
        return 'ExprNode({})'.format(self.expression)
