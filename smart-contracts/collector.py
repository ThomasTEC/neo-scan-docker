from boa.interop.Neo.App import RegisterAppCall
from boa.interop.Neo.Runtime import Log
from boa.interop.Neo.Iterator import Iterator

enumerate = RegisterAppCall('405e0495771565fb35d28c84949fbb1dbe629b81', 'operation', 'args')

def Main():
    token_iter = enumerate('tokensOf_test',)
    count = 0
    result = []
    while token_iter.next() and (count < 5):
        result.append(token_iter.Value)
        count += 1
    return result
