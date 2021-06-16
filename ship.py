import pygame

class Ship:

    def __init__(self, ai_game):
        '''Initialize the ship and it's position'''
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        '''Load the ship's shape and rect'''
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.move = 0
        self.speed = 2
        self.x = float(self.rect.x)

        '''To make the ship responds at the mid bottom of the screen'''
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        '''Draw the ship'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''Update ship's position'''
        if (self.move < 0 and self.rect.left - self.move >= 0) or (self.move > 0 and self.rect.right + self.move <= self.screen_rect.right):
            self.x += self.move
        self.rect.x = self.x

    def center_ship(self):
        # move the ship to the center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x - float(self.rect.x)
