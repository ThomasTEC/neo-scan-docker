from boa.builtins import concat, breakpoint
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.App import RegisterAppCall
from boa.interop.Neo.Blockchain import GetContract
from boa.interop.Neo.Iterator import Iterator, IterNext, IterKey, IterValue
from boa.interop.Neo.Runtime import CheckWitness, GetTrigger, Notify, Serialize, Deserialize, Log
from boa.interop.Neo.Storage import GetContext, Get, Put, Delete, Find
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.System.ExecutionEngine import GetCallingScriptHash

# This is the script hash of the address for the owner of the contract
# This can be found in ``neo-python`` with the wallet open,
# use ``wallet`` command
TOKEN_CONTRACT_OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
TOKEN_NAME = 'FIRST NFT'
TOKEN_SYMBOL = 'NFT'
TOKEN_DECIMALS = 0
TOKEN_CIRC_KEY = b'in_circulation'

# Smart Contract Event Notifications
OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount', 'token_id')
OnError = RegisterAction('error', 'message')

# common errors
ARG_ERROR = 'incorrect arg length'
INVALID_ADDRESS_ERROR = 'invalid address'
PERMISSION_ERROR = 'incorrect permission'
TOKEN_DNE_ERROR = 'token does not exist'

def Main(operation, args):
    trigger = GetTrigger()
    if trigger == Verification():
        assert CheckWitness(TOKEN_CONTRACT_OWNER), PERMISSION_ERROR
        return True

    elif trigger == Application():

        ctx = GetContext()

        if operation == 'name': #bekomme leserliches Ergebnis
            return TOKEN_NAME

        elif operation == 'symbol': #bekomme leserliches Ergebnis
            return TOKEN_SYMBOL

        elif operation == 'supportedStandards': #bekomme leserliches Ergebnis
            return Serialize(['NEP-10','NEP-11'])

        elif operation == 'totalSupply': #bekomme leserliches Ergebnis
            return Get(ctx, TOKEN_CIRC_KEY)

        elif operation == 'decimals': #0 wird nicht ausgegeben
            return TOKEN_DECIMALS

        elif operation == 'ownerOf': #bekomme leserliches Ergebnis
            assert len(args) == 1, ARG_ERROR
            token = get_token(ctx, args[0])
            return token['owner']

        elif operation == 'balanceOf': #bekomme leserliches Ergebnis
            assert len(args) == 1, ARG_ERROR
            assert len(args[0]) == 20, INVALID_ADDRESS_ERROR
            token_iter = Find(ctx, args[0])
            count = 0
            while token_iter.next():
                count += 1
            return count

        elif operation == 'tokensOf': #gehen nicht mit invoke
            assert len(args) == 1, ARG_ERROR
            assert len(args[0]) == 20, INVALID_ADDRESS_ERROR
            result_iter = Find(ctx, args[0])
            items = []
            while result_iter.IterNext():
                items.append(result_iter.Value)
            print(items)
            return items

        elif operation == 'properties': #bekomme leserliches Ergebnis
            assert len(args) == 1, ARG_ERROR
            token = get_token(ctx, args[0])
            return token['properties']

        elif operation == 'transfer':
            assert len(args) == 2, ARG_ERROR
            t_to = args[0]
            t_id = args[1]

            assert len(t_to) == 20, INVALID_ADDRESS_ERROR

            token = get_token(ctx, args[1])
            t_owner = token['owner']

            assert len(t_owner) == 20, INVALID_ADDRESS_ERROR

            assert CheckWitness(t_owner), PERMISSION_ERROR

            token['owner'] = t_to;
            Delete(ctx, concat(t_owner, t_id))
            Put(ctx, concat(token['owner'], t_id), t_id)

            OnTransfer(t_owner, t_to, 1, t_id)
            return save_token(ctx, t_id, token)

        elif operation == 'mintToken':
            assert CheckWitness(TOKEN_CONTRACT_OWNER), PERMISSION_ERROR
            assert len(args) == 4, ARG_ERROR

            t_circ = Get(ctx, TOKEN_CIRC_KEY)
            t_circ += 1

            assert len(args[0]) == 20, INVALID_ADDRESS_ERROR
            assert args[1], 'missing token id'
            assert args[2], 'missing properties'
            assert args[3], 'missing owner'

            t_id = args[1]
            t = Get(ctx, concat('token/', t_id))
            assert not t, 'token already exists'

            token = {}

            token['id'] = t_id
            token['properties'] = args[2]
            token['owner'] = args[3]

            Put(ctx, concat(token['owner'], t_id), t_id)
            Put(ctx, TOKEN_CIRC_KEY, t_circ)  # update total supply

            OnTransfer('', token['owner'], 1, t_id)
            return save_token(ctx, t_id, token)

    AssertionError('unknown operation')

def get_token(ctx, token_id):
    data = Get(ctx, concat('token/', token_id))
    assert len(data) > 0, TOKEN_DNE_ERROR
    obj = Deserialize(data)
    return obj

def save_token(ctx, token_id, token):
    data = Serialize(token)
    Put(ctx, concat('token/', token_id), data)
    return True

def AssertionError(msg):
    OnError(msg) # for neo-cli ApplicationLog
    raise Exception(msg)
