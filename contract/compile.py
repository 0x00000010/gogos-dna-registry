import smartpy as sp

import os
import sys
sys.path.insert(0,"./")

Env = sp.io.import_script_from_url(f"file://{os.getcwd()}/env.py")
Registry = sp.io.import_script_from_url(f"file://{os.getcwd()}/dna_registry.py")

# Compile
admin = Env.Env_config.admin

# the tzip16 metadata (contract)
tzip16 = Env.Env_config.tzip16

sp.add_compilation_target(
    'GogoDNARegistry_comp',
    Registry.GogoDNARegistry(
        admin = admin,
        metadata = tzip16,
    )
)
