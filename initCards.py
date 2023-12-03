# In improved_clue.py:
# from initCards import Card, get_deck
# add to top of file: cards = get_deck()
# On line 53, change card to card.get_name()
# After lines 187 and 211 add: 
# card_names = [card.get_name() for card in items]
# print(f"\033[34m{category}: {', '.join(card_names) if card_names else 'None'}\033[0m")


class Card:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name

def get_deck(): 
    # Create Deck
    deck = {
        "Suspects": [],
        "Weapons": [],
        "Rooms": []
    }

    # Suspects
    deck["Suspects"].append(Card(0, "Miss Scarlet"))
    deck["Suspects"].append(Card(1, "Colonel Mustard"))
    deck["Suspects"].append(Card(2, "Mrs. White"))
    deck["Suspects"].append(Card(3, "Mr. Green"))
    deck["Suspects"].append(Card(4, "Mrs. Peacock"))
    deck["Suspects"].append(Card(5, "Professor Plum"))

    # Weapons
    deck["Weapons"].append(Card(6, "Candlestick"))
    deck["Weapons"].append(Card(7, "Knife"))
    deck["Weapons"].append(Card(8, "Lead Pipe"))
    deck["Weapons"].append(Card(9, "Revolver"))
    deck["Weapons"].append(Card(10, "Rope"))
    deck["Weapons"].append(Card(11, "Wrench"))

    # Rooms
    deck["Rooms"].append(Card(12, "Dining"))
    deck["Rooms"].append(Card(13, "Ballroom"))
    deck["Rooms"].append(Card(14, "Billiards"))
    deck["Rooms"].append(Card(15, "Kitchen"))
    deck["Rooms"].append(Card(16, "Hallway"))
    deck["Rooms"].append(Card(17, "Porch"))
    deck["Rooms"].append(Card(18, "Library"))
    deck["Rooms"].append(Card(19, "Office"))

    return deck
