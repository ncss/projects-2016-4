from template.block_node import BlockNode
from template.exceptions import TemplateSyntaxException
from template.expr_node import ExprNode
from template.for_node import ForNode
from template.if_node import IfNode
from template.include_node import IncludeNode
from template.literal_node import LiteralNode


def build_tree(token_list):
    root_node = BlockNode()
    current_node = root_node

    for t in token_list:
        if t.startswith('{%'):
            t = t[2:-2].strip()
            if t.startswith('include '):
                current_node.add_child(IncludeNode(t[8:]))
            elif t.startswith('for '):
                if ' in ' not in t:
                    raise TemplateSyntaxException('For loop must include an \'in\'')
                for_node = ForNode(*(t[4:]).split(' in ', 1))
                current_node.add_child(for_node)
                current_node = for_node
            elif t.startswith('if '):
                if_node = IfNode(t[3:])
                current_node.add_child(if_node)
                current_node = if_node
            elif t.startswith('elif '):
                current_node.add_elif(t[5:])
            elif t == 'else':
                current_node.add_else();
            elif t == 'end if':
                current_node = current_node.parent
            elif t == 'end for':
                current_node = current_node.parent
        elif t.startswith('{{'):
            current_node.add_child(ExprNode(t[2:-2].strip()))
        else:
            current_node.add_child(LiteralNode(t))
    return root_node

if __name__ == '__main__':
    source = ['<html>', '{{ someVar }}', '{% for x in y %}', '{% if x %}', '<p>', '{% elif someVar %}', 'hello world', '{% else %}', '<marquee>'
              '{{ x.strip() }}', '</p>', '{% end if %}', '{% end for %}', '</html>']

    tree = build_tree(source)
    print(tree)
    print(tree.eval(dict(someVar=24, y=[' hi   ', '', 'cheese'])))

    source = ['<html>', '{{ someVar }}', '{% for x in y %}', '{% if x > 7 %}', '<p>',
              '{% elif x %}', 'hello world', '{% else %}', '<marquee>',
              '{{ x+5 }}', '</p>', '{% end if %}', '{% end for %}', '</html>']

    tree = build_tree(source)
    print(tree)
    print(tree.eval(dict(someVar=24, y=range(10))))
