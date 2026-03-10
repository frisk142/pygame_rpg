import pygame
class Player(pygame.sprite.Sprite): # 定义一个名为player的自定义类，括号内内容为，可以继承pygame内置的精灵基类
    """玩家角色类"""
    def __init__(self,x,y): # 初始化玩家示例时传入的参数
        super().__init__()
        self.original_image = pygame.image.load(r"C:\pycharm\pycharm project\mygame_RPG\assets\images\player.png").convert_alpha() # 主角图片的加载
        self.image = pygame.transform.scale(self.original_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # 自定义属性
        self.speed = 5
        self.screen_width = 800
        self.screen_height = 800

        # 关键玩家属性
        self.gold = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 100
        self.max_mp = 100
        self.attack = 10
        self.defense = 10
        self.items = []

    def update(self,keys):
        # 角色运动逻辑
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        # 边界限制逻辑
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

player_instance = None
def create_player(x = 400,y = 400):
    global player_instance
    player_instance = Player(x,y)
    return player_instance

def get_player():
    return player_instance