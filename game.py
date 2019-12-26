import json
import pygame
from os import walk, getcwd
from gamedisplay import Display
from map import Map
from location import Location
from player import Rouge, Wizard, Knight
from shop import Shop


class Game:
    def __init__(self):
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
        self.display.add_info('Choose game save you want to play:')
        self.display.add_info(getcwd())
        for (dirpath, dirnames, filenames) in walk(getcwd()):
            for file in filenames:
                if '.txt' == file[-4:]:
                    self.display.add_info(file[:-4])
            break
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.map:
                if self.map.game_state == 'explore':
                    self.map.list_possible_directions()
                if self.map.game_state == 'merchant':
                    self.list_shopping_items()
                if self.map.game_state == 'battle':
                    self.display.list_enemies(self.map.player.battle.list_of_enemies, self.map.player.battle.round)

            self.handle_command(self.display.get_input())

    def handle_command(self, command: str):
        # loading map
        if not self.map:
            return self.load_map(command)

        elif self.map.game_state == 'choose class':
            return self.choose_class(command)

        # saving map
        elif self.map.game_state == 'saving':
            return self.save_game(command)

        elif self.map.game_state == 'explore':
            return self.exploring_actions(command)

        elif self.map.game_state == 'battle':
            return self.battle_actions(command)

        elif self.map.game_state == 'level up':
            return self.level_up_actions(command)

        elif self.map.game_state == 'merchant':
            return self.shop_actions(command)

        return False

    def load_map(self, value):
        try:
            with open(f'{value}.txt', 'r') as file:
                self._map = self.map_json_deserializer(file)
            self.display.add_info('Map loaded successfully!')
            if not self.map.player:
                self.display.add_info('Choose your class: rouge, knight or wizard')
                self.map.game_state = 'choose class'
            return True
        except FileNotFoundError:
            self.display.add_info('Map file does not exist! Try again.')
            return False

    def save_game(self, game_save_name):
        json_string = self.map_json_serializer(self.map)
        file = open(f'{game_save_name}.txt', 'a')
        file.write(json_string)
        self.display.add_info('Game saved successfully!')
        file.close()

    @staticmethod
    def map_json_serializer(o: Map):
        temp_list = [o.name, o.player, o.game_state]
        for loc in o.locations:
            temp_mini_list = [loc.id, loc.type, loc.name, loc.description, loc.hidden_items, loc.nearby_locations]
            temp_list.append(temp_mini_list)
        return json.dumps(temp_list)

    @staticmethod
    def map_json_deserializer(file):
        temp_list = json.load(file)
        temp_locations_attributes_list = temp_list[3:]
        temp_locations_list = []
        for loc in temp_locations_attributes_list:
            temp_loc = Location(loc[0], loc[1], loc[2], loc[3], loc[5][0][0], loc[4])
            if len(loc[5]) > 1:
                for n in loc[5][1:]:
                    temp_loc.add_nearby_location(n[0], n[1])
            temp_locations_list.append(temp_loc)
        temp_map = Map(temp_list[0], temp_locations_list[0])
        if len(temp_locations_list) > 1:
            for loc in temp_locations_list[1:]:
                temp_map.add_location(loc)
        temp_map.player = temp_list[1]
        temp_map.game_state = temp_list[2]

        return temp_map

    def choose_class(self, command):
        if 'knight' in command:
            self.display.add_info('Choose your name')
            self.map.player = Knight(self.display.get_input(), self.display)
            self.map.game_state = 'explore'
            return True
        if 'wizard' in command:
            self.display.add_info('Choose your name')

            self.map.player = Wizard(self.display.get_input(), self.display)
            self.map.game_state = 'explore'
            return True
        if 'rouge' in command:
            self.display.add_info('Choose your name')
            self.map.player = Rouge(self.display.get_input(), self.display)
            self.map.game_state = 'explore'
            return True

    def exploring_actions(self, command):
        if 'shop' in command and self.map.locations[self.map.player.current_location].type == 'town':
            self.map.game_state = 'merchant'
            return True
        if 'small potion' in command:
            self.map.player.heal(10)
            self.map.display.add_info('You have been healed')
            return True
        if 'big potion' in command:
            self.map.player.heal(25)
            self.map.display.add_info('You have been healed')
            return True
        if 'list items' in command:
            for item in self.map.player.list_of_items:
                self.display.add_info(item)
        if 'search' in command:
            for item in self.map.player.current_location.hidden_items:
                self.map.player.add_new_item(item)
        for loc_id, loc_direction in self.map.locations[self.map.player.current_location].nearby_locations:
            if loc_direction in command:
                self.map.move_to_different_location(loc_id)
                return True
        return False

    def battle_actions(self, command):
        player_class = self.map.player.get_class()
        if 'item' in command:
            for item in self.map.player.list_of_items:
                self.display.add_info(item)
                return True
        elif player_class == 'knight':
            if 'normal' in command:
                self.map.player.normal_attack()
                return True
            elif 'heavy' in command:
                self.map.player.heavy_attack()
                return True

        elif player_class == 'wizard':
            if 'aoe' in command:
                self.map.player.aoe_attack()
                return True
            elif 'magic' in command:
                self.map.player.magic_attack()
                return True

        elif player_class == 'rouge':
            if 'life steal' in command:
                self.map.player.life_stealing_blade_attack()
                return True
            elif 'fast' in command:
                self.map.player.fast_attack()
                return True

        if 'small potion' in command:
            self.map.player.heal(10)
            self.map.display.add_info('You have been healed')
            self.map.player.battle.round(None, None)
            return True
        if 'big potion' in command:
            self.map.player.heal(25)
            self.map.display.add_info('You have been healed')
            self.map.player.battle.round(None, None)
            return True
        return False

    def level_up_actions(self, command):
        if self.compare_commands('power', command):
            self.map.player.power_increase()
            self.map.display.add_info(f'You have increased your power up to {self.map.player.power}')
            self.map.game_state = 'explore'
            return True
        if self.compare_commands('speed', command):
            self.map.player.speed_increase()
            self.map.display.add_info(f'You have increased your speed up to {self.map.player.speed}')
            self.map.game_state = 'explore'
            return True
        if self.compare_commands('hp', command):
            self.map.player.hp_increase()
            self.map.display.add_info(f'You have increased your hp up to {self.map.player.hp}')
            self.map.game_state = 'explore'
            return True
        if self.compare_commands('agility', command) and self.map.player.character_class == 'rouge':
            self.map.player.agility_increase()
            self.map.display.add_info(f'You have increased your agility up to {self.map.player.agility}')
            self.map.game_state = 'explore'
            return True
        if self.compare_commands('magic barrier', command) and self.map.player.character_class == 'wizard':
            self.map.player.magic_barrier_increase()
            self.map.display.add_info(f'You have increased your magic barrier up to {self.map.player.magic_barrier}')
            self.map.game_state = 'explore'
            return True
        return False

    def shop_actions(self, command):
        items = Shop().items
        for key in items.keys():
            if self.compare_commands(key, command):
                if self.map.player.remove_gold(items.get(key)):
                    self.map.player.add_new_item(key)
                    self.display.add_info(f'You have bought {key}')
                    self.map.game_state = 'explore'
                    return True
                else:
                    self.display.add_info('You don\'t have enough gold')

    def list_shopping_items(self):
        self.display.add_info('You can buy:')
        items = Shop().items
        for key in items.keys():
            self.display.add_info(f'{key} - {items.get(key)} gold')

    @staticmethod
    def compare_commands(str1: str, str2: str):
        return str1.lower() in str2.lower() or str2.lower() in str1.lower()


game = Game()
game.game_loop()
