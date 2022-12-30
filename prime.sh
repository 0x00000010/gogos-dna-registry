#!/bin/bash

# pass in the env name to this command
COMP_NETWORK=$1

# pass in the dna registry address as second argument
COMP_CONTRACT=$2

if [ ! -f "$COMP_NETWORK".env ]; then
    echo "$COMP_NETWORK.env does not exist..."
    exit 1
fi

if [ ! -d node_modules ]; then
    echo "Dependencies not installed, run 'npm install' first..."
    exit 1
fi

echo "[*] Prepare DNA Upload"
echo "[i] Network: $COMP_NETWORK"
echo "[i] Contract: $COMP_CONTRACT"
export $(cat $COMP_NETWORK.env | xargs)

export NODE_NO_WARNINGS=1

node cli/prime.js $COMP_CONTRACT
