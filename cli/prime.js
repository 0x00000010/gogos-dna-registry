import { tzip16 } from '@taquito/tzip16'

import { config } from './config.js'
import { getTezosLedger } from './tezos.js'

import {
  uploadDNA,
} from './upload.js'

const boot = async () => {
  console.log('[*] Preparing to upload DNA')
  console.log(config)

  const tezos = await getTezosLedger()

  const mustProcess = process.argv.slice(2)

  const contractAddress = mustProcess[0]

  console.log(`[*] Loading contract ${contractAddress}`)

  tezos.contract.at(contractAddress, tzip16).then(
    async contract => {
      await uploadDNA(tezos, contract)
    }
  )
  .catch(err => console.error(err))
}

boot()
