import sys
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        #Full screen
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        pygame.display.set_caption("Alien Invasion")


    def run_game(self):

        while True:
            '''Monitor the keyboard and mouse'''
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()
            self._update_screen()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_fleet_bottom()

    def _update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _check_bullet_alien_collisions(self):
        # Destroy the alien and bullets when collide
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, self.settings.bullets_disappeared, True)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)
        available_alien_number = available_space_x // (2 * alien_width)
        for row_number in range(number_rows):
            for alien_number in range(available_alien_number):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.rect.x = alien.x

        self.aliens.add(alien)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_fleet_edges(self):
        # Check if the alien reach the left/right edge of the screen
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_fleet_bottom(self):
        # Check if the alien reach the bottom of the screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1


    def _check_keydown_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.move = self.settings.ship_speed
        elif event.key == pygame.K_LEFT:
            self.ship.move = -1 * self.settings.ship_speed
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        # React when ship got hit
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_keyup_event(self, event):
        self.ship.move = 0

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()

    test_mod = input("Testing mod? Y/N")
    if test_mod == 'Y':
        ai.settings.bullet_width = 500
        ai.settings.bullets_disappeared = False

    ai.run_game()
