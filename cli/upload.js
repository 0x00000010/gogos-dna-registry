import dna from '../dna/dna.json' assert { type: "json" }

const batchSize = 556

// console.log(dna, batchSize)

const chunk = (obj, size) => {
  console.log(Object.keys(obj))
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
  const result = {}
  for (let id of ids) {
    result[id] = getEntry(id)
  }
  return result
}

const send = async (contract, tezos) => {
  const batches = chunk(dna, batchSize)
  console.log(batches,batches.length)
  for (let x = 0; x < batches.length; x++) {
    const payload = prepareBatch(batches[x])
    console.log('payload:', payload)
  }
}

export const uploadDNA = async (tezos, contract) => {
  console.log('[*] Uploading DNA')
  await send(contract, tezos)
}
