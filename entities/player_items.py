import pygame
class Item:
    """基础物品类"""
    def __init__(self,name,description,price,icon_path = None): # 定义类的构造方法，初始化物品的公共属性
        self.name = name
        self.description = description # 物品描述
        self.price = price # 物品价格
        self.icon = None # 图标，用None占位
        if icon_path:
            try:
                self.icon = pygame.image.load(icon_path).convert_alpha()
                self.icon = pygame.transform.scale(self.icon, (40, 40))
            except:
                print(f"无法加载图标：{icon_path}")

class HealingItem(Item):
    """治疗物品"""
    def __init__(self,name,description,price,heal_amount,icon_path = None): # 定义子类的构造方法，初始化子类的专属属性
        super().__init__(name,description,price,icon_path) # 调用父类方法 super调用父类
        self.heal_amount = heal_amount # 将传入的治疗量绑定为该子类的专属实例属性

    def use(self,player_hp,player_max_hp = 100): # 定义物品的使用方法
        new_hp = min(player_hp + self.heal_amount,player_max_hp) # 玩家血量+使用道具血量，最大不超过玩家最大血量
        return new_hp # 返回新代码

class ManaItem(Item):
    """魔法物品"""
    def __init__(self,name,description,price,mana_amount,icon_path = None): # 定义子类的构造方法
        super().__init__(name.name, description, price, icon_path) # 调用父类的定义
        self.mana_amount = mana_amount # mp回复量

    def use(self,player_mp,player_max_mp = 100): #
        new_mp = min(player_mp + self.mana_amount,player_max_mp)
        return new_mp
    
class StatBoostItem(Item):
    """属性增强物品"""
    def __init__(self,name,description,price,stat_type,boost_amount,icon_path = None):
        super().__init__(name, description, price, icon_path)
        self.stat_type = stat_type # "attack","defense","max_hp","max_mp" 增强的属性类型
        self.boost_amount = boost_amount

    def use(self,current_value): # current_value该属性的当前数值
        return current_value + self.boost_amount # 返回增强后的属性值

def create_default_items():
    items = {
        "health_potion" : HealingItem(
            name = "简易生命药水",
            description = "可以回复30点血量，很实惠，也很好用",
            price = 20,
            heal_amount = 30,
            icon_path=None,
        ),
        "mana_potion" : ManaItem(
            name = "简易魔力药水",
            description = "可以回复30点魔力值，很实惠，也很好用",
            price = 20,
            mana_amount = 30,
            icon_path = None
        ),
        "attack_boost" : StatBoostItem(
            name = "力量药水",
            description = f"可以在本次战斗中提升5点战斗",
            price = 50,
            stat_type = "attack",
            boost_amount = 5,
            icon_path = None,
        ),
        "max_hp_boots" : StatBoostItem(
            name = "生命精华",
            description = "永久性的提升10点生命值上限，是珍品中的珍品",
            price = 100,
            stat_type = "max_hp",
            boost_amount= 10,
            icon_path = None
        ),
        "max_mp_boots" : StatBoostItem(
            name = "魔力花",
            description = "永久提升10点魔力上限，是珍品中的珍品",
            price = 100,
            stat_type = "max_mp",
            boost_amount = 10,
            icon_path = None
        ),
        "defense_boost" : StatBoostItem(
            name = "铁皮药水",
            description = "本次战斗提升3点的防御力",
            price = 50,
            stat_type = "defense",
            boost_amount = 3,
            icon_path = None
        )
    }
    return items




