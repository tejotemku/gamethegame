from os import walk, getcwd
from file_system import map_json_deserializer, map_json_serializer
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
        self._running = True

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
        print('Choose game save you want to play:')
        for (dirpath, dirnames, filenames) in walk(getcwd()):
            for file in filenames:
                if '.txt' == file[-4:]:
                    print(file[:-4])
            break
        while self.running:
            self.general_command_handler(str(input()))

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

            if command in commands:
                commands.get(command)()
                return
            elif self.map.game_state == 'explore':
                self.exploring_actions(command)
                return
            elif self.map.game_state == 'saving':
                self.map.game_state = 'explore'
                self.save_game(command)
                return
            elif self.map.game_state == 'battle':
                self.battle_actions(command)
                return
            elif self.map.game_state == 'level up':
                self.level_up_actions(command)
                return
            elif self.map.game_state == 'merchant':
                self.shop_actions(command)
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
                print('Write command \'help\' to view commands you can use!')
        except FileNotFoundError:
            print('Map file does not exist! Try again.')

    def save_game(self, game_save_name):
        """
        Saves the game to file
        :param game_save_name: game's save file's name
        """
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
        classes = {
            'knight': Knight,
            'wizard': Wizard,
            'rouge': Rouge
        }

        for c in classes:
            if self.compare_commands(c, command):
                print('Choose your name')
                self.map.player = classes.get(c)(str(input()))
                self.map.game_state = 'explore'
                print('Write command \'help\' to view commands you can use!')
                return

    def exploring_actions(self, command):
        """
        Command handler during exploring map
        :param command: inputted command
        """

        if command == 'search':
            self.map.player.new_items(self.map.current_location.find_hidden_items())
            return

        if self.map.current_location.type == 'town':
            if self.compare_commands('shop', command):
                self.map.game_state = 'merchant'
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

        if player_class == 'knight':
            if self.compare_commands('normal', command):
                self.map.player.normal_attack(command.split(' ')[-1])
            elif self.compare_commands('heavy', command):
                self.map.player.heavy_attack(command.split(' ')[-1])
            elif self.compare_commands('help', command):
                print('Try:\nitems - list items you can use in battle\n\
                normal attack <enemy id> - uses normal attack on selected enemy\n\
                heavy attack <enemy id> - uses heavy attack on selected enemy\nquit - quits game')

        elif player_class == 'wizard':
            if self.compare_commands('aoe', command):
                self.map.player.aoe_attack()
            elif self.compare_commands('magic', command):
                self.map.player.magic_attack(command.split(' ')[-1])
            elif self.compare_commands('help', command):
                print('Try:\nitems - list items you can use in battle\n\
                               magic attack <enemy id> - uses magic attack on selected enemy\n\
                               aoe - attacks all enemies\nquit - quits game')
        elif player_class == 'rouge':
            if self.compare_commands('life steal', command):
                self.map.player.life_stealing_blade_attack(command.split(' ')[-1])
            elif self.compare_commands('fast', command):
                self.map.player.fast_attack(command.split(' ')[-1])
            elif self.compare_commands('help', command):
                print('Try:\nitems - list items you can use in battle\n\
                               life steal <enemy id> - uses attack on selected enemy that steals his hp and heals you\n\
                               fast attack <enemy id> - uses fast attack on selected enemy\nquit - quits game')
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
                    print(f'You have bought {key}')
                    self.map.game_state = 'explore'
                else:
                    print('You don\'t have enough gold')
        if self.compare_commands(command, 'leave'):
            self.map.game_state = 'explore'
            print('You have left the shop')

    def help_command(self):
        self.map.player.help_command()
        self.map.current_location.help_command()

        game_states = {
            'battle': self.map.player.battle_help_command,
            'merchant': Shop.leave_shop
        }

        if self.map.game_state in game_states:
            game_states.get(self.map.game_state)()

        if self.map.current_location == 'town':
            print('save - to save the game\nshop - to go to town shop')

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
