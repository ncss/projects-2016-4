from template.node import Node


class IfNode(Node):
    def __init__(self, condition):
        self.condition = condition
        self.children = []

    def eval(self, context):
        if eval(self.condition, {}, context):
            results = []
            for child in self.children:
                results.append(child.eval(context))
            return ''.join(results)
        else:
            return ''

if __name__ == '__main__':
    IfNode('user is not None')