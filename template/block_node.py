from template.node import Node


class BlockNode(Node):

    def __init__(self):
        self.children = []

    def eval(self, context):
        text_list = []
        for child in self.children:
            text_list.append(eval(child, context))
        return ''.join(text_list)
