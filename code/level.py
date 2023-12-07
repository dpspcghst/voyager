from random import choice, randint
import pygame
# from debug import debug
from enemy import Enemy
from magic import MagicPlayer
from particles import AnimationPlayer
from player import Player
from setting import TILESIZE
from support import import_csv_layout, import_folder
from tile import Tile
from ui import UI
from weapon import Weapon

class Level():
    """
    Class representing a game level.
    """

    def __init__(self):
        """
        Initialize the level class.
        """

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        if self.display_surface is None:

            # Error handling if the display surface is not initialized
            print("Error: Display surface not initialized.")

            return
        
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        """
        Create the game map based on layouts and graphics.
        """

        layouts = {
            "boundary": import_csv_layout("map/map_FloorBlocks.csv"),
            "entities": import_csv_layout("map/map_Entities.csv"),
            "grass": import_csv_layout("map/map_Grass.csv"),
            "object": import_csv_layout("map/map_Objects.csv")
        }

        graphics = {
            "grass": import_folder("graphics/grass"),
            "objects": import_folder("graphics/objects")
        }

        for style, layout in layouts.items():

            for row_index, row in enumerate(layout):
    
                for col_index, col in enumerate(row):

                    if col != "-1":
    
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                    
                        if style == "boundary":

                            Tile(
                                (x, y),
                                [self.obstacle_sprites],
                                "invisible",
                                surface=pygame.Surface(
                                    (TILESIZE, TILESIZE)
                                )
                            )

                        if style == "entities":

                            if col == "394":

                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                )

                            else:

                                if col == "390":

                                    monster_name = "bamboo"

                                elif col == "391":

                                    monster_name = "spirit"

                                elif col == "392":

                                    monster_name = "raccoon"

                                else:
                                    monster_name = "squid"

                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [
                                        self.visible_sprites,
                                        self.attackable_sprites
                                    ],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles
                                )
                        
                        if style == "grass":

                            grass_image = choice(graphics["grass"])
                            Tile(
                                (x, y),
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites
                                ],
                                "grass",
                                grass_image
                            )

                        if style == "object":

                            surf = graphics["objects"][int(col)]
                            Tile(
                                (x, y),
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites
                                ],
                                "objects",
                                surf
                            )

    def create_attack(self):
        """
        Create an attack for the player.
        """

        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites]
        )

    def create_magic(self, style, strength, cost):

        if style == "heal":

            self.magic_player.heal(
                self.player, strength, cost, [self.visible_sprites]
            )

        if style == "flame":

            self.magic_player.flame(
                self.player, cost,
                [self.visible_sprites, self.attack_sprites]
            )

    def destroy_attack(self):
        """
        Destroy the current attack.
        """

        if self.current_attack:

            self.current_attack.kill()
        self.current_attack = None
    
    def player_attack_logic(self):

        if self.attack_sprites:

            for attack_sprite in self.attack_sprites:

                remove_sprite = False
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites,
                    remove_sprite
                )

                if collision_sprites:

                    for target_sprite in collision_sprites:

                        if target_sprite.sprite_type == "grass":

                            pos = target_sprite.rect.center
                            x_vector_coordinate = 0
                            y_vector_coordinate = 75
                            offset = pygame.math.Vector2(
                                x_vector_coordinate,
                                y_vector_coordinate
                            )

                            for leaf in range(randint(3, 6)):

                                self.animation_player.create_grass_particles(
                                    pos - offset,
                                    [self.visible_sprites]
                                )
                            target_sprite.kill()

                        else:
                            
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type
                            )
    
    def damage_player(self, amount, attack_type):

        if self.player.vulnerable:

            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(
                attack_type, self.player.rect.center,
                [self.visible_sprites]
            )

    def trigger_death_particles(self, pos, particle_type):

        self.animation_player.create_particles(
            particle_type, pos, self.visible_sprites
        )

    def run(self):
        """
        Run the game loop.
        """

        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    """
    Custom sprite group for Y-sorting.
    """

    def __init__(self):
        """
        Initialize the YSortCameraGroup class.
        """

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        if self.display_surface is None:

            # Error handling if the display surface is not initialized
            print("Error: Display surface not initialized.")

            return
        
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        floor_image_path = "graphics/tilemap/ground.png"
        self.floor_surf = pygame.image.load(
            floor_image_path
        ).convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        """
        Draw sprites with Y-sorting and adjust the offset based on the
        player.
        """

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(
            self.sprites(), key=lambda sprite: sprite.rect.centery
        ):

            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):

        # long lines...
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']

        for enemy in enemy_sprites:

            enemy.enemy_update(player)
