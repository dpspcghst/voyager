import pygame
from entity import Entity
from settings import magic_data, weapon_data
from support import import_folder


class Player(Entity):
    
    def __init__(
        self, pos, groups, obstacle_sprites, create_attack, destroy_attack,
        create_magic
    ):

        super().__init__(groups)

        player_image_path = "graphics/test/player.png"
        self.image = pygame.image.load(player_image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_player_assets()
        self.status = "down"

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {
            "attack": 10, "energy": 60, "health": 100, "magic": 4, "speed": 5
        }
        self.energy = self.stats["energy"]
        self.exp = 123
        self.health = self.stats["health"]
        self.speed = self.stats["speed"]

    def import_player_assets(self):

        character_path = "graphics/player/"
        self.animations = {
            "down": [], "down_attack": [], "down_idle": [], "left": [],
            "left_attack": [], "left_idle": [], "right": [], "right_attack": [],
            "right_idle": [], "up": [], "up_attack": [], "up_idle": []
        }

        for animation in self.animations.keys():

            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):

        if not self.attacking:

            keys = pygame.key.get_pressed()

            # movement input
            
            if keys[pygame.K_DOWN]:

                self.direction.y = 1
                self.status = "down"

            elif keys[pygame.K_UP]:

                self.direction.y = -1
                self.status = "up"

            else:

                self.direction.y = 0

            if keys[pygame.K_LEFT]:

                self.direction.x = -1
                self.status = "left"

            elif keys[pygame.K_RIGHT]:

                self.direction.x = 1
                self.status = "right"

            else:

                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:

                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            # magic input
            if keys[pygame.K_LCTRL]:

                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                shortening = list(magic_data.values())[self.magic_index]
                strength = shortening["strength"] + self.stats["magic"]
                cost = shortening["cost"]
                self.create_magic(style, strength, cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    
                    self.weapon_index += 1

                else:

                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:

                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
    
                if self.magic_index < len(list(magic_data.keys())) - 1:
    
                    self.magic_index += 1
    
                else:
    
                    self.magic_index = 0
    
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            
            if "idle" not in self.status and "attack" not in self.status:
                
                self.status = self.status + "_idle"
        
        if self.attacking:

            self.direction.x = 0
            self.direction.y = 0

            if "attack" not in self.status:

                if "idle" in self.status:

                    # overwrite idle
                    self.status = self.status.replace("_idle", "_attack")

                else:
                    self.status = self.status + "_attack"
        
        else:

            if "attack" in self.status:
                
                self.status = self.status.replace("_attack", "")
    
    def cooldowns(self):

        current_time = pygame.time.get_ticks()

        if self.attacking:

            total_cooldown = self.attack_cooldown + weapon_data[self.weapon]["cooldown"]

            if current_time - self.attack_time >= total_cooldown:

                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:

            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:

            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
    
    def animate(self):

        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
    
    def get_full_weapon_damage(self):

        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]

        return base_damage + weapon_damage
    
    def update(self):

        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
