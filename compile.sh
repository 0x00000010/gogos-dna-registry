#!/bin/bash

# pass in the env name to this command
COMP_NETWORK=$1

TARGET="GogoDNARegistry_comp"
OUTPUT_DIR=compile/registry

if [ ! -f "$COMP_NETWORK".env ]; then
    echo "$COMP_NETWORK.env does not exist..."
    exit 1
fi

if [ ! -f ~/smartpy-cli/SmartPy.sh ]; then
    echo "~/smartpy-cli/SmartPy.sh does not exist..."
    exit 1
fi

echo "[*] Prepare DNA Registry"
echo "[i] Network: $COMP_NETWORK"
export $(cat $COMP_NETWORK.env | xargs)

cd contract > /dev/null

echo "[*] Compiling Registry"

~/smartpy-cli/SmartPy.sh compile compile.py $OUTPUT_DIR

echo "[*] Generated TZIP-16 Metadata"

echo "[i] Existing CID: $COMP_TZIP16"

NEW_TZIP16=$(ipfs add --cid-version 1 $OUTPUT_DIR/$TARGET/step_000_cont_0_metadata.metadata.json -Q)

echo "[i] Generated CID: $NEW_TZIP16"

if [ "$COMP_TZIP16" != "$NEW_TZIP16" ]; then
  echo "[i] Metadata has changed, adding new metadata"
  ipfs pin add $NEW_TZIP16
  echo "[i] Pinning..."

  PINRES=$(curl -X 'POST' \
    'https://api.nft.storage/upload' \
    -H 'accept: application/json' \
    -H "Authorization: Bearer $STORAGE_API_KEY" \
    -H 'Content-Type: application/json' \
    --data-binary "@$OUTPUT_DIR/$TARGET/step_000_cont_0_metadata.metadata.json")

  echo "[i] Finished pinning new metadata, updating configurations"
  sed -i.bak "s/COMP_TZIP16=.*/COMP_TZIP16='${NEW_TZIP16}'/" ../$COMP_NETWORK.env
  COMP_TZIP16=$NEW_TZIP16
  echo "[i] Recompiling with new metadata CID..."
  ~/smartpy-cli/SmartPy.sh compile compile.py $OUTPUT_DIR
else
  echo "[i] Metadata verified"
fi

echo "[*] Originating Registry"

cd - > /dev/null

CONTRACT_ADDR=$(node cli/originate.js contract/$OUTPUT_DIR/$TARGET/step_000_cont_0_contract.json contract/$OUTPUT_DIR/$TARGET/step_000_cont_0_storage.json)
#
echo "[i] Originated ${CONTRACT_ADDR}"
