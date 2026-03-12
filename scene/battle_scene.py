import pygame
import random
from mygame_RPG.entities.player_items import Item
from mygame_RPG.entities.player import get_player
from mygame_RPG.entities.Enemy import create_enemy


class \
        Battle_scene:
    def __init__(self,encountered_enemy):
        self.enemy = get_Enemy() # 怪物信息
        self.enemy.name = "堕落骑士"
        self.player = get_player()
        self.enemy_hp = 80 # 怪物血量

        self.display_player_hp = self.player.hp # 用于显示缓降落的ui条
        self.display_enemy_hp = self.enemy_hp
        self.display_player_mp = self.player.mp

        # 战斗内部状态机
        self.battle_state = "PLAYER_TURN" # 初始为玩家回合
        font_path = r"C:\Windows\Fonts\Deng.ttf"
        self.font = pygame.font.Font(font_path, 36)

        # 菜单相关
        self.menu_options = ["攻击","技能","防御","逃跑","道具"]
        self.skills_menu = ["火球术","治疗术","闪电球","喷射火焰"]


        self.selected_index = 0 # 主菜单当前选中索引,
        self.skills_index = 0 # 子菜单当前选中索引
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
        self.enemy_Gold_coins = random.randint(10,30) # 敌人身上携带的金币
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

                elif self.battle_state in ["VICTORY","DEFEAT"]:
                    if event.key == pygame.K_RETURN:
                        self.pending_scene_instruction = "to_world"


    def execute_player_action(self):
        """执行玩家选择的行动"""
        action = self.menu_options[self.selected_index]
        print(f"玩家选择了{action}")

        if action == "攻击": # 简单的伤害计算
            damage = 20
            self.enemy_hp -= damage
            print(f"对敌人造成了{damage}点伤害！，敌人剩余hp{self.enemy_hp}")
            self.add_dialog_message(f"对敌人造成了{damage}点伤害！，敌人剩余hp{max(self.enemy_hp,0)}")
            self.enemy_hp = max(self.enemy_hp,0)
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
        return None


    def use_selected_skill(self):
        """使用选中的技能"""
        skill_name = self.skills_menu[self.skills_index]
        print(f"玩家使用了技能{skill_name}")
        self.add_dialog_message(f"使用了{skill_name}!!!")
        if self.player.mp <= 0:
            self.add_dialog_message("蓝量不够，无法使用技能")

        elif skill_name == "火球术":
            damage = 50
            player_mp = 20
            self.player.mp -= player_mp
            self.enemy_hp -= damage
            self.add_dialog_message(f"火球术造成了{damage}点伤害！敌人剩余{max(self.enemy_hp,0)}")
            print(f"现在还剩的mp： {self.player.mp}")
            self.enemy_hp = max(self.enemy_hp,0)
            self.damage_state = "PLAYER_DAMAGE"
            self.damage_display_timer =pygame.time.get_ticks()

        elif skill_name == "治疗术":
            heal_amount = 40
            player_mp = 20
            self.player.mp -= player_mp
            self.player.hp += heal_amount
            self.add_dialog_message(f"玩家使用了治疗术，回复了{heal_amount}点血量! 玩家剩余血量{max(self.player.hp,0)}")
            self.enemy_hp = max(self.enemy_hp,0)
            self.player.hp = min(self.player.hp,100)
            self.damage_state = "PLAYER_DAMAGE"
            self.damage_display_timer = pygame.time.get_ticks()

        elif skill_name == "闪电球":
            # 群体技能，放个单个伤害占位
            damage = 50
            player_mp = 40
            self.player.mp -= player_mp
            self.enemy_hp -= damage
            self.add_dialog_message(f"玩家使用了闪电球，造成了{damage}点伤害，敌人剩余血量为{max(self.enemy_hp,0)}")
            self.enemy_hp = max(self.enemy_hp, 0)
            self.damage_state = "PLAYER_DAMAGE"
            self.damage_display_timer = pygame.time.get_ticks()

        elif skill_name == "喷射火焰":
            damage = 999999
            player_damage = 0.1
            self.player.hp = int(self.player.hp * player_damage)
            self.enemy_hp -= damage
            self.add_dialog_message(f"玩家使用了喷射火焰造成了{damage}点伤害！！")
            print(f"玩家剩余血量{self.player.hp}")
            self.enemy_hp = max(self.enemy_hp, 0)
            self.damage_state = "PLAYER_DAMAGE"
            self.damage_display_timer = pygame.time.get_ticks()
        return None


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
        if self.display_enemy_hp > self.enemy_hp:
            self.display_enemy_hp -= int(max(1, (self.display_enemy_hp - self.enemy_hp) * 0.2))
        if self.display_player_hp > self.player.hp:
            self.display_player_hp -= int(max(1, (self.display_player_hp - self.player.hp) * 0.2))

            # 只降玩家血条（敌人造成的伤害）
        if self.display_player_hp > self.player.hp:
            self.display_player_hp -= int(max(1, (self.display_player_hp - self.player.hp) * 0.2))
        if self.display_enemy_hp > self.enemy_hp:
            self.display_enemy_hp -= int(max(1, (self.display_enemy_hp - self.enemy_hp) * 0.2))

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
            if self.enemy_hp <= 0 :
                self.battle_state = "VICTORY"
                self.battle_ended = True
                self.player.gold += self.enemy_Gold_coins
                print(f"战斗胜利！ 获得了{self.enemy_Gold_coins}金币")
                self.add_dialog_message(f"获得了{self.enemy_Gold_coins}个金币")
                self.add_dialog_message("战斗胜利\n点击回车返回主世界")


            elif self.player.hp <= 0 :
                self.battle_state = "DEFEAT"
                self.battle_ended = True
                print("战斗失败...\n胜败乃兵家常事，少侠请重新来过")
                self.add_dialog_message("战斗失败...\n胜败乃兵家常事，少侠请重新来过\n点击回车返回主世界")

        # 处理伤害显示状态
        if self.battle_ended:
            return None
        if self.damage_state != "NONE":
            current_time = pygame.time.get_ticks()

            if current_time - self.damage_display_timer >= self.damage_display_delay:
                if self.damage_state == "PLAYER_DAMAGE":
                    self.battle_state = "ENEMY_TURN"
                    self.damage_state = "NONE"
                elif self.damage_state == "ENEMY_DAMAGE":
                    self.battle_state ="PLAYER_TURN"
                    self.last_action = None
                    self.damage_state = "NONE"


        if not self.battle_ended and self.battle_state == "ENEMY_TURN" and self.damage_state == "NONE":
            if self.enemy_turn_start_time == 0: # 敌人回合开始计算事件
                self.enemy_turn_start_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.enemy_turn_start_time
            if elapsed_time >= self.enemy_turn_delay:
                enemy_damage = 20 # 敌人基础伤害
                self.add_dialog_message("敌人回合开始")
                if self.last_action == "防御":
                    enemy_damage = int(enemy_damage * 0.5)
                self.player.hp -= enemy_damage
                self.add_dialog_message(f"敌人对你造成了{enemy_damage}点伤害，玩家剩余hp为{self.player.hp}")

                self.enemy_turn_start_time = 0

                # 敌人回合结束后切换为玩家回合
                # entities.battle_state = "PLAYER_TURN"
                self.damage_state = "ENEMY_DAMAGE"
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

        player_text = self.font.render(f"玩家 HP：{int(self.display_player_hp)}",True,(255,255,255))
        enemy_text = self.font.render(f"敌人 HP：{int(self.display_enemy_hp)}",True,(255,255,255))
        player_enemy_txt = self.font.render(f"玩家 MP：{int(self.display_player_mp)}",True,(255,255,255))
        screen.blit(player_text,(50,50))
        screen.blit(enemy_text,(550,50))
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
        enemy_current_width = (self.display_enemy_hp / 80) * enemy_bar_width
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


                # 绘制当前战斗显示
        # state_text = entities.font.render(f"状态：{entities.battle_state}",True,(150,250,150))
        # screen.blit(state_text,(300,200))

        self.draw_dialog_box(screen)


