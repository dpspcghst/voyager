import pygame
import setting as s

class UI():

    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()

        if self.display_surface is None:

            # Error handling if the display surface is not initialized
            print("Error: Display surface not initialized.")

            return

        self.font = pygame.font.Font(s.UI_FONT_PATH, s.UI_FONT_SIZE)

        # bar setup
        left_position = 10
        top_position = 10
        self.health_bar_rect = pygame.Rect(
            left_position, top_position, s.HEALTH_BAR_WIDTH, s.BAR_HEIGHT
        )

        other_top_position = 34
        self.energy_bar_rect = pygame.Rect(
            left_position, other_top_position, s.ENERGY_BAR_WIDTH, s.BAR_HEIGHT
        )

        #convert weapon dictionary
        self.weapon_graphics = []

        for weapon in s.weapon_data.values():
            path = weapon["graphic"]
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        #convert weapon dictionary
        self.magic_graphics = []

        for magic in s.magic_data.values():
            path = magic["graphic"]
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

        self.border_line_width = 3

    def show_bar(self, current, max_amount, bg_rect, color):

        # draw bg
        pygame.draw.rect(self.display_surface, s.UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
    
        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(
            self.display_surface, s.UI_BORDER_COLOR, bg_rect, self.border_line_width
        )
    
    def show_exp(self, exp):

        text_surf = self.font.render(str(int(exp)), False, s.TEXT_COLOR)
        offset = 20
        x = self.display_surface.get_size()[0] - offset
        y = self.display_surface.get_size()[1] - offset
        text_rect = text_surf.get_rect(bottomright=(x, y))

        inflate_size = 20
        pygame.draw.rect(
            self.display_surface, s.UI_BG_COLOR,
            text_rect.inflate(inflate_size, inflate_size)
        )
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface, s.UI_BORDER_COLOR,
            text_rect.inflate(inflate_size, inflate_size), self.border_line_width
        )
    
    def selection_box(self, left, top, has_switched):

        bg_rect = pygame.Rect(left, top, s.ITEM_BOX_SIZE, s.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, s.UI_BG_COLOR, bg_rect)
        
        if has_switched:

            pygame.draw.rect(
                self.display_surface, s.UI_BORDER_COLOR_ACTIVE, bg_rect,
                self.border_line_width
            )

        else:

            pygame.draw.rect(
                self.display_surface, s.UI_BORDER_COLOR, bg_rect,
                self.border_line_width
            )

        return bg_rect
    
    def weapon_overlay(self, weapon_index, has_switched):

        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def magic_overlay(self, magic_index, has_switched):

        bg_rect = self.selection_box(80, 635, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)
    
    def display(self, player):

        self.show_bar(
            player.health, player.stats["health"], self.health_bar_rect, s.HEALTH_COLOR
        )
        self.show_bar(
            player.energy, player.stats["energy"], self.energy_bar_rect, s.ENERGY_COLOR
        )

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
