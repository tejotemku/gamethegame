class Game:
    def __init__(self, game_map):
        self._map = game_map

    @property
    def map(self):
        return self._map

    def handle_command(self, command: str):
        if self.map.map.game_state == 'explore':

            for loc_id, loc_direction in self.map.get_all_locations()[self.map.player.current_location].nearby_locations:
                if loc_direction in command:
                    self.map.move_to_different_location(loc_id)
                    return True
        elif self.map.game_state == 'battle':
            player_class = self.map.player().get_class()
            if player_class == 'knight':
                if 'normal' in command:
                    self.map.player().normal_attack()
                    return True
                elif 'heavy' in command:
                    self.map.player().heavy_attack()
                    return True
            if player_class == 'wizard':
                if 'aoe' in command:
                    self.map.player().aoe_attack()
                    return True
                elif 'magic' in command:
                    self.map.player().magic_attack()
                    return True
            if player_class == 'rouge':
                if 'life steal' in command:
                    self.map.player().life_stealing_blade_attack()
                    return True
                elif 'fast' in command:
                    self.map.player().fast_attack()
                    return True
        elif self.map.game_state == 'level up':
            if command == 'power':
                self.map.player.power_increase()
                self.map.display.add_info(f'You have increased your power up to {self.map.player.power}')
                return True
            if command == 'speed':
                self.map.player.speed_increase()
                self.map.display.add_info(f'You have increased your speed up to {self.map.player.speed}')
                return True
            # todo proceed
        return False
