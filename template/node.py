class Node:
    def __init__(self):
        pass

    def eval(self, context):
        raise NotImplementedError()

    def __str__(self):
        return 'Node()'

    def pprint(self):
        return 'Generic Node'
