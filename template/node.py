class Node(object):
    def __init__(self):
        self.parent = None
        self.children = []

    def eval(self, context):
        raise NotImplementedError()

    def pprint(self):
        return 'GenericNode()'

    def __repr__(self):
        words = [self.pprint()]
        for child in self.children:
            child_repr = repr(child)
            parts = child_repr.split('\n')  # so that extra spaces are added for multilevel children
            for part in parts:
                words.append('  '+part)  # add two spaces to show child relationship
        return '\n'.join(words)
