# Calculate using  parsing

# OPERATORS
T_ADD = '+'
T_SUB = '-'
T_MUL = '*'
T_DIV = '/'

T_POW = '^'
T_MOD = '%'

T_LPA = '('
T_RPA = ')'

# Order of operations must be applied in this list
OPERATORS = [T_POW, T_MOD, T_MUL, T_DIV, T_ADD, T_SUB]


def simplify(a, b, op):
    if op == T_ADD:
        return a + b
    if op == T_SUB:
        return a - b
    if op == T_MUL:
        return a * b
    if op == T_DIV:
        return a / b
    if op == T_POW:
        return a ** b
    if op == T_MOD:
        return a % b


def tokenize(c):
    grouping = 0
    current_groups = 0
    data = ['']
    curr_negative = False

    def group():
        if grouping == 1:
            data.append(s[i])
        elif grouping == -1:
            data[-1] += s[i]
            data.append('')
        elif grouping == 0:
            data[-1] += s[i]

    s = ''
    for i in c.split(' '):
        s += i

    if s[0] == T_LPA and s[-1] == T_RPA:
        s = s[1:-1]

    """
    group = 1: start a new token
    group = -1: end current token (adds itself before ending it)
    group = 0: continue current token

    sub-expression in parentheses is counted as one token
    """

    # tokenize by parentheses
    for i in range(len(s)):
        if s[i] == T_SUB or i == 0:
            if s[i] == T_SUB and i == 0:  # if current token and next token make to be a negative
                grouping = 1  # continue
                group()
                curr_negative = True
                continue
            elif s[i] == T_SUB and (s[i - 1] in OPERATORS or s[i - 1] == T_LPA or s[i - 1] == T_RPA):
                grouping = 1  # continue
                group()
                curr_negative = True
                continue
            else:
                pass
        if current_groups == 0:
            if s[i] == T_LPA:  # left p states new token
                grouping = 1
                current_groups += 1
            elif s[i] == T_RPA:  # right p will end current token
                grouping = -1
                current_groups -= 1
            elif s[i] in OPERATORS:  # if current char is an operator
                grouping = 1
            elif i > 0:  # if previous token is an operator
                if s[i - 1] in OPERATORS:
                    if curr_negative:
                        grouping = 0
                        curr_negative = False
                    else:
                        grouping = 1
                else:
                    grouping = 0  # continue token
            else:
                grouping = 0  # continue token
        else:
            if s[i] == T_RPA:  # right p will end current token
                if current_groups == 0:
                    grouping = -1
                current_groups -= 1
            elif s[i] == T_LPA:
                current_groups += 1
                grouping = 0
            else:
                grouping = 0

        group()

    clean_data = []
    for i in data:
        if i != '':
            clean_data.append(i)

    return clean_data


def solve(t):
    sub_exp = []
    tokens = t.copy()

    # solve each expression in parentheses using recursion
    for i in range(len(tokens)):
        if T_LPA in tokens[i] and T_RPA in tokens[i]:
            sub_exp.append(True)
        else:
            sub_exp.append(False)

    for i in range(len(tokens)):
        if sub_exp[i]:
            tokens[i] = solve(tokenize(tokens[i]))

    if len(tokens) == 1:
        return tokens[0]

    cycles = 0
    cycle_limit = 100
    while len(tokens) > 1:
        if cycles > cycle_limit:
            raise ValueError("Please use * as a multiplication sign when needed")
        for op in OPERATORS:
            for i in range(len(tokens)):
                # make sure there are still expressions to evaluate
                try:
                    tok = tokens[i]
                except IndexError:
                    break

                if tok == op:
                    tok_a = float(tokens[i - 1])
                    tok_b = float(tokens[i + 1])

                    # remove the mini-expression and replace with the result token
                    tokens.pop(i + 1)
                    tokens.pop(i)

                    tokens[i - 1] = simplify(tok_a, tok_b, op)

        cycles += 1

    if int(tokens[0]) == float(tokens[0]):
        return int(tokens[0])
    else:
        return float(tokens[0])

