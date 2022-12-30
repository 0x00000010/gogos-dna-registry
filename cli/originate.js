import { tzip16 } from '@taquito/tzip16'

import { config } from './config.js'
import { getTezosLedger } from './tezos.js'

import fs from 'fs'

const loadJsonFile = path => {
  const data = fs.readFileSync(path, 'utf8')
  const json = JSON.parse(data)
  return json
}

const go = async () => {
  const tezos = await getTezosLedger()

  const contractPath = process.argv[2]
  const storagePath = process.argv[3]

  const contractFile = await loadJsonFile(contractPath)
  const storageFile = await loadJsonFile(storagePath)

  // console.log(contractFile, storageFile, config)
  const contractAddress = await tezos.contract.originate({
    code: contractFile,
    init: storageFile,
  }).then(async op => {
    await op.confirmation()
    return op.contractAddress
  })
  .catch(err => console.error(err))

  console.log(contractAddress)
}

go()
