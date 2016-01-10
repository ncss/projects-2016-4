from template.node import Node


class BlockNode(Node):
    def eval(self, context):
        text_list = []
        for child in self.children:
            text_list.append(child.eval(context))
        return ''.join(text_list)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def pprint(self):
        return 'BlockNode()'

