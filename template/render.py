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
    root = compile_template(fname)
    rendered = root.eval()
    return rendered
