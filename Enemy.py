from abc import ABC, abstractmethod
from entity import Entity

class Enemy(Entity, ABC):
    """
        An abstract class to be implemented to represent all kinds of elements to
        be displayed on the game's screen
        """
    def __init__(self, x, y, health=100, damage=20, img=None):
        super().__init__(img, x, y)
        pass

    @abstractmethod
    def _load_frames(self, num_frames, num_movement):
        """load animation frames"""

    @abstractmethod
    def _dead_animation(self, screen, camera):
        """run dead animation"""

    @abstractmethod
    def _walk_animation(self):
        """run walk animation"""

    @abstractmethod
    def _atk_animation(self, screen, camera):
        """run attack animation"""

    @abstractmethod
    def move(self, player, enemies):
        """enemy moving to player"""

    @abstractmethod
    def _avoid_others(self, enemies):
        """avoid other enemies"""

    @abstractmethod
    def get_damage(self, bullet, damage):
        """get shot by a bullet"""

    @abstractmethod
    def check_alive(self):
        """check that enemy is alive or not"""

    @abstractmethod
    def hit_player(self, player):
        """check that enemy hit player or not"""

    @abstractmethod
    def draw(self, screen, camera):
        """draw this enemy and apply to camera"""

    @abstractmethod
    def get_size(self):
        """get size of image"""

