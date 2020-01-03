import pygame
import time
from shop import Shop


class Display:
    """
    This class represents and manages a pygame window screen
    """
    def __init__(self):
        """
        This method creates display object launches a game window using pygame library
        """
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Game \"The Game\"')
        # input box
        self.input_box_border = pygame.rect.Rect(0, 450, 800, 150)
        self.input_box = pygame.rect.Rect(10, 460, 780, 130)
        self.input_text = ''
        # info box
        self.info_box_border = pygame.rect.Rect(0, 0, 800, 449)
        self.info_box = pygame.rect.Rect(10, 10, 780, 439)
        self.info_text = ''
        # colors and fonts
        self.box_border_color = (249, 242, 236)
        self.box_color = (26, 26, 26)
        self.font = pygame.font.SysFont('Arial', 20)

        self.draw_info_box()
        self.draw_input_box()

    def draw_info_box(self):
        """
        Draws displayed info and background
        """
        pygame.draw.rect(self.screen, self.box_border_color, self.info_box_border)
        pygame.draw.rect(self.screen, self.box_color, self.info_box)
        text_split = self.info_text.splitlines()
        for i, l in enumerate(text_split):
            self.screen.blit(self.font.render(l, True, (255, 255, 255)), (15, i*30))
        pygame.display.update()

    def draw_input_box(self):
        """
        Draws input box and hitherto written text
        """
        pygame.draw.rect(self.screen, self.box_border_color, self.input_box_border)
        pygame.draw.rect(self.screen, self.box_color, self.input_box)
        text_split = self.input_text.splitlines()
        for i, l in enumerate(text_split):
            self.screen.blit(self.font.render(l, True, (255, 255, 255)), (15, 470 + i*30))
        pygame.display.update()

    def add_info(self, text):
        """
        Adds and manages text to be displayed
        :param text: text to be displayed
        """
        if len(self.info_text.splitlines()) > 10:
            self.info_text = '\n'.join(self.info_text.splitlines()[-14:])
        self.info_text += '\n' + text
        self.draw_info_box()

    def get_input(self):
        """
        Gets inputted text and sends it to be handled
        :return: inputted text
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.input_text.strip('\n')) % 40 == 0:
                            self.input_text = self.input_text[:-1]
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        text = self.input_text
                        self.input_text = ''
                        self.draw_input_box()
                        return text
                        # self.add_info(text)
                    else:
                        if len(self.input_text) <= 120:
                            if len(self.input_text.strip('\n')) % 40 == 0 and len(self.input_text) > 0:
                                self.input_text += '\n'
                            self.input_text += event.unicode
                self.draw_input_box()

    def start_a_battle_string(self):
        """
        String displayed at the beginning of a battle
        """
        self.info_text = ' '
        self.add_info('      -------Battle-------')

    def list_enemies(self, list_of_enemies, round_nr):
        """
        Lists enemies and  their hp in a battle
        :param list_of_enemies: list of enemies in a battle
        :param round_nr: number of current round
        """
        self.add_info(f'   ---Round  {round_nr}---')
        for i, enemy in enumerate(list_of_enemies):
            self.add_info(f'{i+1}. {enemy.name} - {enemy.hp}')
        self.add_info('   ---' + len(str(round_nr))*'-' + '---')

    def list_shopping_items(self):
        """
        Lists items you can buy
        """
        self.add_info('You can buy:')
        items = Shop().items
        for key in items.keys():
            self.add_info(f'{key} - {items.get(key)} gold')

    def notification_box(self, text, time_length):
        """
        Notification box that shows custom information on center of game window for chosen amount of time
        :param text: text of notification
        :param time_length: time length of notification
        """
        rect_border = pygame.rect.Rect(300, 250, 200, 100)
        rect_box = pygame.rect.Rect(305, 255, 190, 90)
        pygame.draw.rect(self.screen, self.box_border_color, rect_border)
        pygame.draw.rect(self.screen, self.box_color, rect_box)
        self.screen.blit(self.font.render(text, True, (255, 255, 255)), (315, 300))
        pygame.display.update()
        time.sleep(time_length)
        self.draw_info_box()
        self.draw_input_box()
