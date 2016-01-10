from template.block_node import BlockNode


class IfNode(BlockNode):
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    def eval(self, context):
        if eval(self.condition, {}, context):
            return super().eval(context)
        else:
            return ''

    def pprint(self):
        return 'IfNode({})'.format(self.condition)

if __name__ == '__main__':
    IfNode('user is not None')
