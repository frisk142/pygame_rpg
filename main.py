import pygame
import sys
from mygame_RPG.scene.world_scene import world_scene
from mygame_RPG.scene.battle_scene import Battle_scene

def main():
    pygame.init() # 初始化
    screen = pygame.display.set_mode((800, 800)) # 创建一个800，800大小的窗口
    clock = pygame.time.Clock() # 时间和电脑时间绑定，创建时钟对象

    # 初始状态：探索场景
    current_scene = world_scene() # 创建探索场景实例，赋值当前场景

    running = True
    while running:

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False

        current_scene.handle_events(events) # 将收集到的事情传给当前场景处理
        next_scene_request = current_scene.update() # 更新当前场景逻辑，获取场景切换请求


        # 处理场景切换请求
        if next_scene_request == "to_battle":
            if isinstance(current_scene,world_scene): # 获取探索场景遇到的敌人，并转递给战斗场景
                current_scene = Battle_scene(current_scene.encountered_enemy)
        elif next_scene_request == "to_world":
            if isinstance(current_scene,Battle_scene):
                current_scene = world_scene()



        current_scene.draw(screen) # 绘制当前场景
        pygame.display.flip() # 刷新屏幕
        clock.tick(60) # 限制60帧

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()