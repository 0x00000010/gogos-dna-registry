import smartpy as sp
import os

class GogoDNARegistry(sp.Contract):
    @staticmethod
    def split(s, sep):
        prev_idx = sp.local('pi', 0)
        res = sp.local('res', [])
        with sp.for_('itr', sp.range(0, sp.len(s))) as idx:
            with sp.if_(sp.slice(s, idx, 1).open_some() == sep):
                res.value.push(sp.slice(s, prev_idx.value, sp.as_nat(idx - prev_idx.value)).open_some())
                prev_idx.value = idx + 1
        with sp.if_(sp.len(s) > 0):
            res.value.push(sp.slice(s, prev_idx.value, sp.as_nat(sp.len(s) - prev_idx.value)).open_some())
        return res.value.rev()

    def __init__(self, admin):
        metadata_base = {
            "name": "GOGOs DNA Registry",
            "description" : "On-chain DNA registry for GOGOs",
            "version": "1.0.0",
            "interfaces": ["TZIP-012", "TZIP-016"],
            "authors": [
              "0x10 <https://twitter.com/0x00000010>",
            ],
            "homepage": "https://gogos.tez.page",
            "views": [],
            "source": {
                "tools": ["0x10"],
                "location": "https://github.com/0x00000010",
            },
        }

        self.init_metadata("metadata", metadata_base)

        self.init(
            # dna=sp.map(
            dna=sp.big_map(
                l={},
                # The ID of the token
                tkey=sp.TNat,
                # The DNA sequence string, like 0_1_2_3_4_5_6_7_8
                tvalue=sp.TString,
            ),
            config=sp.record(
                # How many pieces in a DNA strand?
                length=sp.nat(10),
                # Map of pieces, must match length
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
            ),
            # A single entry per DNA sequence, in order
            traits=sp.map({
                # Left Arm
                0: sp.map({
                    '0': 'None',
                    '1': 'Hoodie',
                    '2': 'Space',
                    '3': 'Bracelet',
                    '4': 'Jacket',
                    '5': 'Green',
                    '6': 'Denim',
                    '7': 'Zombie',
                    '8': 'Mech',
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
                # Left Hand
                1: sp.map({
                    '0': 'Flames',
                    '1': 'Dagger',
                    '2': 'Phone',
                    '3': 'Skull',
                    '4': 'Mace',
                    '5': 'Roboto',
                    '6': 'OK (Yellow)',
                    '7': 'OK (Blue)',
                    '8': 'OK (Red)',
                    '9': 'OK (Green)',
                    '10': 'Birdy',
                    '11': 'Claw',
                    '12': 'Fist',
                    '13': 'Torch',
                    '101': 'Number 1',
                    '102': 'Knives',
                    '103': 'Scythe',
                    '104': 'Thumbs Up',
                    '105': 'Mask',
                    '106': 'Cherries',
                    '107': 'Junk',
                    '108': 'Eyeball',
                    '109': 'Pitchfork',
                    '110': 'Heart',
                }),
                # Body
                2: sp.map({
                    '0': 'Hoodie',
                    '1': 'Space Jacket',
                    '2': 'Chef',
                    '3': 'Polo',
                    '4': 'Denim Vest',
                    '5': 'Dinosaur',
                    '6': 'Armour',
                    '7': 'Skully',
                    '8': 'Zombie',
                    '9': 'Purple Tee',
                    '10': 'Onesie',
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
                # Head
                3: sp.map({
                    '0': 'Flushed',
                    '1': 'Space Cadet',
                    '2': 'Demon',
                    '3': 'Purple Goblin',
                    '4': 'Peachy',
                    '5': 'Cat',
                    '6': 'Merperson',
                    '7': 'Bot',
                    '8': 'Zombie',
                    '9': 'Blue Goblin',
                    '10': 'Blue',
                    '11': 'Imp',
                    '12': 'Purple Goblin',
                    '13': 'Flushed',
                    '14': 'Ashen',
                    '15': 'Peachy',
                    '16': 'Bear',
                    '17': 'Skull',
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
                # Face
                4: sp.map({
                    '0': 'None',
                    '1': 'Happy',
                    '2': 'Angry',
                    '3': 'Tripping',
                    '4': 'Blazed',
                    '5': 'Ghoul',
                    '6': 'Scuba',
                    '7': 'Ripped',
                    '8': 'Vampire',
                    '9': 'Bear',
                    '10': 'Raging',
                    '11': 'Unimpressed',
                    '12': 'Roboto',
                    '13': 'Disgusted',
                    '14': 'Laughing',
                    '15': 'Shocked',
                    '16': 'Mask',
                    '17': 'None',
                    '18': 'None',
                    '101': 'Aokuma',
                    '102': 'Maung',
                    '103': 'Reaper',
                    '104': 'Chief',
                    '105': 'Exposed',
                    '106': 'Bunny Scout',
                    '107': 'Open',
                    '108': 'Builder A',
                    '109': 'Demon Alburn',
                    '110': 'Agent 7734',
                }),
                # Hat
                5: sp.map({
                    '0': 'None',
                    '1': 'Bowler',
                    '2': 'Crown',
                    '3': 'Bucket',
                    '4': 'Spikes',
                    '5': 'Padded',
                    '6': 'Helmet',
                    '7': 'None',
                    '101': 'None',
                    '102': 'None',
                    '103': 'None',
                    '104': 'Chief Beanie',
                    '105': 'None',
                    '106': 'None',
                    '107': 'None',
                    '108': 'Blue Hat',
                    '109': 'None',
                    '110': 'None',
                }),
                # Bling
                6: sp.map({
                    '0': 'None',
                    '1': 'Chain',
                    '2': 'Sword',
                    '3': 'None',
                    '4': 'None',
                    '5': 'None',
                    '101': 'Chain',
                    '102': 'None',
                    '103': 'Reaper Chain',
                    '104': 'None',
                    '105': 'None',
                    '106': 'None',
                    '107': 'None',
                    '108': 'Access Pass',
                    '109': 'None',
                    '110': 'None',
                }),
                # Hair
                7: sp.map({
                    '0': 'None',
                    '1': 'Bowl',
                    '2': 'Blue',
                    '3': 'Red',
                    '4': 'Purple',
                    '5': 'Green',
                    '6': 'Black',
                    '7': 'Blue Punk',
                    '8': 'Red Punk',
                    '9': 'Cheeto',
                    '10': 'Bubblegum',
                    '11': 'Red',
                    '12': 'Blue',
                    '13': 'Purple',
                    '14': 'Green',
                    '15': 'Yellow',
                    '16': 'None',
                    '101': 'Blue',
                    '102': 'Tiger Stripes',
                    '103': 'None',
                    '104': 'None',
                    '105': 'Black',
                    '106': 'Pink',
                    '107': 'None',
                    '108': 'Black',
                    '109': 'None',
                    '110': 'Black',
                }),
                # Accessory
                8: sp.map({
                    '0': 'None',
                    '1': 'Headset',
                    '2': 'Red Scarf',
                    '3': 'Blue Scarf',
                    '4': 'None',
                    '5': 'None',
                    '6': 'None',
                    '7': 'None',
                    '8': 'None',
                    '9': 'None',
                    '101': 'None',
                    '102': 'None',
                    '103': 'None',
                    '104': 'None',
                    '105': 'None',
                    '106': 'Cyberware',
                    '107': 'None',
                    '108': 'Mask',
                    '109': 'Sweatband',
                    '110': 'Headband',
                }),
                # Aura
                9: sp.map({
                    '0': 'Yellow',
                    '1': 'Blue',
                    '2': 'Red',
                    '3': 'Blue and Orange',
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
                })
            }),
            admin=admin,
        )

    @sp.onchain_view(doc='Retrieve the DNA Configuration')
    def get_dna_config(self):
        sp.result(self.data.config)

    @sp.onchain_view(doc='Retrieve the DNA in String format. Each piece is seperated by an underscore.')
    def get_dna(self, item):
        sp.set_type(item, sp.TNat)
        info = sp.local('info', self.data.dna[item])
        sp.set_type(info.value, sp.TString)
        sp.result(info.value)

    @sp.onchain_view(doc='Retrieve a named DNA array with a key integer reference.')
    def get_full_dna_keys(self, item):
        sp.set_type(item, sp.TNat)

        dna = sp.local('dna', self.data.dna[item])
        spl = sp.local('spl', self.split(dna.value, '_'))
        ret = sp.local('ret', sp.map())

        i = sp.local('i', 0)
        with sp.for_ ('xx', spl.value) as x:
            ret.value[self.data.config.pieces[i.value]] = x

            i.value = i.value + 1

        sp.result(ret.value)

    @sp.onchain_view(doc='Retrieve a named DNA array with the value as a String.')
    def get_full_dna_values(self, item):
        sp.set_type(item, sp.TNat)

        dna = sp.local('dna2', self.data.dna[item])
        spl = sp.local('spl2', self.split(dna.value, '_'))
        ret = sp.local('ret2', sp.map())

        i = sp.local('i2', 0)
        with sp.for_ ('xx', spl.value) as x:
            ret.value[self.data.config.pieces[i.value]] = self.data.traits[i.value][x]

            i.value = i.value + 1

        sp.result(ret.value)

    @sp.onchain_view(doc='Check if a token has any of a given set of trait IDs')
    def token_has_trait(self, params):
        sp.set_type(params, sp.TRecord(
            item=sp.TNat,
            trait=sp.TString,
            vals=sp.TSet(sp.TString),
        ))

        dna = sp.local('dna3', self.data.dna[params.item])
        spl = sp.local('spl3', self.split(dna.value, '_'))
        ret = sp.local('ret3', sp.map())

        i = sp.local('i3', 0)
        with sp.for_ ('xx', spl.value) as x:
            ret.value[self.data.config.pieces[i.value]] = x

            i.value = i.value + 1

        sp.result(params.vals.contains(ret.value[params.trait]))

    @sp.entry_point()
    def set_dna(self, params):
        sp.verify(self.data.admin == sp.sender, message = 'NOT_ADMIN')
        sp.set_type(params, sp.TList(sp.TPair(sp.TNat, sp.TString)))

        sp.for item in params:
            sp.set_type(item, sp.TPair(sp.TNat, sp.TString))
            self.data.dna[sp.fst(item)] = sp.snd(item)


sp.add_compilation_target("GogoDNARegistry_comp", GogoDNARegistry(
    admin = sp.address("tz1cxvWkkzkvKQz6Y81n2FUrxtX2pjtu9ziS")
))
