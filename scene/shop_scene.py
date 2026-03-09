import pygame
from mygame_RPG.entities import player_items
from mygame_RPG.entities.player_items import create_default_items
from mygame_RPG.entities.player_items import HealingItem
from mygame_RPG.entities.player_items import ManaItem
from mygame_RPG.entities.player_items import StatBoostItem


class ShopScene:
    def __init__(self,player_state):
        # 玩家状态引用
        self.player_state = player_state #
        # 字体
        font_path = r"C:\Windows\Fonts\simsun.ttc"
        self.title_font = pygame.font.Font(font_path,48)
        self.font = pygame.font.Font(font_path,36)
        self.small_font = pygame.font.Font(font_path,24)

        # 商品列表
        self.items = create_default_items()
        self.items_list = list(self.items.values())

