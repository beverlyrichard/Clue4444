import random

 

# Define cards

cards = {

    "Suspects": ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"],

    "Weapons": ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"],

    "Rooms": ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]

}

 

class Player:

    def __init__(self, name, is_human):

        self.name = name

        self.is_human = is_human

        self.hand = []

        self.showed = []

        self.checklist = {category: list(items)

                          for category, items in cards.items()}

 

    def make_suggestion(self, sug_cards):

        if self.is_human:

            for category in ["Suspects", "Weapons", "Rooms"]:

                unknown_cards = [card for card in cards[category] if card not in self.hand and card not in [

                    shown[0] for shown in self.showed]]

 

                if unknown_cards:

                    # Create a list of tuples (card, count) for unknown cards

                    card_counts = [(card, sug_cards[category].count(card))

                                   for card in unknown_cards]

                    # Sort based on count

                    sorted_card_counts = sorted(

                        card_counts, key=lambda item: item[1], reverse=True)

 

                    print(

                        f'\033[1;35;40m{category}: {sorted_card_counts}\033[0m')

                else:

                    pass

            return input("Make your suggestion (Suspect, Weapon, Room): ").split(", ")

 

        else:

            return self.ai_make_suggestion(sug_cards)

 

    def ai_make_suggestion(self, sug_cards):

        suggestion = []

        for category in ["Suspects", "Weapons", "Rooms"]:

            unknown_cards = [card for card in cards[category] if card not in self.hand and card not in [

                shown[0] for shown in self.showed]]

 

            if unknown_cards:

                # Create a list of tuples (card, count) for unknown cards

                card_counts = [(card, sug_cards[category].count(card))

                               for card in unknown_cards]

                # Sort based on count

                sorted_card_counts = sorted(

                    card_counts, key=lambda item: item[1], reverse=True)

 

                # print(f'************** {sorted_card_counts} ******************')

                # Pick the card with the least count

                # Selecting the card from the tuple

                suggestion.append(sorted_card_counts[0][0])

            else:

                # If all cards in a category are known, choose randomly from all cards in the category

                suggestion.append(random.choice(cards[category]))

 

        return suggestion

 

    def refute_suggestion(self, suggestion):

        matching_cards = [card for card in self.hand if card in suggestion]

        if matching_cards:

            return random.choice(matching_cards)

        return None

 

    # def make_accusation(self):

    #     if self.is_human:

    #         return input("Make your accusation (Suspect, Weapon, Room): ").split(", ")

    #     else:

    #         # Simple AI for accusation (can be improved)

    #         return [random.choice(cards[category]) for category in ["Suspects", "Weapons", "Rooms"]]

 

    def update_checklist(self, card, player_name):

        for category in self.checklist:

            if card in self.checklist[category]:

                self.checklist[category].remove(card)

                if card not in self.hand:

                    # Add shown card to showed

                    self.showed.append([card, player_name])

 

    def display_hand(self):

        hand_by_category = {category: [] for category in cards}

        for card in self.hand:

            for category in cards:

                if card in cards[category]:

                    hand_by_category[category].append(card)

 

        print(f"\033[34m\n{self.name}'s Hand:\033[0m")

        for category, items in hand_by_category.items():

            print(

                f"\033[34m{category}: {', '.join(items) if items else 'None'}\033[0m")

 

        showed_by_category = {category: [] for category in cards}

        for card in self.showed:

            for category in cards:

                if card[0] in cards[category]:

                    showed_by_category[category].append(

                        f'{card[0]} ({card[1]})')

        print(f"\033[33m\nShown to {self.name}:\033[0m")

        for category, items in showed_by_category.items():

            print(

                f"\033[33m{category}: {', '.join(items) if items else 'None'}\033[0m")

 

# Initialize players

players = [Player("Human", True)] + \

    [Player(f"AI {i}", False) for i in range(1, 4)]

 

# Distribute cards

solution = {category: random.choice(items)

            for category, items in cards.items()}

remaining_cards = [card for sublist in cards.values()

                   for card in sublist if card not in solution.values()]

random.shuffle(remaining_cards)

for i, card in enumerate(remaining_cards):

    players[i % len(players)].hand.append(card)

 

# Main game loop

 

def main_game_loop():

    turn = 0

    game_over = False

    sug_cards = {'Suspects': [], 'Weapons': [], 'Rooms': []}

 

    while not game_over:

        current_player = players[turn % len(players)]

 

        # Display current player's hand

        if current_player.is_human:

            current_player.display_hand()

 

        print(

            f"\033[1;35;40m\n{current_player.name}'s turn (possible options)\033[0m")

 

        # Player makes a suggestion

        suggestion = current_player.make_suggestion(sug_cards)

        print(f"{current_player.name} suggests: {suggestion}")

        sug_cards['Suspects'].append(suggestion[0])

        sug_cards['Weapons'].append(suggestion[1])

        sug_cards['Rooms'].append(suggestion[2])

 

        # print(sug_cards) **************************

 

        # Other players refute the suggestion if possible

        for player in players:

            if player != current_player:

                refutation = player.refute_suggestion(suggestion)

                if refutation:

                    print(

                        f"\033[31m{player.name} shows a card to {current_player.name}\033[0m")

                    current_player.update_checklist(refutation, player.name)

                    break

 

        if not refutation:

            # AI makes an accusation if suggestion was not refuted

            accusation = suggestion

            print(f"\n\n{current_player.name} makes an accusation: {accusation}")

            if accusation == list(solution.values()):

                print(

                    f"\033[32mCongratulations {current_player.name}, you have won the game!\033[0m")

                game_over = True

            else:

                print(

                    f"\033[31mIncorrect accusation. {current_player.name} has lost the game.\033[0m")

                # AI is eliminated from the game

                players.remove(current_player)

                if len(players) == 1:

                    print(

                        f"\033[32m{players[0].name} is the only player remaining and wins by default!\033[0m")

                    game_over = True

        turn += 1

 

# Start the game

main_game_loop()
