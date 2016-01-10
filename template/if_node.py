from template.block_node import BlockNode


class IfNode(BlockNode):
    def __init__(self, condition):
        super().__init__()
        self.conditions = [condition]
        self.children = [[]]

    def add_elif(self, condition):
        self.conditions.append(condition)
        self.children.append([])

    def add_else(self):
        self.add_elif('True')

    def add_child(self, child):
        self.children[-1].append(child)
        child.parent = self

    def eval(self, context):
        for children, condition in zip(self.children, self.conditions):
            if eval(condition, {}, context):
                text_list = []
                for child in children:
                    text_list.append(child.eval(context))
                return ''.join(text_list)
        return ''

    def pprint(self):
        return 'IfNode({})'.format(self.conditions[0])

    def __repr__(self):
        words = []
        first = True
        for children, condition in zip(self.children, self.conditions):
            if first:
                first = False
                words.append(self.pprint())
            else:
                words.append('ElifNode({})'.format(condition))
            for child in children:
                child_repr = repr(child)
                parts = child_repr.split('\n')
                for part in parts:
                    words.append('  '+part)
        return '\n'.join(words)


if __name__ == '__main__':
    IfNode('user is not None')
