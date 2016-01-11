from template.block_node import BlockNode
from template.exceptions import TemplateSyntaxException
from template.exec_node import ExecNode
from template.expr_node import ExprNode
from template.for_node import ForNode
from template.if_node import IfNode
from template.include_node import IncludeNode
from template.literal_node import LiteralNode


def build_tree(token_list, fname):
    root_node = BlockNode()
    current_node = root_node

    for t in token_list:
        if t.startswith('{%'):
            t = t[2:-2].strip()
            if t.startswith('include '):
                current_node.add_child(IncludeNode(t[8:]))
            elif t.startswith('exec '):
                exec_node = ExecNode(t[5:].strip())
                current_node.add_child(exec_node)
            elif t.startswith('for '):
                if ' in ' not in t:
                    raise TemplateSyntaxException('[' + fname + '] For loop must include an \'in\'')
                for_node = ForNode(*(t[4:]).split(' in ', 1))
                current_node.add_child(for_node)
                current_node = for_node
            elif t.startswith('if '):
                if_node = IfNode(t[3:])
                current_node.add_child(if_node)
                current_node = if_node
            elif t.startswith('elif '):
                if not isinstance(current_node, IfNode):
                    raise TemplateSyntaxException('[' + fname + '] {% elif %} must follow an {% if ... %}')
                current_node.add_elif(t[5:], fname)
            elif t == 'else':
                if not isinstance(current_node, IfNode):
                    raise TemplateSyntaxException('[' + fname + '] {% else %} must follow an {% if ... %}')
                current_node.add_else(fname)
            elif t == 'end if':
                if not isinstance(current_node, IfNode):
                    raise TemplateSyntaxException('[' + fname + '] {% end if %} not expected')
                current_node = current_node.parent
            elif t == 'end for':
                if not isinstance(current_node, ForNode):
                    raise TemplateSyntaxException('[' + fname + '] {% end for %} not expected')
                current_node = current_node.parent
            else:
                raise TemplateSyntaxException('[' + fname + '] {% ' + t + ' %} is not a valid command')
        elif t.startswith('{{'):
            current_node.add_child(ExprNode(t[2:-2].strip()))
        else:
            current_node.add_child(LiteralNode(t))
    if current_node != root_node:
        raise TemplateSyntaxException('[' + fname + '] end expected, not found')
    return root_node

if __name__ == '__main__':
    source = ['<html>', '{{ someVar }}', '{% for x in y %}', '{% if x %}', '<p>', '{% elif someVar %}', 'hello world',
              '{% else %}', '<marquee>', '{{ x.strip() }}', '</p>', '{% end if %}', '{% end for %}', '</html>']

    tree = build_tree(source, "<test>")
    print(tree)
    print(tree.eval(dict(someVar=24, y=[' hi   ', '', 'cheese'])))

    source = ['<html>', '{{ someVar }}', '{% for x in y %}', '{% if x > 7 %}', '<p>',
              '{% elif x %}', 'hello world', '{% else %}', '<marquee>',
              '{{ x+5 }}', '</p>', '{% end if %}', '{% end for %}', '</html>']

    tree = build_tree(source, "<test>")
    print(tree)
    print(tree.eval(dict(someVar=24, y=range(10))))
