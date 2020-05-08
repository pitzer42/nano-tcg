from gameplay.nano_magic.deck import parse_deck_str


def test_create_from_deck_list():
    deck_str = """
        4 Aether Vial
        2 Benthic Biomancer
        2 Botanical Sanctum
        2 Breeding Pool
        1 Cavern of Souls
        1 Flooded Strand
        4 Force of Negation
        4 Island
        4 Kumena's Speaker
        4 Lord of Atlantis
        4 Master of the Pearl Trident
        4 Merfolk Mistbinder
        4 Merfolk Trickster
        4 Mutavault
        4 Once Upon a Time
        4 Silvergill Adept
        4 Spreading Seas
        4 Waterlogged Grove
    """
    expected_length = 60

    deck = parse_deck_str(deck_str)

    assert len(deck) == expected_length



