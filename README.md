# GOGOs DNA Registry

This contract stores the DNA information for GOGOs. When GOGOs were released there was no such thing as an "on-chain view" on Tezos and having this information availble on-chain is a key part of the long-term GOGOs development goals.

This repository creates a contract that provides a set of on-chain views regarding the unique DNA string associated with each GOGO.

This DNA was originally used to select the source images when generating the GOGOs and is available inside each GOGOs offchain TZIP-21 metadata.

This contract brings additional metadata on-chain that complements and subtly augments the existing offchain metadata.

### Differences from GOGOs TZIP21 / offchain meta

There are small differences between the "traits" shown on-chain and the ones that ended up in the final off-chain metadata.

The DNA values represents the "before" generation state of the GOGOs, and the final metadata shows their finshed state.

The main difference is that the DNA shows what's in the *left* hand _even if the left hand is out of the frame_, and the offchain meta also shows details of the "tool" which the on-chain DNA does not keep track of and represents so-called _hidden traits_ for GOGOs where you cannot see their left hand.

GOGOs selected their own "tools" (if any) as seen in the TZIP21 metadata at the end of their generation function and their input DNA did not impact their choice of tool, meaning the DNA does not show what is in the GOGOs *right* hand.

The DNA also does not track or dictate the "background" or "stress" values as these are the results of the GOGOs lived experience and outside of the control of their DNA. These values are available in the off-chain TZIP-21 metadata.

Meteor and UFO traits are intentionally untracked both on and off-chain to add a bit of spice.

### Usage

The contract adds the following on-chain views. You pass in the ID of the GOGO you want to query along with any additional options if the view requires it.

#### Get DNA Config

`get_dna_config()`

Returns the DNA configuration object

```
length:10
pieces:10 items
  0:left_arm
  1:left_hand
  2:body
  3:head
  4:face
  5:hat
  6:bling
  7:hair
  8:accessory
  9:aura
```

#### Get DNA

`get_dna(1)`

Returns the DNA for the specific GOGO in String format

```
@string_1: 0_4_9_14_13_4_3_7_1_2
```

#### Get Full DNA

There are 2 options here, the one returns integer keys and the other has the String

##### Key-Based

`get_full_dna_keys(1)`

Will return a trait map with integer values mapping to traits

```
@map_1:10 items
  accessory:1
  aura:2
  bling:3
  body:9
  face:13
  hair:7
  hat:4
  head:14
  left_arm:0
  left_hand:4
```

##### Value Based

`get_full_dna_values(1)`

Will return a trait map with the String value of the trait pre-populated

```
@map_1:10 items
  accessory:Headset
  aura:Red
  bling:None
  body:Purple Tee
  face:Disgusted
  hair:Blue Punk
  hat:Spikes
  head:Ashen
  left_arm:None
  left_hand:Mace
```

> Because left_arm is 'None' the left_hand is out of frame so it is not present in the final TZIP21 metadata in this example GOGO #1

#### Check Has Trait

`token_has_trait(token=1,trait='body',vals={'9'})`

Check if a given Token has any of the supplied Traits for a given Trait type

Will return True if the token has any of the matching values for the given trait.

### Forking

If you own or manage an existing Tezos FA2 collection you may use this repository to create your own on-chain dna trait registry.

You only need to deploy this if you need to access trait information about a specific collection on-chain inside other contracts, or if you want to make this information available to other third-parties on-chain for any reason.

Priming the DNA data is a very expensive operation, and costs about 0.01tz per DNA entry, meaning seeding the GOGOs DNA (5555 pieces) to mainnet costs around 55tz split across multiple batch operations. This only has to be done once though.

If you're deploying your own DNA library then you need to modify the contract with your specific configuration, and generate new `dna.json` files that map your token traits exactly.

The traits are hard-coded at contract origination and there are no entrypoints to update this information with. If you're making a dynamic DNA bank you will need to add this functionality yourself.

#### Key Changes

When modifying this for your own collection you must make changes to the dna_registry.py contract.

- Set your own metadata in the metadata_base value
- Define the `length` of your dna string
- Define the trait `pieces` and their order in the dna sequence
- Define a map for each dna trait to the available trait values
- Define your `mythic` dna markers

You must also configure your environment with the correct wallet, key etc.

If you modify the `metadata_base` value a new file will be generated and pinned to ipfs with your nft.storage STORAGE_API_KEY and the contract will be recompiled with this new value before origination when you run `compile.sh`

### Configure Environment

Create a `ghostnet.env` file inside the `contract` folder based on the `example.env` and fill in your specific values.

You need to add an admin wallet address and an NFT.storage key and set the network to a valid value like `ghostnet`.

You can create a `mainnet` env when you're ready to go to production.

All `*.env` files are ignored by version control so you can't accidently commit secrets.

### Deploying

You must have the file `~/smartpy-cli/SmartPy.sh` available in your home directory. You can follow the instructions at https://smartpy.io/docs/cli to configure.

Before you can originate you must first run `npm install` in the root. This will add the required Taquito dependencies.

Pass in the value of the env you want to deploy to, if you want to deploy to `ghostnet` make sure there is a properly configured `ghostnet.env` file in the root directory and run `./compile.sh ghostnet` to deploy to `ghostnet`.

The `compile.sh` file will call the `cli/originate.js` file - do not call this file yourself as it needs the environmental setup performed by `compile.sh` to be in place in order to function correctly.

This will not register any DNA it just compiles and originates a new contract.

#### Ledger (mainnet) vs Faucet (ghostnet) Deployments

If the COMP_USE_LEDGER value is set to 0 (e.g. non-mainnet deployments like ghostnet) will use whatever the `COMP_ADMIN_KEY` value in the env file is when originating. You can get this value from a testnet wallet faucet file.

If the COMP_USE_LEDGER value is set to 1 then this key is ignored during orignation and you will need to check your connected ledger and approve each transaction there. You must make sure the COMP_ADMIN wallet address matches the ledger, and the correct COMP_LEDGER_PATH is set in your env file (default wallet for Tezos on ledger is `44'/1729'/0'/0` and subsequent wallets created in ledger live are `44'/1729'/1'/0` then `44'/1729'/2'/0` etc)

All `mainnet` deployments should happen through a ledger hardware wallet only.

#### NFT.storage Requirement

During the `compile.sh` process the script will check if new TZIP16 metadata has been generated or not.

If new metadata is generated (ie you change the contract tzip16 metadata) then a new IPFS CID will be generated and pinned to ipfs and filecoin using https://nft.storage. You need to add a free key to the `STORAGE_API_KEY` value in your selected .env file. See https://nft.storage/docs/quickstart/#get-an-api-token for information on how to get this key. The selected `.env` file will be updated with the new `COMP_TZIP16` value.

### Mythics

To define a mythic GOGO, such as Aukouma (#786) the DNA is set to a repeating pattern of the same number 101 with the resulting DNA being 101_101_101_101_101_101_101_101_101_101

In the case of GOGOs the threshold is '100' and any DNA trait ID above that number is considered mythic. If your collection has more than 100 traits then increse this value to 1000 and make the adjustment in the contract. All mythics must be defined in the contract.

### Priming

Once the contract is deployed you can prime it with all of your DNA.

This is a *very expensive operation* so be sure that you've done all of your teting on ghostnet before performing this operation on mainnet.
