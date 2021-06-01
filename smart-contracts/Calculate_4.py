def Main(operation, args):

    a = args[0]
    b = args[1]

    print(operation)

    if operation == 'add':
        result = add(a, b)
        return result

    elif operation == 'sub':
        result = sub(a, b)
        return result

    elif operation == 'mul':
        result = mul(a, b)
        return result

    elif operation == 'div':
        result = div(a, b)
        return result

    else:
        return -1

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def div(x, y):
    return x / y
