from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import sys

if len(sys.argv) != 2:
    print "Usage: findcoinbaseshieldings.py FILEOFTXIDS"
    exit(1)

# have a local running instance of zcashd
api = AuthServiceProxy("http://username:password@127.0.0.1:8232")

# coinbasecount will be incremented if a transaction:
# 1. has joinsplits
# 2. has transparent inputs
# 3. and at least one of those inputs is a coinbase utxo
coinbasecount = 0
txidcount = 0
fname = sys.argv[1]
with open(fname, 'r+') as f:
    for line in f:
        txidcount = txidcount + 1
        txid = line.strip()
        is_coinbase = False
        tx = api.getrawtransaction(txid,1)
        if len(tx["vjoinsplit"]) is 0:
            continue
        if len(tx["vin"]) is 0:
            continue
        inputs = tx["vin"]
        for vin in inputs:
            input_txid = vin["txid"]
            input_tx = api.getrawtransaction(input_txid,1)
            if len(input_tx["vin"]) is 0:
                continue
            if "coinbase" in input_tx["vin"][0]:
                #print input_tx["vin"][0]["coinbase"]
                is_coinbase = True
                break
        if is_coinbase is True:
            coinbasecount = coinbasecount + 1

print "number of txids = %d" % (txidcount)
print "number of tx shielding coinbase = %d (%.2f%%)" % (coinbasecount, 100.0 * coinbasecount / txidcount)

