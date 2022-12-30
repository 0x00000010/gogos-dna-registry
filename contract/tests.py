import smartpy as sp
import os

import sys

Registry = sp.io.import_script_from_url(f"file://{os.getcwd()}/dna_registry.py")

def setup_test_env():
    scenario = sp.test_scenario()
    scenario.add_flag("view-check-exception")

    user = sp.test_account("user")
    admin = sp.test_account("admin")

    registryContract = Registry.GogoDNARegistry(
        admin=admin.address,
        metadata = sp.utils.metadata_of_url("ipfs://bafkreiagzew46z4yfyhj6rxf4i73sxdc5d3cghrvjsyfzy3bjri4g75nba"),
    )

    scenario += registryContract

    return {
        "scenario": scenario,
        "user": user,
        "admin": admin,
        "contract": registryContract,
    }

@sp.add_test(name = 'GOGOs On-Chain DNA Registry Tests', is_default = True)
def test_registry():
    env = setup_test_env()

    scenario = env["scenario"]
    scenario.h1("GOGOs On-Chain DNA Tests")
    scenario.table_of_contents()

    user = env['user']
    admin = env['admin']

    # Try change DNA as user and fail
    scenario += env['contract'].set_dna(
        [
            (1, '0_4_9_14_13_4_3_7_1_2'),
            (2, '2_7_4_9_7_7_2_11_5_3'),
            (3, '0_11_1_14_9_4_1_8_6_0'),
            (4, '0_4_5_8_4_3_5_0_8_0'),
            (5, '0_2_0_11_3_2_4_0_0_2'),
        ]
    ).run(sender=user,valid=False,exception='NOT_ADMIN')

    # Try change DNA as admin and succeed
    scenario += env['contract'].set_dna(
        [
            (1, '0_4_9_14_13_4_3_7_1_2'),
            (2, '2_7_4_9_7_7_2_11_5_3'),
            (3, '0_11_1_14_9_4_1_8_6_0'),
            (4, '0_4_5_8_4_3_5_0_8_0'),
            (5, '0_2_0_11_3_2_4_0_0_2'),
            (786, '101_101_101_101_101_101_101_101_101_101'),
        ]
    ).run(sender=admin)

    # Retrieve info on the DNA config
    scenario.verify_equal(env['contract'].get_dna_config(), sp.record(
        length=sp.nat(10),
        mythics=sp.map({
            '101': 'Aokuma',
            '102': 'Maung',
            '103': 'Reaper',
            '104': 'Chief',
            '105': 'Cyborgia',
            '106': 'Bunny Scout',
            '107': 'Cyberjunk Droid',
            '108': 'Builder A',
            '109': 'Demon Alburn',
            '110': 'Agent 7734',
        }),
        # Map of pieces, must match length and be in order
        pieces=sp.map({
            0: 'left_arm',
            1: 'left_hand',
            2: 'body',
            3: 'head',
            4: 'face',
            5: 'hat',
            6: 'bling',
            7: 'hair',
            8: 'accessory',
            9: 'aura',
        })
    ))

    # Get DNA
    scenario.verify_equal(env['contract'].get_dna(1), '0_4_9_14_13_4_3_7_1_2')

    # Get expanded DNA info (keys)
    scenario.verify_equal(env['contract'].get_full_dna_keys(1), sp.map({
        'left_arm':'0',
        'left_hand':'4',
        'body':'9',
        'head':'14',
        'face':'13',
        'hat':'4',
        'bling':'3',
        'hair':'7',
        'accessory':'1',
        'aura':'2',
    }))

    # Get expanded DNA info (values)
    scenario.verify_equal(env['contract'].get_full_dna_values(1), sp.map({
        'left_arm':'None',
        'left_hand':'Mace',
        'body':'Purple Tee',
        'head':'Ashen',
        'face':'Disgusted',
        'hat':'Spikes',
        'bling':'None',
        'hair':'Blue Punk',
        'accessory':'Headset',
        'aura':'Red',
    }))

    # Check if a token has a given trait (passing)
    scenario.verify_equal(env['contract'].token_has_trait(sp.record(
        token=1,
        trait='body',
        vals={'9'},
    )), True)

    # Check if a token has a given trait (passing, multiple)
    scenario.verify_equal(env['contract'].token_has_trait(sp.record(
        token=1,
        trait='body',
        vals={'7','8','9'},
    )), True)

    # Check if a token has a given trait (failing)
    scenario.verify_equal(env['contract'].token_has_trait(sp.record(
        token=1,
        trait='body',
        vals={'10'},
    )), False)

    # Check if a token has a given trait (failing, multiple)
    scenario.verify_equal(env['contract'].token_has_trait(sp.record(
        token=1,
        trait='body',
        vals={'10','11','12'},
    )), False)

    # Get name of a trait
    scenario.verify_equal(env['contract'].trait_key_value(sp.record(
        trait='body',
        key='9',
    )), 'Purple Tee')

    scenario.verify_equal(env['contract'].trait_key_value(sp.record(
        trait='body',
        key='5',
    )), 'Dinosaur')

    # Check if a token is mythic (failing)
    scenario.verify_equal(env['contract'].is_mythic(1), False)

    # Check if mythic (passing)
    scenario.verify_equal(env['contract'].is_mythic(786), True)

    # Lock the DNA (fail as user)
    env['contract'].lock().run(sender=user,valid=False,exception='NOT_ADMIN')

    # Lock the DNA (succeed as admin)
    env['contract'].lock().run(sender=admin)

    # Try add DNA as admin and fail
    scenario += env['contract'].set_dna(
        [
            (6, '0_1_2_3_4_5_4_3_2_1'),
        ]
    ).run(sender=admin,valid=False,exception='REGISTRY_LOCKED')
