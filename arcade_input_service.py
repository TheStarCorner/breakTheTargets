import sys
# from game.point import Point
# import game.constants as constants
import arcade

class ArcadeInputService:
    """Detects player input. The responsibility of the class of objects is to detect and communicate player keypresses.

    Stereotype: 
        Service Provider

    Attributes:
        _keys (list): 
            WASD: movement for player 1
            IJKL: movement for player 2
            C: shooting for player 1
            P: shooting for player 2
    """

    def __init__(self):
        """The class constructor."""
        self._keys = []
    
    def set_key(self, key, modifiers):
        #Ignoring modifies ar this point...
        self._keys.append(key)

    def remove_key(self, key, modifiers):
        self._keys.remove(key)

    def get_direction_player1(self):
        """Gets the selected direction for the given player.

        Returns:
            Point: The selected direction.
        """
        x = 0
        y = 0

        if arcade.key.A in self._keys:
            x = -1
        elif arcade.key.D in self._keys:
            x = 1

        if arcade.key.W in self._keys:
            y = 1
        elif arcade.key.S in self._keys:
            y = -1

        # velocity = Point(x, y)
        # return velocity

    def get_direction_player2(self):
        """Gets the selected direction for the given player.

        Returns:
            Point: The selected direction.
        """
        x = 0
        y = 0

        if arcade.key.J in self._keys:
            x = -1
        elif arcade.key.L in self._keys:
            x = 1

        if arcade.key.I in self._keys:
            y = 1
        elif arcade.key.K in self._keys:
            y = -1

        # velocity = Point(x, y)
        # return velocity
            
    # def is_player1_shooting(self):
    #     if arcade.key.V in self._keys:
    #         arcade.sound.play_sound(arcade.sound.load_sound(constants.SHOT_SOUND))
    #         return True
    #     return False
    
    # def is_player2_shooting(self):
    #     if arcade.key.P in self._keys:
    #         arcade.sound.play_sound(arcade.sound.load_sound(constants.SHOT_SOUND))
    #         return True
    #     return False