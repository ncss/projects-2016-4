from template.node import Node


class ExecNode(Node):
    def __init__(self, statement):
        super().__init__()
        self.statement = statement

    def eval(self, context):
        exec(self.statement, {}, context)
        return ''

    def pprint(self):
        return 'ExecNode({})'.format(self.statement)
