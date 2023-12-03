# Add to improved_clue.py at top of file bc I don't have push access:
# Initialize Pygame:
# pygame_initializer = PygameInitializer(1000, 800)

# Change main_game_loop to take in parameter pygame_initializer

# Add to improved_clue.py at top of main_game_loop:
# pygame_initializer.run(players, cards)


import pygame
import time

class PygameInitializer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 24)
        pygame.display.set_caption("Clue")

    def run(self, players, cards):
        turn = 0
        sug_cards = {'Suspects': [], 'Weapons': [], 'Rooms': []}
        running = True
        while running:
            current_player = players[turn % len(players)]

            # self.display_turn_with_options(current_player, cards, sug_cards)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.rect.collidepoint(mouse_pos):
                            button.action(cards, sug_cards, current_player)

            self.render(players, current_player, cards, sug_cards)

            turn += 1
        time.sleep(1)
        pygame.quit()

    # def display_turn_with_options(self, player, cards, sug_cards):
    #     text = "\033[1;35;40m\n{}'s turn (possible options)\033[0m".format(player.name)
    #     font = pygame.font.Font(None, 24)
    #     text_surface = font.render(text, True, (0, 0, 0))
    #     text_rect = text_surface.get_rect()
    #     self.screen.blit(text_surface, text_rect)

    def draw_players(self, x, y, playerName, rect_color, width=200, height=100, font_size=24, text_color=(0, 0, 0)):
        pygame.draw.rect(self.screen, rect_color, (x, y, width, height))
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(playerName, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_control_panel(self, humanPlayer, x=400, y=125, width=300, height=500, rect_color=(125, 125, 125)):
        pygame.draw.rect(self.screen, rect_color, (x, y, width, height))

        font = pygame.font.Font(None, 24)
        title_text_surface = font.render("Your hand:", True, (0, 0, 0))
        text_rect = title_text_surface.get_rect(center=(x + width // 2, y + 30))
        self.screen.blit(title_text_surface, text_rect)

        self.draw_cards(humanPlayer, x, y)

        options_text_surface = font.render("Pick one:", True, (0, 0, 0))
        options_text_rect = options_text_surface.get_rect(center=(x + width // 2, y + height - 90))
        self.screen.blit(options_text_surface, options_text_rect)

        # Clear existing buttons
        self.buttons = []

        # Draw buttons
        suggest_button = Buttons(x + 10, y + height - 60, 100, 40, (255, 255, 255), "Suggest", self.suggest_action)
        accuse_button = Buttons(x + width - 110, y + height - 60, 100, 40, (255, 255, 255), "Accuse", self.accuse_action)

        self.buttons.extend([suggest_button, accuse_button])
        
    def draw_cards(self, humanPlayer, x, y):
        cardXVal = x + 10
        cardYVal = y + 60
        cardWidth, cardHeight = 80, 100
        max_line_width = cardWidth - 10

        for card in humanPlayer.get_hand():
            pygame.draw.rect(self.screen, (128, 0, 128), (cardXVal, cardYVal, cardWidth, cardHeight))
            font = pygame.font.Font(None, 18)

            # Wrap the text if its wider than the card
            lines = self.wrap_text(card.get_name(), font, max_line_width)
            text_y = cardYVal + 10
            for line in lines:
                text_surface = font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(cardXVal + cardWidth // 2, text_y))
                self.screen.blit(text_surface, text_rect)
                # Move down for the next line
                text_y += text_surface.get_height()

            cardXVal += 100
            # Keep cards within control panel width
            if cardXVal > 620:
                cardXVal = 410
                cardYVal += 120
    
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            test_width, _ = font.size(test_line)

            if test_width <= max_width:
                current_line = test_line
            else:
                current_line = word
        
        lines.append(current_line)
        return lines
    
    def suggest_action(self, cards, sug_cards, player):
        print("Suggest")
        suggestion_info = self.make_suggestion(cards, sug_cards, player)
        self.draw_suggestion_info(suggestion_info, x=850, y=300)

    def accuse_action(self, cards, sug_cards, player):
        print("Accuse")

    def draw_suggestion_info(self, suggestion_info, x, y):
        text_y = y
        
        if len(suggestion_info) < 1:
            text_surface = self.font.render("You have not made any suggestions", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x, text_y))
            self.screen.blit(text_surface, text_rect)
        else:
            for suggestion in suggestion_info:
                text_surface = self.font.render(str(suggestion), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x, text_y))
                self.screen.blit(text_surface, text_rect)

                text_y += text_surface.get_height()

    def make_suggestion(self, cards, sug_cards, player):
        unknown_cards = []
        for category in ["Suspects", "Weapons", "Rooms"]:
            unknown_cards = [card for card in cards[category] if card not in player.hand and card not in [
                shown[0] for shown in player.showed]]

            if unknown_cards:
                # Create a list of tuples (card, count) for unknown cards
                card_counts = [(card.get_name(), sug_cards[category].count(card))
                                for card in unknown_cards]
                # Sort based on count
                sorted_card_counts = sorted(
                    card_counts, key=lambda item: item[1], reverse=True)
                category_info = f'{category}: {sorted_card_counts}'
                unknown_cards.append(category_info)
        
        return unknown_cards

    def render(self, players, current_player, cards, sug_cards):
        # Clear the screen
        self.screen.fill((255, 255, 255))

        font = pygame.font.Font(None, 24)
        text_surface = font.render("Players:", True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(120, 50))
        self.screen.blit(text_surface, text_rect)

        # Display players while also getting human player
        human_player = None
        x = 50
        y = 100
        for player in players:
            if player.is_human == True:
                human_player = player
                self.draw_players(x, y, player.name, (255, 165, 0))
            else:
                self.draw_players(x, y, player.name, (0, 255, 255))
            
            y += 150

        self.draw_control_panel(human_player)
        for button in self.buttons:
            button.draw(self.screen)
        
        pygame.display.flip()

class Buttons:
    def __init__(self, x, y, width, height, color, text, action: None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
