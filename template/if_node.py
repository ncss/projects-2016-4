from template.block_node import BlockNode


class IfNode(BlockNode):
    def __init__(self, condition):
        self.condition = condition
        self.children = []

    def eval(self, context):
        if eval(self.condition, {}, context):
            return super(self).eval(context)
        else:
            return ''

if __name__ == '__main__':
    IfNode('user is not None')
