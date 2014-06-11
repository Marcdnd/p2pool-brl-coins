import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
	sambacoin=math.Object(
        P2P_PREFIX='eba0062b'.decode('hex'), # 0xeb, 0xa0, 0x06, 0x2b
        P2P_PORT=11255, #SambaCoins's p2p port
        ADDRESS_VERSION=62, #look again in the sourcecode in the file base58.h, and find the value of PUBKEY_ADDRESS.
        RPC_PORT=11233, #SambaCoins's rpc port
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'sambacoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
		SUBSIDY_FUNC=lambda height: 4000*100000000 if height<10580 else 400*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=90, # one block generation time
        SYMBOL='SMB',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'sambacoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/sambacoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.sambacoin'), 'sambacoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://be.sambacoin.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://be.sambacoin.info/address/',
        TX_EXPLORER_URL_PREFIX='http://be.sambacoin.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1), #??
        DUMB_SCRYPT_DIFF=2**16, #??
        DUST_THRESHOLD=0.03e8, #??
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
