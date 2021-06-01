from boa.interop.Neo.Storage import GetContext, Get, Put, Delete, Find

DECIMALS = '0'
STORAGE_KEY = b'storage_key'

def Main(operation, args):
    ctx = GetContext()

    if operation == "store":
        Put(ctx, STORAGE_KEY, 1)  # store value
        return True

    elif operation == "getvalue":
        return Get(ctx, STORAGE_KEY)

    elif operation == "decimals":
        return DECIMALS

    elif operation == "raise":
        new_val = Get(ctx, STORAGE_KEY)
        new_val += 1
        Put(ctx, STORAGE_KEY, new_val)
        return True

    else:
        print('invalid operation')
        return False
