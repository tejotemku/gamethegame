import pygame


class Display:
    def __init__(self):
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
        self.font = pygame.font.SysFont('Arial', 25)

        self.draw_info_box()
        self.draw_input_box()

    def draw_info_box(self):
        pygame.draw.rect(self.screen, self.box_border_color, self.info_box_border)
        pygame.draw.rect(self.screen, self.box_color, self.info_box)
        text_split = self.info_text.splitlines()
        for i, l in enumerate(text_split):
            self.screen.blit(self.font.render(l, False, (255, 255, 255)), (15, 20 + i*30))
        pygame.display.update()

    def draw_input_box(self):
        pygame.draw.rect(self.screen, self.box_border_color, self.input_box_border)
        pygame.draw.rect(self.screen, self.box_color, self.input_box)
        text_split = self.input_text.splitlines()
        for i, l in enumerate(text_split):
            self.screen.blit(self.font.render(l, False, (255, 255, 255)), (15, 470 + i*30))
        pygame.display.update()

    def add_info(self, text):
        if len(self.info_text.splitlines()) > 10:
            self.info_text = '\n'.join(self.info_text.splitlines()[1:])
        self.info_text += '\n' + text
        self.draw_info_box()

    def get_input(self):
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
                    else:
                        if len(self.input_text) <= 120:
                            if len(self.input_text.strip('\n')) % 40 == 0 and len(self.input_text) > 0:
                                self.input_text += '\n'
                            self.input_text += event.unicode
                self.draw_input_box()

