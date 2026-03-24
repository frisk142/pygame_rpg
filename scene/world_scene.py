import random
from mygame_RPG.entities.Enemy import Enemy
import pygame
from mygame_RPG.entities.player import get_player
from mygame_RPG.entities.stair import Stair
from mygame_RPG.scene.shop_scene import ShopEntrance

class world_scene:
    def __init__ (self,floor = 1):
        self.all_sprites = pygame.sprite.Group() # 创建一个精灵组
        self.player = get_player() # 创建主角
        self.floor = floor
        self.stair = Stair(x = self.stair.x , y = self.stair.y)

        # 字体相关
        font_path = r"C:\Windows\Fonts\Deng.ttf"
        self.font = pygame.font.Font(font_path, 36)

        self.enemy = Enemy.create_enemy_by_floor(floor) # 放置敌人
        self.shop_scene = ShopEntrance(600,600)
        self.all_sprites.add(self.player) # 添加主角到精灵分类
        self.all_sprites.add(self.enemy) # 添加敌人至精灵分类

        # 商店刷新

        self.shop_entrance = None
        if floor % 5 == 0:
            self.shop_entrance = ShopEntrance(600,600)
            self.all_sprites.add(self.shop_entrance)

        self.encountered_enemy = None # 记录碰到了谁

    def update(self):  # 获取按键
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        if self.enemy and self.enemy.hp > 0:
            self.enemy.update()

        # 碰撞检测
        if pygame.sprite.collide_rect(self.player, self.enemy,):
            self.encountered_enemy = self.enemy
            if self.player.hp <= 0:
                return None
            return "to_battle"

        if self.enemy and self.enemy.hp <= 0 and self.stair is None:
            # 在随机位置附近生成楼梯入口
            self.stair = (self.stair.x,self.stair.y)
            self.all_sprites.add(self.stair)

        # 如果楼梯存在，检测碰撞
        if pygame.sprite.collide_rect(self.player, self.stair,):
            return "to_next_floor"


        if pygame.sprite.collide_rect(self.player, self.shop_scene):
            self.encountered_shop_scene = self.shop_scene
            return "to_shop"

        return None

    def handle_events(self, events):
        # 场景级别的事件处理（比如按ESC返回菜单）
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "to_menu"  # 将来可切换场景
                # 其他世界场景特有按键
        return None


    def draw(self,screen):
        screen.fill((100,100,200)) # 探索背景色
        self.all_sprites.draw(screen)

        # 显示层数
        floor_text = self.font.render(f"{self.floor}层",True,(255,255,255))
        screen.blit(floor_text,(10,10))