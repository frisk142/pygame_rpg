import pygame
import random
class Stair(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((40,40)) # 创建一个40，40大小的方块
        self.image.fill((139,69,19)) # 棕色
        self.rect = self.image.get_rect(center = (x,y))
        self.x = random.randint(0,800)
        self.y = random.randint(0,800)