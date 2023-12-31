from random import randint

import pygame

from setting import TILESIZE

class MagicPlayer():

    def __init__(self, animation_player):

        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):

        if player.energy >= cost:

            player.health += strength
            player.energy -= cost

            if player.health >= player.stats["health"]:

                player.health = player.stats["health"]

            self.animation_player.create_particles(
                "aura", player.rect.center, groups
            )
            self.animation_player.create_particles(
                "heal", player.rect.center, groups
            )

    def flame(self, player, cost, groups):

        if player.energy >= cost:

            player.energy -= cost

            if player.status.split("_")[0] == "down":

                direction = pygame.math.Vector2(0, 1)

            elif player.status.split("_")[0] == "left":

                direction = pygame.math.Vector2(-1, 0)

            elif player.status.split("_")[0] == "right":

                direction = pygame.math.Vector2(1, 0)

            else:

                # up
                direction = pygame.math.Vector2(0, -1)

            for i in range(1, 6):

                if direction.x: #horizontal

                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x
                    new_x = x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery
                    self.animation_player.create_particles(
                        "flame", (new_x, y), groups
                    )

                else: #vertical

                    pass
