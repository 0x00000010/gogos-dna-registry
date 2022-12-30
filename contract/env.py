import smartpy as sp
import os

print('[*] ADMIN: ' + os.environ['COMP_ADMIN'])
# print('[*] TZIP-16: ' + os.environ['COMP_TZIP16'])

class Env_config:
    admin = sp.address(os.environ['COMP_ADMIN'])
    tzip16 = sp.utils.metadata_of_url("ipfs://" + os.environ['COMP_TZIP16'])
