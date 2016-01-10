from os.path import dirname, join

from template.tokenizer import tokenize
from template.tree import build_tree


# Returns the compiled node tree for a file
def compile_template(fname):
    with open(fname) as f:
        source = f.read()
    tokens = tokenize(source)
    root = build_tree(tokens)
    return root


# Renders a file to a string given a context (dictionary)
def render(fname, context):
    path = join(dirname(__file__), '../templates', fname)
    root = compile_template(path)
    rendered = root.eval(context)
    return rendered

if __name__ == '__main__':
    context = {}
    context['name'] = "Jason"
    context['x'] = 42

    messages = []
    messages.append({'id': 0, 'content': 'Hi this is a test messages...', 'read': True})
    messages.append({'id': 1, 'content': 'So is this one', 'read': True})
    messages.append({'id': 2, 'content': 'Lorem ipsum dolor sit amet', 'read': False})
    messages.append({'id': 3, 'content': 'TEMPLATES ARE COOL', 'read': True})
    context['messages'] = messages

    rendered = render('test/broken/unended_if.html', context)
    print(rendered)
