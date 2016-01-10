from template import expr_node
from template.block_node import BlockNode


class ForNode(BlockNode):
    def __init__(self, var, constraint):
        super().__init__()
        self.constraint = constraint
        self.var = var

    def eval(self, context):
        results = []
        for i in eval(self.constraint, {}, context):
            context[self.var] = i
            for child in self.children:
                results.append(child.eval(context))
        return ''.join(results)

    def pprint(self):
        return 'ForNode({} in {})'.format(self.var, self.constraint)
