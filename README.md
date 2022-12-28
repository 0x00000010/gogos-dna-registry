# GOGOs DNA Registry

This contract stores the DNA information for GOGOs. When GOGOs were released there was no such thing as an "on-chain view" on Tezos.

This repository creates a contract that provides a set of on-chain views regarding the unique DNA string associated with each GOGO.

This DNA was used to select the source images when generating the GOGOs.

## Differences from TZIP21 / offchain meta

There are differences between the "traits" shown on-chain and the ones that ended up in the final off-chain metadata.

The DNA represents the "before" generation state of the GOGOs, and the final metadata shows the finshed state.

The main difference is that the DNA shows what's in the *left* hand even if the left hand is out of the frame, and the offchain meta also shows details of the "tool" which the on-chain DNA does not keep track of.

GOGOs selected their own tools at the end of their generation function and their DNA did not impact their choice of tool, meaning the DNA does not show what is in the GOGOs *right* hand.

The DNA also does not track or dictate the "background" or "stress" values.
