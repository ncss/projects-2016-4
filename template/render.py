from os.path import dirname, join, basename

from os import listdir

from template.exceptions import TemplateSyntaxException
from template.tokenizer import tokenize
from template.tree import build_tree


# Returns the compiled node tree for a file
def compile_template(fname):
    with open(fname) as f:
        source = f.read()
    fname_base = basename(fname)

    tokens = tokenize(source, fname_base)
    root = build_tree(tokens, fname_base)
    return root


# Renders a file to a string given a context (dictionary)
def render(fname, context):
    path = join(dirname(__file__), '../templates', fname)
    root = compile_template(path)
    rendered = root.eval(context)
    return rendered

if __name__ == '__main__':
    # Use case examples for context
    context = {}
    context['name'] = "Jason"
    context['x'] = 42

    # Use case examples for context
    messages = []
    messages.append({'id': 0, 'content': 'Hi this is a test messages...', 'read': True})
    messages.append({'id': 1, 'content': 'So is <b>this</b> one', 'read': True})
    messages.append({'id': 2, 'content': 'Lorem ipsum dolor sit amet', 'read': False})
    messages.append({'id': 3, 'content': 'TEMPLATES ARE COOL', 'read': True})
    context['messages'] = messages

    # valid test cases
    valid_tests = ['template.html', 'exec_test.html']
    for test in valid_tests:
        rendered = render('test/' + test, context)
        print('Test: ' + test + '\n' + rendered)

    invalid_tests = listdir(join(dirname(__file__), '../templates/test/broken'))
    for test in invalid_tests:
        try:
            print('Test: ' + test)
            rendered = render('test/broken/' + test, context)
            print(rendered)
            print('TEST FAILED')
        except TemplateSyntaxException as e:
            print('Exception caught! ' + str(e) + '\n')
