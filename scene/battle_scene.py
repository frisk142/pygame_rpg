import pygame
import random
from mygame_RPG.entities.player import get_player
from mygame_RPG.entities.Enemy import create_enemy
from mygame_RPG.data.skill_data import SKILLS


class \
        Battle_scene:
    def __init__(self,encountered_enemy):
        self.enemy = create_enemy() # 怪物信息
        self.player = get_player()

        self.display_player_hp = self.player.hp # 用于显示缓降落的ui条
        self.display_enemy_hp = self.enemy.hp
        self.display_player_mp = self.player.mp

        # 战斗内部状态机
        self.battle_state = "PLAYER_TURN" # 初始为玩家回合
        font_path = r"C:\Windows\Fonts\Deng.ttf"
        self.font = pygame.font.Font(font_path, 36)

        # 菜单相关
        self.menu_options = ["攻击","技能","防御","逃跑","道具"]
        self.skills_menu = list(SKILLS.keys())


        self.selected_index = 0 # 主菜单当前选中索引,
        self.skills_index = 0 # 技能子菜单当前选中索引
        self.items_index = 0 # 道具子菜单索引

        # 道具相关
        self.usable_items = [] # 当前可用的物品列表
        self.refresh_usable_items() # 初始化可用物品

        self.last_action = None # 储存玩家最后选择的行动
        self.current_menu = "MAIN" # 跟踪当前菜单
        self.damage_state = "NONE"


        # 计时器
        self.enemy_turn_start_time = 0
        self.enemy_turn_delay = 1000 # 敌人回合延迟

        self.damage_display_delay = 500 # 伤害显示延迟


        self.pending_scene_instruction = None # 待处理的场景切换
        # 对话框系统
        self.dialog_messages = [] # 创建列表储存要显示的消息
        self.max_dialog_lines = 4 # 最大显示行数
        self.dialog_font =  pygame.font.Font(font_path, 24) # 对话框字体
        # 初始战斗消息
        self.add_dialog_message(f"遇到了{self.enemy.name}!")
        self.add_dialog_message("战斗开始！")

        # 战斗结束标记
        self.battle_ended = False

        # 创建金币奖励
        self.display_Gold_coins = self.player.gold # 用于显示的金币


    def add_dialog_message(self,message):
        """添加消息至对话框"""
        self.dialog_messages.append(message)
         # 至保留最近的消息
        if len(self.dialog_messages) > self.max_dialog_lines:
            self.dialog_messages.pop(0)


    def handle_events(self,events):
        """菜单动作执行"""
        for event in events: # 遍历所有事件
            if event.type == pygame.KEYDOWN: # 如果是按键按下事件
                if self.battle_state == "PLAYER_TURN": # 只在玩家回合内处理事件
                    if self.current_menu == "MAIN":
                        if event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % len(self.menu_options) # 循环体向上选择
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % len(self.menu_options) # 循环体向下选择
                        elif event.key == pygame.K_RETURN:
                            action_result = self.execute_player_action()
                            self.last_action = self.menu_options[self.selected_index]
                            if action_result:
                                self.pending_scene_instruction = action_result

                    elif self.current_menu == "SKILLS":
                        if event.key == pygame.K_UP:
                            self.skills_index =  (self.skills_index - 1) % len (self.skills_menu)
                        elif event.key == pygame.K_DOWN:
                            self.skills_index = (self.skills_index + 1 ) % len(self.skills_menu)
                        elif event.key == pygame.K_RETURN:
                            self.use_selected_skill()
                        elif event.key == pygame.K_ESCAPE:
                            self.current_menu = "MAIN"
                        elif event.key == pygame.K_SPACE:
                            self.battle_state = "ENEMY_TURN" if self.battle_state == "PLAYER_TURN" else "PLAYER_TURN"
                            print(f"调试：切换状态到{self.battle_state}")

                    elif self.current_menu == "ITEMS":
                        if event.key == pygame.K_UP:
                            self.items_index =  (self.items_index - 1) % len (self.usable_items)
                        elif event.key == pygame.K_DOWN:
                            self.items_index = (self.items_index + 1 ) % len(self.usable_items)
                        elif event.key == pygame.K_RETURN:
                            self.use_selected_item()
                        elif event.key == pygame.K_ESCAPE:
                            self.current_menu = "MAIN"
                        elif event.key == pygame.K_SPACE:
                            self.battle_state = "ENEMY_TURN" if self.battle_state == "PLAYER_TURN" else "PLAYER_TURN"
                            print(f"调试：切换状态到{self.battle_state}")


                elif self.battle_state in ["VICTORY","DEFEAT"]:
                    if event.key == pygame.K_RETURN:
                        self.pending_scene_instruction = "to_world"


    def execute_player_action(self):
        """执行玩家选择的行动"""
        action = self.menu_options[self.selected_index]
        print(f"玩家选择了{action}")

        if action == "攻击": # 简单的伤害计算
            damage = 20
            self.enemy.hp -= damage
            print(f"对敌人造成了{damage}点伤害！，敌人剩余hp{self.enemy.hp}")
            self.add_dialog_message(f"对敌人造成了{damage}点伤害！，敌人剩余hp{max(self.enemy.hp,0)}")
            self.enemy.hp = max(self.enemy.hp,0)
            self.damage_state = "PLAYER_DAMAGE"
            self.damage_display_timer = pygame.time.get_ticks()
            self.battle_state = "ENEMY_TURN"

            # 玩家行动后，切换到敌人回合
            # entities.battle_state = "ENEMY_TURN"

        if action == "防御":
            print(f"玩家选择了防御！极大的降低了敌人的伤害！")
            self.battle_state = "ENEMY_TURN"

        if action == "逃跑":
            escape_chance = 0.7
            if random.random() < escape_chance:
                print("已给路哒哟！！！逃跑成功")
                return "to_world"
            else:
                print("逃跑失败！！！！敌人缠上来了")
                self.battle_state = "PLAYER_TURN"

        if action == "技能":
            print("玩家选择了技能")
            self.current_menu = "SKILLS"
            self.skills_index = 0 # 重置技能默认选择第一个

        if action == "道具":
            print("玩家选择了道具")
            self.current_menu = "ITEMS"
            self.selected_index = 0
            self.refresh_usable_items()

        return None



    def use_selected_skill(self):
        """使用选中的技能"""
        skill_name = self.skills_menu[self.skills_index]
        skill = SKILLS.get(skill_name) # 从data文件获取技能对象
        if skill is None:
            self.add_dialog_message(f"错误：没找不到技能{skill_name}")
            return
        # 检测mp是否不足
        if not skill.can_use(self.player):
            self.add_dialog_message("MP不足")
            return
        # 使用技能，得到返回值
        success,msg = skill.use(self.player,self.enemy)
        self.add_dialog_message(msg)
        # 更新伤害显示状态
        self.damage_state = "PLAYER_DAMAGE"
        self.damage_display_timer = pygame.time.get_ticks()
        self.battle_state = "ENEMY_TURN"


    def refresh_usable_items(self):   # 从玩家背包中筛选出可用的物品
        """从玩家包里筛选出需要的道具"""
        self.usable_items = self.player.inventory[:]
        if not self.usable_items:  # if是为了确保是列表
            self.usable_items = []

    def use_selected_item(self):
        if not self.usable_items:
            self.add_dialog_message ("没有可用物品")
            self.current_menu = "MAIN"  # 如果背包没有可用物品的话就返回主菜单选项
            return

        item = self.usable_items[self.selected_index]
        msg =  item.use(self.player) #  物品use方法定义时我们改成了接收玩家实例并返回消息
        self.add_dialog_message(msg) # 物品使用后可能从背包移除，但是usable_items 列表需要同步更新
        # 因为usable_items 是引用 player.inventory 所以同步，但是需要重新索引
        self.refresh_usable_items() # 调整索引防止过界
        

    def update(self):
        """根据战斗状态更新逻辑"""
        if self.pending_scene_instruction:
            instruction = self.pending_scene_instruction
            self.pending_scene_instruction = None
            return instruction

        scene_instruction = None

        """血条缓降逻辑"""
        # 血条缓降逻辑（现在根据damage_state决定先降哪个）

            # 只降敌人血条（玩家造成的伤害）
        if self.display_enemy_hp > self.enemy.hp:
            self.display_enemy_hp -= int(max(1, (self.display_enemy_hp - self.enemy.hp) * 0.2))
        if self.display_player_hp > self.player.hp:
            self.display_player_hp -= int(max(1, (self.display_player_hp - self.player.hp) * 0.2))

            # 只降玩家血条（敌人造成的伤害）
        if self.display_player_hp > self.player.hp:
            self.display_player_hp -= int(max(1, (self.display_player_hp - self.player.hp) * 0.2))
        if self.display_enemy_hp > self.enemy.hp:
            self.display_enemy_hp -= int(max(1, (self.display_enemy_hp - self.enemy.hp) * 0.2))

            # 没有伤害显示时，可以同时缓降
        if self.display_player_hp > self.player.hp:
            self.display_player_hp -= int(max(1, (self.display_player_hp - self.player.hp) * 0.2))
        elif self.display_player_hp < self.player.hp:
            self.display_player_hp += int(max(1, (self.player.hp - self.display_player_hp) * 0.2))

        # MP条缓降（一直进行）
        if self.display_player_mp > self.player.mp:
           self.display_player_mp -= int(max(1, (self.display_player_mp - self.player.mp) * 0.2))

        # 胜负判断
        if not self.battle_ended:
            if self.enemy.hp <= 0 :
                self.battle_state = "VICTORY"
                self.battle_ended = True
                self.player.gold += self.enemy.gold
                print(f"战斗胜利！ 获得了{self.enemy.gold}金币")
                self.add_dialog_message(f"获得了{self.enemy.gold}个金币")
                self.add_dialog_message("战斗胜利\n点击回车返回主世界")
                return "VICTORY_to_world"



            elif self.player.hp <= 0 :
                self.battle_state = "DEFEAT"
                self.battle_ended = True
                print("战斗失败...\n胜败乃兵家常事，少侠请重新来过")
                self.add_dialog_message("战斗失败...胜败乃兵家常事，少侠请重新来过")
                self.add_dialog_message("点击回车返回主世界")

        # 处理伤害显示状态
        if self.battle_ended:
            return None
        if self.damage_state != "NONE":
            current_time = pygame.time.get_ticks()

            if current_time - self.damage_display_timer >= self.damage_display_delay:
                if self.damage_state == "PLAYER_DAMAGE":
                    self.battle_state = "ENEMY_TURN"
                    self.damage_state = "NONE"
                elif self.damage_state == "self.enemy.damage":
                    self.battle_state ="PLAYER_TURN"
                    self.last_action = None
                    self.damage_state = "NONE"


        if not self.battle_ended and self.battle_state == "ENEMY_TURN" and self.damage_state == "NONE":
            if self.enemy_turn_start_time == 0: # 敌人回合开始计算事件
                self.enemy_turn_start_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.enemy_turn_start_time
            if elapsed_time >= self.enemy_turn_delay:
                self.add_dialog_message("敌人回合开始")
                if self.last_action == "防御":
                    self.enemy.damage = int(self.enemy.damage * 0.5)
                self.player.hp -= self.enemy.damage
                self.add_dialog_message(f"敌人对你造成了{self.enemy.damage}点伤害，玩家剩余hp为{max(0,self.player.hp)}")

                self.enemy_turn_start_time = 0

                # 敌人回合结束后切换为玩家回合
                # entities.battle_state = "PLAYER_TURN"
                self.damage_state = "self.enemy.damage"
                self.damage_display_timer = pygame.time.get_ticks()
                # entities.last_action = None


    def draw_dialog_box(self,screen):
        """绘制对话框"""
        # 对话框的位置和大小
        dialog_width = 600
        dialog_height = 175
        dialog_x = 175
        dialog_y = 600

        # 绘制对话框背景
        pygame.draw.rect(screen, (0, 0, 0), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(screen, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        # 绘制消息
        for i ,message in enumerate(self.dialog_messages):
            text = self.dialog_font.render(message,True,(255,255,255))
            screen.blit(text,(dialog_x + 10,dialog_y + 10 + i * 30))


    def draw(self,screen):

        screen.fill((30,20,40))

        player_text = self.font.render(f"玩家 HP：{max(0,int(self.display_player_hp))}",True,(255,255,255))
        enemy_text = self.font.render(f"敌人 HP：{int(self.display_enemy_hp)}",True,(255,255,255))
        player_enemy_txt = self.font.render(f"玩家 MP：{int(self.display_player_mp)}",True,(255,255,255))
        screen.blit(player_text,(50,50))
        screen.blit(enemy_text,(500,50))
        screen.blit(player_enemy_txt,(50,150))

        # 绘制血条ui
        # 玩家血条位置
        bar_width = 200
        bar_height = 20
        bar_x = 50
        bar_y = 100
        # 玩家血条位置与绘制
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height)) # 绘制红色背景条，代表已经损失的血量
        current_width = (self.display_player_hp / 100) * bar_width # 绿色血量条
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # 敌人血条ui
        # 敌人血条位置
        enemy_bar_width = 200
        enemy_bar_height = 20
        enemy_bar_x = 500
        enemy_bar_y = 100
        # 敌人血条位置与绘制
        pygame.draw.rect(screen, (255, 0, 0), (enemy_bar_x, enemy_bar_y, enemy_bar_width, enemy_bar_height))
        enemy_current_width = (self.display_enemy_hp / self.enemy.max_hp) * enemy_bar_width
        pygame.draw.rect(screen, (0, 255, 0), (enemy_bar_x, enemy_bar_y, enemy_current_width, enemy_bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (enemy_bar_x, enemy_bar_y, enemy_bar_width, enemy_bar_height), 2)

        # 玩家蓝条ui
        player_energy_width = 200
        player_energy_height = 20
        player_energy_x = 50
        player_energy_y = 130
        # 玩家蓝条位置与绘制
        pygame.draw.rect(screen, (0, 255, 128), (player_energy_x, player_energy_y, player_energy_width, player_energy_height))
        energy_current_width = (self.display_player_mp / 100) * player_energy_width
        pygame.draw.rect(screen, (0, 255, 255), (player_energy_x, player_energy_y, energy_current_width, player_energy_height))
        pygame.draw.rect(screen, (255, 255, 255), (player_energy_x, player_energy_y, player_energy_width, player_energy_height), 2)

        # 战斗菜单（玩家回合显示）
        if self.battle_state == "PLAYER_TURN":
            if self.current_menu == "MAIN":
                menu_y = 575
                menu_x = 20.
                for i,option in enumerate(self.menu_options):
                    color = (255,215,0) if i == self.selected_index else (200,200,200)
                    prefix = ">" if i == self.selected_index else ""
                    option_text = self.font.render(f"{prefix},{option}",True,color)
                    screen.blit(option_text,(menu_x,menu_y + i * 40))
            elif self.current_menu == "SKILLS":
                menu_y = 575.
                menu_x = 20.
                for i, option in enumerate(self.skills_menu):
                    color = (255, 215, 0) if i == self.skills_index else (200, 200, 200)
                    prefix = ">" if i == self.skills_index else ""
                    option_text = self.font.render(f"{prefix},{option}", True, color)
                    screen.blit(option_text, (menu_x, menu_y + i * 40))
            elif self.current_menu == "ITEMS":
                menu_y = 575
                menu_x = 20
                for i , item in enumerate(self.usable_items):
                    color = (255,215,0) if  i == self.items_index else (200, 200, 200)
                    prefix = ">" if i == self.items_index else ""
                    item_text = self.font.render(f"{prefix},{item.name}", True, color)
                    screen.blit(item_text, (menu_x, menu_y + i * 40))
                    if not self.usable_items:
                        empty_text = self.font.render(("没有可用物品"),True,(255,255,255))
                        screen.blit(empty_text,(menu_x, menu_y))


                # 绘制当前战斗显示
        # state_text = entities.font.render(f"状态：{entities.battle_state}",True,(150,250,150))
        # screen.blit(state_text,(300,200))

        self.draw_dialog_box(screen)


