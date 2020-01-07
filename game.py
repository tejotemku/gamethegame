import json
import pygame
from os import walk, getcwd
from gamedisplay import Display
from map import Map
from location import Location
from player import Rouge, Wizard, Knight
from shop import Shop


class Game:
    """
    This class defines a game
    """
    def __init__(self):
        """
        initiates game
        """
        self._map = None
        self._display = Display()
        self._running = True

    @property
    def map(self):
        return self._map

    @property
    def display(self):
        return self._display

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    def game_loop(self):
        """
        This methods initiates all game mechanics, also listing items while in shop or enemies during battle
        """
        self.display.add_info('Choose game save you want to play:')
        for (dirpath, dirnames, filenames) in walk(getcwd()):
            for file in filenames:
                if '.txt' == file[-4:]:
                    self.display.add_info(file[:-4])
            break
        while self.running:
            self.display.add_info(' ')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.map:
                if self.map.game_state == 'merchant':
                    self.display.list_shopping_items()
                if self.map.game_state == 'battle':
                    self.display.list_enemies(self.map.player.battle.list_of_enemies, self.map.player.battle.rounds)

            self.general_command_handler(self.display.get_input())

    def general_command_handler(self, command: str):
        """
        This is general command handler that sends command to more specific handlers depending on game state
        :param command: inputted command
        """
        if not self.map:
            self.load_map(command)
        elif self.map.game_state == 'choose class':
            self.choose_class(command)
        elif self.map.game_state == 'saving':
            self.map.game_state = 'explore'
            self.save_game(command)
        elif self.map.game_state == 'explore':
            self.exploring_actions(command)
        elif self.map.game_state == 'battle':
            self.battle_actions(command)
        elif self.map.game_state == 'level up':
            self.level_up_actions(command)
        elif self.map.game_state == 'merchant':
            self.shop_actions(command)

    def load_map(self, file_name):
        """
        load map from file
        :param file_name: name of map's txt file
        """
        try:
            with open(f'{file_name}.txt', 'r') as file:
                self._map = self.map_json_deserializer(file)
            self.display.add_info('Map loaded successfully!')
            if not self.map.player:
                self.display.add_info('Choose your class: rouge, knight or wizard')
                self.map.game_state = 'choose class'
        except FileNotFoundError:
            self.display.add_info('Map file does not exist! Try again.')

    def save_game(self, game_save_name):
        """
        Saves the game to file
        :param game_save_name: game's save file's name
        """
        json_string = self.map_json_serializer(self.map)
        with open(game_save_name + '.txt', 'w') as file:
            file.write(json_string)
        self.display.add_info('Game saved successfully!')
        file.close()

    @staticmethod
    def map_json_serializer(o: Map):
        """
        Serializes map object to json so it can be saved
        :param o: map object
        :return:
        """
        temp_list = []
        p = o.player
        temp_player = [p.name, p.hp_max, p.hp, p.speed, p.power, p.character_class, p.current_location,
                       p.exp, p.level, p.gold, p.items, p.keys]
        if p.character_class == 'wizard':
            temp_player.append(p.magic_barrier)

        elif p.character_class == 'rouge':
            temp_player.append(p.agility)

        temp_locations_list = []
        for loc in o.locations:
            temp_locations_list.append([loc.id, loc.type, loc.name, loc.description,
                                        loc.nearby_locations, loc.hidden_items, loc.enemies, loc.key])
        temp_list.append(temp_locations_list)
        temp_list.append(temp_player)
        return json.dumps(temp_list)

    def map_json_deserializer(self, file):
        """
        Deserializes json into map object
        :param file: file content
        :return:
        """
        temp_list = json.load(file)
        temp_locations = []
        for loc in temp_list[0]:
            temp_locations.append(Location(loc[0], loc[1], loc[2], loc[3], loc[4], loc[5], loc[6], loc[7]))
        p = temp_list[1]
        player = None
        if p:
            if p[5] == 'knight':
                player = Knight(p[0], self.display, p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])
            if p[5] == 'wizard':
                player = Wizard(p[0], self.display, p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12])
            if p[5] == 'rouge':
                player = Rouge(p[0], self.display, p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12])

        return Map(temp_locations, player)

    def choose_class(self, command):
        """
        Command handler when user chooses class for a new player, also asks user for a name
        :param command: inputted command
        """
        if self.compare_commands('knight', command):
            self.display.add_info('Choose your name')
            self.map.player = Knight(self.display.get_input(), self.display)
            self.map.game_state = 'explore'
        if self.compare_commands('wizard', command):
            self.display.add_info('Choose your name')
            self.map.player = Wizard(self.display.get_input(), self.display)
            self.map.game_state = 'explore'
        if self.compare_commands('rouge', command):
            self.display.add_info('Choose your name')
            self.map.player = Rouge(self.display.get_input(), self.display)
            self.map.game_state = 'explore'

    def exploring_actions(self, command):
        """
        Command handler during exploring map
        :param command: inputted command
        """
        if self.compare_commands('look around', command):
            self.map.list_possible_directions()
        elif self.compare_commands('shop', command) and \
                self.map.locations[self.map.player.current_location].type == 'town':
            self.map.game_state = 'merchant'
        elif self.compare_commands('save', command) and \
                self.map.locations[self.map.player.current_location].type == 'town':
            self.map.game_state = 'saving'
            self.display.add_info('Type the name of the save')
        elif self.compare_commands('small potion', command):
            self.map.player.heal(10)
            self.map.player.display.add_info('You have been healed')
        elif self.compare_commands('big potion', command):
            self.map.player.heal(25)
            self.map.player.display.add_info('You have been healed')
        elif self.compare_commands('items', command):
            for item in self.map.player.items:
                self.display.add_info(f'{item} - {self.map.player.items.get(item)}')
            for key in self.map.player.keys:
                self.display.add_info(key)
        elif self.compare_commands('search', command):
            items = self.map.locations[self.map.player.current_location].hidden_items
            if items:
                for item in items:
                    self.map.player.add_new_item(item)
        elif self.compare_commands('help', command):
            self.display.add_info('Try:\nlook around - to list where you can go\nitems - to list items you have\n\
            save - to save the game\nsearch - to search for hidden items')
            if self.map.locations[self.map.player.current_location].type == 'town':
                self.display.add_info('shop - to buy something')
        for loc_id, loc_direction in self.map.locations[self.map.player.current_location].nearby_locations:
            if self.compare_commands(loc_direction, command):
                if self.map.locations[loc_id].key:
                    if self.map.player.remove_item(self.map.locations[loc_id].key):
                        self.map.locations[loc_id].open_location()
                        self.display.add_info(f"You have opened: {self.map.locations[loc_id].name}")
                        self.map.move_to_different_location(loc_id)
                else:
                    self.map.move_to_different_location(loc_id)

    def battle_actions(self, command):
        """
        Command handler during battle
        :param command: inputted command
        """
        player_class = self.map.player.character_class
        if self.compare_commands('item', command):
            for item in self.map.player.items:
                if item != 'golden key':
                    self.display.add_info(item)

        elif player_class == 'knight':
            if self.compare_commands('normal', command):
                self.map.player.normal_attack(command.split(' ')[-1])
            elif self.compare_commands('heavy', command):
                self.map.player.heavy_attack(command.split(' ')[-1])
            elif self.compare_commands('help', command):
                self.display.add_info('Try:\nitems - list items you can use in battle\n\
                normal attack <enemy id> - uses normal attack on selected enemy\n\
                heavy attack <enemy id> - uses heavy attack on selected enemy')

        elif player_class == 'wizard':
            if self.compare_commands('aoe', command):
                self.map.player.aoe_attack()
            elif self.compare_commands('magic', command):
                self.map.player.magic_attack(command.split(' ')[-1])
            elif self.compare_commands('help', command):
                self.display.add_info('Try:\nitems - list items you can use in battle\n\
                               magic attack <enemy id> - uses magic attack on selected enemy\n\
                               aoe - attacks all enemies')
        elif player_class == 'rouge':
            if self.compare_commands('life steal', command):
                self.map.player.life_stealing_blade_attack(command.split(' ')[-1])
            elif self.compare_commands('fast', command):
                self.map.player.fast_attack(command.split(' ')[-1])
            elif self.compare_commands('help', command):
                self.display.add_info('Try:\nitems - list items you can use in battle\n\
                               life steal <enemy id> - uses attack on selected enemy that steals his hp and heals you\n\
                               fast attack <enemy id> - uses fast attack on selected enemy')
        if self.compare_commands('small potion', command) and self.map.player.remove_item('small potion'):
            self.map.player.heal(10)
            self.map.player.display.add_info('You have been healed')
            self.map.player.battle.round(None, None)
        if self.compare_commands('big potion', command) and self.map.player.remove_item('big potion'):
            self.map.player.heal(25)
            self.map.player.display.add_info('You have been healed')
            self.map.player.battle.round(None, None)

    def level_up_actions(self, command):
        """
        Command handler when player level ups
        :param command: inputted command
        """
        if self.compare_commands('power', command):
            self.map.player.power_increase()
            self.map.player.display.add_info(f'You have increased your power up to {self.map.player.power}')
            self.map.game_state = 'explore'
        if self.compare_commands('speed', command):
            self.map.player.speed_increase()
            self.map.player.display.add_info(f'You have increased your speed up to {self.map.player.speed}')
            self.map.game_state = 'explore'
        if self.compare_commands('hp', command):
            self.map.player.hp_increase()
            self.map.player.display.add_info(f'You have increased your hp up to {self.map.player.hp}')
            self.map.game_state = 'explore'
        if self.compare_commands('agility', command) and self.map.player.character_class == 'rouge':
            self.map.player.agility_increase()
            self.map.player.display.add_info(f'You have increased your agility up to {self.map.player.agility}')
            self.map.game_state = 'explore'
        if self.compare_commands('magic barrier', command) and self.map.player.character_class == 'wizard':
            self.map.player.magic_barrier_increase()
            self.map.player.display.add_info(f'You have increased your magic barrier up to \
{self.map.player.magic_barrier}')
            self.map.game_state = 'explore'

    def shop_actions(self, command):
        """
        Command handler during shopping
        :param command: inputted command
        """
        items = Shop().items
        for key in items.keys():
            if self.compare_commands(key, command):
                if self.map.player.remove_gold(items.get(key)):
                    self.map.player.add_new_item(key)
                    self.display.add_info(f'You have bought {key}')
                    self.map.game_state = 'explore'
                else:
                    self.display.add_info('You don\'t have enough gold')

    @staticmethod
    def compare_commands(str1: str, str2: str):
        """
        :return: compares two strings by checking if one contains the other
        """
        return str1.lower() in str2.lower() or str2.lower() in str1.lower()


game = Game()
game.game_loop()

# todo help and attributes listing and correct saving file so it replaces previous content
# todo notification box commands on actions
