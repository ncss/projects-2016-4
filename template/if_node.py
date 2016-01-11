from template.block_node import BlockNode
from template.exceptions import TemplateSyntaxException


class IfNode(BlockNode):
    def __init__(self, condition):
        super().__init__()
        self.conditions = [condition]
        self.children = [[]]
        self.has_else = False

    def add_elif(self, condition, fname):
        if self.has_else:
            raise TemplateSyntaxException('[' + fname + '] {% elif ... %} should not be placed after {% else %}')
        self.conditions.append(condition)
        self.children.append([])

    def add_else(self, fname):
        if self.has_else:
            raise TemplateSyntaxException('[' + fname + '] {% else %} should not be placed after another {% else %}')
        self.add_elif('True', fname)
        self.has_else = True

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
