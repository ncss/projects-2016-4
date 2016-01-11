from template.node import Node


class IncludeNode(Node):
    def __init__(self, reference):
        super().__init__()
        self.reference = reference

    def eval(self, context):
        from template.render import render
        read_file = render(self.reference, context)
        return read_file

    def pprint(self):
        return 'IncludeNode({})'.format(self.reference)
