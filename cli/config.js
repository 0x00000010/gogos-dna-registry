export const config = {
  rpc: process.env.COMP_RPC,
  useLedger: process.env.COMP_USE_LEDGER === 1 ? true : false,
  ledgerWalletPath: process.env.COMP_LEDGER_PATH,
  adminWallet: process.env.COMP_ADMIN,
  adminKey: (process.env.COMP_USE_LEDGER !== 1) ? process.env.COMP_ADMIN_KEY : null,
}
