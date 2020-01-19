from os import walk, getcwd
from file_system import map_json_deserializer, map_json_serializer
from player import Rouge, Wizard, Knight
from shop import Shop
from colorama import init, Fore


class Game:
    """
    This class defines a game
    """
    def __init__(self):
        """
        initiates game
        """
        self._map = None
        self._running = True
        init()

    @property
    def map(self):
        return self._map

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    def quit(self):
        self.running = False

    def game_loop(self):
        """
        This methods initiates all game mechanics, also listing items while in shop or enemies during battle
        """
        print(Fore.WHITE + 'Choose game save you want to play:')
        for (dirpath, dirnames, filenames) in walk(getcwd()):
            for file in filenames:
                if '.txt' == file[-4:]:
                    print(file[:-4])
            break
        while self.running:
            if self.map:
                if self.map.game_state == 'game_over':
                    self.running = False
                    return
            self.general_command_handler(self.get_input())

    def general_command_handler(self, command):
        """
        This is general command handler that sends command to more specific handlers depending on game state
        :param command: inputted command
        """

        if not self.map:
            self.load_map(command)
        elif self.map.game_state == 'choose class':
            self.choose_class(command)
        else:
            commands = {
                'help': self.help_command,
                'quit': self.quit
            }
            commands.update(self.map.player.basic_commands())
            commands.update(self.map.current_location.basic_commands())

            if self.map.game_state == 'merchant':
                commands.pop("small potion")
                commands.pop("big potion")

            if command in commands:
                commands.get(command)()
                return
            else:
                game_states = {
                    'explore': self.exploring_actions,
                    'saving': self.save_game,
                    'battle': self.battle_actions,
                    'level up': self.level_up_actions,
                    'merchant': self.shop_actions
                }
                if self.map.game_state in game_states:
                    game_states.get(self.map.game_state)(command)
                    return

    def load_map(self, file_name):
        """
        load map from file
        :param file_name: name of map's txt file
        """
        try:
            with open(f'{file_name}.txt', 'r') as file:
                self._map = map_json_deserializer(file)
            print('Map loaded successfully!')
            if not self.map.player:
                print('Choose your class: rouge, knight or wizard')
                self.map.game_state = 'choose class'
            else:
                print(f'You are in: {Fore.YELLOW}{self.map.current_location.name}{Fore.WHITE}')
                print(Fore.LIGHTYELLOW_EX + self.map.current_location.description + Fore.WHITE)
                self.map.current_location.get_locations()

                print(f'Write command \'{Fore.CYAN}help{Fore.WHITE}\' to view commands you can use!')
        except FileNotFoundError:
            print(f'{Fore.RED}Map file does not exist! Try again.{Fore.WHITE}')

    def save_game(self, game_save_name):
        """
        Saves the game to file
        :param game_save_name: game's save file's name
        """
        self.map.game_state = 'explore'
        json_string = map_json_serializer(self.map)
        with open(game_save_name + '.txt', 'w') as file:
            file.write(json_string)
        print('Game saved successfully!')
        file.close()

    def choose_class(self, command):
        """
        Command handler when user chooses class for a new player, also asks user for a name
        :param command: inputted command
        """
        player_dict = {
            'exp': 0,
            'level': 1,
            'skill points': 0,
            'gold': 0,
            'keys': [],
            'items': {}
        }

        classes = {
            'knight': (
                Knight,
                {
                    'hp': 40,
                    'hp max': 40,
                    'speed': 5,
                    'power': 8
                }),
            'wizard': (
                Wizard,
                {
                    'hp': 18,
                    'hp max': 18,
                    'speed': 7,
                    'power': 8,
                    'magic barrier': 4
                }),
            'rouge': (
                Rouge,
                {
                    'hp': 20,
                    'hp max': 20,
                    'speed': 7,
                    'power': 11,
                    'agility': 20
                })
        }

        for c in classes:
            if self.compare_commands(c, command):
                print('Choose your name')
                player_dict.update({'name': self.get_input()})
                player_dict.update(classes.get(c)[1])
                self.map.player = classes.get(c)[0](player_dict)
                self.map.game_state = 'explore'
                print(f'You are in: {Fore.YELLOW}{self.map.current_location.name}{Fore.WHITE}')
                print(Fore.LIGHTYELLOW_EX + self.map.current_location.description + Fore.WHITE)
                self.map.current_location.get_locations()
                print(f'Write command \'{Fore.CYAN}help{Fore.WHITE}\' to view commands you can use!')
                return
        print(f'{Fore.RED}Unknown class, please choose one of the following:{Fore.WHITE}')
        for c in classes:
            print(c)

    def exploring_actions(self, command):
        """
        Command handler during exploring map
        :param command: inputted command
        """

        if command == 'search':
            self.map.player.new_items(self.map.current_location.find_hidden_items())
            return
        elif command == 'upgrade':
            if self.map.player.skill_points > 0:
                self.map.game_state = 'level up'
                self.map.player.upgrade()
                return
            else:
                print('You don\'t have skill points')
                return
        elif self.map.current_location.type == 'town':
            if self.compare_commands('shop', command):
                self.map.game_state = 'merchant'
                shop = Shop()
                shop.leave_shop()
                print(shop)
                return
            elif self.compare_commands('save', command):
                self.map.game_state = 'saving'
                print('Type the name of the save')
                return
        self.map.move(command)

    def battle_actions(self, command):
        """
        Command handler during battle
        :param command: inputted command
        """
        player_class = self.map.player.character_class

        if player_class == 'wizard' and command == 'aoe':
            self.map.player.aoe_attack()
            return

        if len(command.split(' ')) > 1:
            enemy = command.split(' ')[-1]
            length = 1 + len(enemy)
            attack = command[:-length]
            if enemy.isdigit():
                actions = {}
                if player_class == 'knight':
                    actions = {
                        'normal': self.map.player.normal_attack,
                        'heavy':  self.map.player.heavy_attack
                        }
                elif player_class == 'wizard':
                    actions = {
                        'magic': self.map.player.magic_attack
                        }
                elif player_class == 'rouge':
                    actions = {
                        'life steal': self.map.player.life_stealing_blade_attack,
                        'fast':  self.map.player.fast_attack
                        }

                if attack in actions:
                    if int(enemy) <= len(self.map.player.battle.list_of_enemies):
                        actions.get(attack)(enemy)
                        return
                    else:
                        print('There is no enemy with that id')
        else:
            print(f'{Fore.RED}Invalid Command{Fore.WHITE}')

    def level_up_actions(self, command):
        """
        Command handler when player level ups
        :param command: inputted command
        """

        upgrades = {
            'power': self.map.player.power_increase,
            'speed': self.map.player.speed_increase,
            'hp': self.map.player.hp_increase,
        }
        if self.map.player.character_class == 'rouge':
            upgrades.update({'agility': self.map.player.agility_increase})
        elif self.map.player.character_class == 'wizard':
            upgrades.update({
                'magic barrier': self.map.player.magic_barrier_increase})

        if command in upgrades:
            upgrades.get(command)()
            self.map.game_state = 'explore'
            return

        print(f'{Fore.RED}Invalid Command{Fore.WHITE}')

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
                    print(f'You have bought {key}')
                    self.map.game_state = 'explore'
                    return
                else:
                    print('You don\'t have enough gold')
                    return
        if self.compare_commands(command, 'leave'):
            self.map.game_state = 'explore'
            print('You have left the shop')
            return
        print(f'{Fore.RED}Invalid Command{Fore.WHITE}')

    def help_command(self):
        self.map.player.help_command()
        self.map.current_location.help_command()

        game_states = {
            'battle': self.map.player.battle_help_command
        }

        if self.map.game_state in game_states:
            game_states.get(self.map.game_state)()

        if self.map.current_location.type == 'town':
            print(f'{Fore.CYAN}save{Fore.WHITE} - to save the game\n{Fore.CYAN}shop{Fore.WHITE} - to go to town shop')

    @staticmethod
    def compare_commands(str1: str, str2: str):
        """
        :return: compares two strings by checking if one contains the other
        """
        return str1.lower() in str2.lower() or str2.lower() in str1.lower()

    @staticmethod
    def get_input():
        print(Fore.GREEN)
        loop = True
        string = ''
        while loop:
            string = str(input())
            if string.strip():
                loop = False
        print(Fore.WHITE)
        return string


game = Game()
game.game_loop()
