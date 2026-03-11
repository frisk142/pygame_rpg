import random
import pygame

# 主世界怪物代码
class Enemy (pygame.sprite.Sprite): # 定义一个名为Enemy的类别，继承自pygame.sprite.Sprite基类
    def __init__ (self,x,y): # 类的构造，
        super().__init__() # 调用父类，父类的初始化

        self.name = "堕落骑士"
        # 外观
        self.original = pygame.image.load(r"C:\pycharm\pycharm project\mygame_RPG\assets\images\Enemy.png").convert_alpha() # 加载图片
        self.image = pygame.transform.scale(self.original, (60, 60)) # 限制图片大小
        self.rect = self.image.get_rect() # 创建rect类型
        self.rect.center = (x,y)

        # 属性
        self.speed = random.choice([-2,-1,1,2]) # 随机一个初始移动方向
        self.screen_Width = 800
        self.screem_height = 800

        # 战斗系统重要数据
        self.hp = 80
        self.max_hp = 80
        self.mp = 50
        self.max_mp = 50
        self.gold = int(random.randint(10, 30))
        self.damage = 20


    def update(self):
        """敌人的ai：简单的左右移动，摸到边界反弹"""
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= self.screen_Width:
            self.speed = -self.speed # 反向
        self.rect.y += random.choice([-1,0,1])

enemy_instance = None
def create_enemy(x = random.randint(0,800),y = random.randint(0,800)):
    global enemy_instance
    enemy_instance = Enemy(x,y)
    return enemy_instance

def get_Enemy():
    return enemy_instance



