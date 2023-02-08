import { TezosToolkit, compose } from '@taquito/taquito'

import {
    Tzip16Module,
} from '@taquito/tzip16'

import {
    importKey,
} from '@taquito/signer'

// for mainnet ledger deployment
import TransportNodeHid from '@ledgerhq/hw-transport-node-hid'
import { LedgerSigner } from '@taquito/ledger-signer'

import { config } from './config.js'

export const tezos = new TezosToolkit(config.rpc)
tezos.addExtension(new Tzip16Module())

export const getTezosLedger = async () => {

  if (config.useLedger) {
    const transport = await TransportNodeHid.default.open('')
    const ledgerSigner = new LedgerSigner(transport, config.ledgerWalletPath)

    tezos.setProvider({ signer: ledgerSigner })

    const publicKey = await tezos.signer.publicKey()
    const publicKeyHash = await tezos.signer.publicKeyHash()
  } else {
    // faucet deploys like ghostnet use COMP_ADMIN_KEY env value
    await importKey(tezos, config.adminKey)
  }

  return tezos
}
