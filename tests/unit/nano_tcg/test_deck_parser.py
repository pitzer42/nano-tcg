from gameplay.nano_magic.deck import parse_deck_str


def test_numbered_list_with_empty_lines_and_tabs():
    deck_list = """
        2 Grim Lavamancer
        2 Restoration Angel
        2 Vendilion Clique
        4 Snapcaster Mage
        4 Spell Queller
        3 Teferi, Time Raveler
        2 Dovin's Veto
        3 Lightning Helix
        4 Lightning Bolt
        4 Opt
        4 Path to Exile
        2 Spreading Seas
        1 Mountain
        1 Plains
        2 Island
        1 Arid Mesa
        1 Glacial Fortress
        1 Sacred Foundry
        1 Spirebluff Canal
        1 Sulfur Falls
        2 Celestial Colonnade
        2 Field of Ruin
        2 Hallowed Fountain
        2 Steam Vents
        3 Scalding Tarn
        4 Flooded Strand
        
        1 Abrade
        2 Ashiok, Dream Render
        1 Celestial Purge
        2 Detention Sphere
        1 Disdainful Stroke
        2 Force of Negation
        1 Magma Spray
        2 Stony Silence
        3 Surgical Extraction
    """
    cards = parse_deck_str(deck_list)

    assert len(cards) == 75
