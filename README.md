# GOGOs DNA Registry

This contract stores the DNA information for GOGOs. When GOGOs were released there was no such thing as an "on-chain view" on Tezos.

This repository creates a contract that provides a set of on-chain views regarding the unique DNA string associated with each GOGO.

This DNA was used to select the source images when generating the GOGOs.

### Differences from GOGOs TZIP21 / offchain meta

There are differences between the "traits" shown on-chain and the ones that ended up in the final off-chain metadata.

The DNA represents the "before" generation state of the GOGOs, and the final metadata shows the finshed state.

The main difference is that the DNA shows what's in the *left* hand _even if the left hand is out of the frame_, and the offchain meta also shows details of the "tool" which the on-chain DNA does not keep track of and represents so-called _hidden traits_ for GOGOs where you cannot see their left hand.

GOGOs selected their own "tools" (if any) at the end of their generation function and their DNA did not impact their choice of tool, meaning the DNA does not show what is in the GOGOs *right* hand.

The DNA also does not track or dictate the "background" or "stress" values as these are the results of the GOGOs lived experience and outside of the control of their DNA.

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

### Forking

You only need to add this if you need to access trait information about a specific collection on-chain inside other contracts or if you want to make this information available to third-parties on-chain.

Priming the DNA data is a very expensive operation, and costs about 0.01tz per DNA entry, meaning seeding the GOGOs DNA (5555 pieces) to mainnet costs around 55tz split across multiple batch operations. This only has to be done once.

If you're deploying your own DNA library then you need to modify the contract with your specific configuration, and generate new `dna.json` files that map your token traits exactly.

The traits are hard-coded at contract origination and there are no entrypoints to update this information with. If you're making a dynamic DNA bank you will need to add this functionality yourself.

### Building

Create a `ghostnet.env` file inside the `contract` folder based on the `example.env` and fill in your specific values

You need to add an admin wallet address and an NFT.storage key and set the network to a valid value like `ghostnet`.

### Deploying
