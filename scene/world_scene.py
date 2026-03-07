import pygame
from mygame_RPG.entities.player import Player
from mygame_RPG.entities.Enemy import Enemy

class world_scene:
    def __init__ (self):
        self.all_sprites = pygame.sprite.Group() # 创建一个精灵组
        self.player = Player(400,400) # 创建主角
        self.all_sprites.add(self.player) # 添加主角到精灵分类

        self.enemy = Enemy(200,200) # 放置敌人
        self.all_sprites.add(self.enemy) # 添加敌人至精灵分类

        self.encountered_enemy = None # 记录碰到了谁

    def update(self):  # 获取按键
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.enemy.update()

        # 碰撞检测

        if pygame.sprite.collide_rect(self.player, self.enemy):
            self.encountered_enemy = self.enemy
            return "to_battle"
        return None

    def draw(self,screen):
        screen.fill((100,100,200)) # 探索背景色
        self.all_sprites.draw(screen)

    def handle_events(self, events):
        """专门处理按键按下/释放等离散事件"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("主角跳跃！")
                elif event.key == pygame.K_ESCAPE:
                    return "to_menu"  # 可以返回其他场景切换指令
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    print("停止跳跃")