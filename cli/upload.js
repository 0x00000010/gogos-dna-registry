import dna from '../dna/dna.json' assert { type: "json" }
import { config } from './config.js'

const batchSize = 800

const chunk = (obj, size) => {
  // This prevents infinite loops
  if (size < 1) throw new Error('Size must be positive')

  const array = Object.keys(obj)

  const result = []
  for (let i = 0; i < array.length; i += size) {
    result.push(
      array.slice(i, i + size)
    )
  }
  return result
}

const getEntry = (id) => {
  return dna[id].join('_')
}

const prepareBatch = (ids) => {
  const result = []
  for (let id of ids) {
    result.push([parseInt(id), getEntry(id)])
  }
  return result
}

const send = async (contract, tezos) => {
  const batches = chunk(dna, batchSize)
  for (let x = 0; x < batches.length; x++) {
    const payload = prepareBatch(batches[x])

    const batch = tezos.contract.batch()
    const transferOp = await batch
      .withContractCall(
        contract.methods.set_dna(payload)
      ).send()
      .catch(e => console.log(e))

    const transfered = await transferOp.confirmation()
    console.log(`[i] Confirmation ${x + 1} of ${batches.length}: ${transfered}`)
  }
}

export const uploadDNA = async (tezos, contract) => {
  console.log('[*] Uploading DNA')
  if (config.useLedger) {
    console.log('[i] Please confirm the transaction(s) on your ledger')
  }
  await send(contract, tezos)
}
