def parse(deck: str):
    cards = list()
    deck = deck.split('\n')
    for deck_entry in deck:
        deck_entry = deck_entry.strip().lower()
        if deck_entry == '':
            continue
        try:
            first_space_index = deck_entry.index(' ')
            quantity_str = deck_entry[:first_space_index]
            quantity_str.replace('x', '')
            quantity_str = quantity_str.strip()
            quantity = int(quantity_str)
            card = deck_entry[first_space_index + 1:]
            card = card.strip()
        except:
            quantity = 1
            card = deck_entry.strip()

        cards += [card] * quantity

    return cards
        




