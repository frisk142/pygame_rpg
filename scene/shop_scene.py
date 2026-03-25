import pygame
from mygame_RPG.entities.player_items import create_default_items


class ShopEntrance(pygame.sprite.Sprite): # 商店入口，创建商店精灵类
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((60,60))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


class ShopScene:
    def __init__(self,player):
        # 玩家状态引用
        self.player = player
        # 字体
        font_path = r"C:\Windows\Fonts\simsun.ttc"
        self.title_font = pygame.font.Font(font_path,48)
        self.font = pygame.font.Font(font_path,36)
        self.small_font = pygame.font.Font(font_path,24)
        # 商品列表
        self.items = create_default_items()
        self.items_list = list(self.items.values())
        self.selected_index = 0 # 选中当前商品索引

        self.pending_scene_instruction = None

    # draw绘制商店界面
    def draw(self,screen):
        screen.fill((0,0,0)) # 背景

        title = self.title_font.render("商店",True,(255,210,0)) # 标题
        screen.blit(title,(300,50))

        glod_txt = self.font.render(f"金币{self.player.gold}",True,(255,255,0))
        screen.blit(glod_txt,(50,120))

        # 商品列表
        for i , item in enumerate(self.items_list):
            y = 200 + i * 70 # 每个商品都占70像素高度
            color = (255,255,255)if i != self.selected_index else (255,215,0)
            prefix = ">" if i == self.selected_index else ""

            # 显示名称和价格
            name_text = self.font.render(f"{prefix} {item.name} - {item.price}金币",True,color)
            screen.blit(name_text,(50,y))

            # 显示名字
            desc_text = self.small_font.render(item.description,True , (200,200,200))
            screen.blit(desc_text,(80,y + 30))

    # 按键事件处理
    def handle_events(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len (self.items_list)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len (self.items_list)
                elif event.key == pygame.K_RETURN:
                    self.buy_item()
                elif event.key == pygame.K_ESCAPE:
                   self.pending_scene_instruction = "to_world"  # 按 ESC 返回世界场景

        return None

    # 购买物品处理
    def buy_item(self):
        item = self.items_list[self.selected_index]
        if self.player.gold >= item.price:
            self.player.gold -= item.price

            # 把物品副本添加到背包

            self.player.inventory.append(item)
            print(f"购买成功！获得了{item.name}")

        else :
            print("金币不足")

    # update传递数据给main
    def update(self):
        if self.pending_scene_instruction:
            instruction = self.pending_scene_instruction
            self.pending_scene_instruction = None
            return instruction
        return None







