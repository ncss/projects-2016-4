from template.exceptions import TemplateSyntaxException

TOKEN_LITERAL = 0
TOKEN_EXPR = 1
TOKEN_ACTION = 2


# Convert source code to list of tokens
def tokenize(source):
    tokens = []
    token_start = 0
    token_end = 0
    cur = 0
    line = 1
    mode = TOKEN_LITERAL
    prev_char = ' '
    while True:
        char = source[cur]

        # Increment line counter every line
        if char == '\n':
            line += 1

        # Handle token split on {{ or {%
        if (char == '{' or char == '%') and prev_char == '{':
            token_end = cur - 1  # Set end of token
            tokens.append(source[token_start:token_end])  # Add previous token
            token_start = cur - 1  # Set start of new token
            mode = TOKEN_EXPR if char == '{' else TOKEN_ACTION  # Set to either expr or action mode

        # Handle token split on }} or %}
        if char == '}' and (prev_char == '}' or prev_char == '%'):
            # Make sure expr token is properly closed by %}
            if mode == TOKEN_EXPR and prev_char == '%':
                    raise TemplateSyntaxException('Line ' + str(line) + ': Expected }} got %}')

            # Make sure action token is properly closed by }}
            if mode == TOKEN_ACTION and prev_char == '}':
                    raise TemplateSyntaxException('Line ' + str(line) + ': Expected %} got }}')

            token_end = cur + 1  # Set end of token
            tokens.append(source[token_start:token_end])  # Add previous token
            token_start = cur + 1  # Set start of new token

        prev_char = char  # Update previous char
        cur += 1  # Increment cursor
        if cur == len(source):
            token_end = cur  # Set end of token
            tokens.append(source[token_start:token_end])  # Add previous token
            break
    return tokens


# random test stuff pls ignore
if __name__ == "__main__":
    test = """
        <html>
            {% include some_stuff.fun %}
        {{ someVar }}
            {% for x in y %}
                <a>{{ x.strip() }}</a>
            {% end for %}
            {% hi }}
        </html>
            """

    print(tokenize(test))
