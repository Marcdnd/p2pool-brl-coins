from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
	sambacoin=math.Object(
		PARENT=networks.nets['sambacoin'],
		SHARE_PERIOD=5,
		CHAIN_LENGTH=24*60*60//10,
		REAL_CHAIN_LENGTH=24*60*60//10,
		TARGET_LOOKBEHIND=30,
        SPREAD=20, # blocks
        IDENTIFIER='ab88699cb8855988'.decode('hex'),
        PREFIX='9b89658bb9547bb8'.decode('hex'),
        P2P_PORT=11256,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=24006,
        BOOTSTRAP_ADDRS='theminingcrew.com'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: True,		
	),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
