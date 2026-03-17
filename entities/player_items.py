import pygame
from mygame_RPG.entities.player import get_player

class Item:
    """基础物品类"""
    def __init__(self, name, description, price, icon_path=None):
        self.name = name
        self.description = description
        self.price = price
        self.icon = None
        self.player = get_player()  # 所有物品持有同一个玩家实例（全局单例）
        if icon_path:
            try:
                self.icon = pygame.image.load(icon_path).convert_alpha()
                self.icon = pygame.transform.scale(self.icon, (40, 40))
            except:
                print(f"无法加载图标：{icon_path}")

    def use(self):
        """基类use，子类应重写此方法"""
        raise NotImplementedError("子类必须实现 use 方法")


class HealingItem(Item):
    """治疗物品"""
    def __init__(self, name, description, price, heal_amount, icon_path=None):
        super().__init__(name, description, price, icon_path)
        self.heal_amount = heal_amount

    def use(self):
        self.player.hp = min(self.player.hp + self.heal_amount, self.player.max_hp)
        # 从背包移除自身
        if self in self.player.inventory:
            self.player.inventory.remove(self)
        return f"使用了{self.name}，恢复了{self.heal_amount}点生命"


class ManaItem(Item):
    """魔法物品"""
    def __init__(self, name, description, price, mana_amount, icon_path=None):
        super().__init__(name, description, price, icon_path)
        self.mana_amount = mana_amount

    def use(self):
        self.player.mp = min(self.player.mp + self.mana_amount, self.player.max_mp)
        if self in self.player.inventory:
            self.player.inventory.remove(self)
        return f"使用了{self.name}，恢复了{self.mana_amount}点魔力"


class StatBoostItem(Item):
    """属性增强物品"""
    def __init__(self, name, description, price, stat_type, boost_amount, icon_path=None):
        super().__init__(name, description, price, icon_path)
        self.stat_type = stat_type   # "attack", "defense", "max_hp", "max_mp"
        self.boost_amount = boost_amount

    def use(self):
        if self.stat_type == "attack":
            self.player.attack += self.boost_amount
        elif self.stat_type == "defense":
            self.player.defense += self.boost_amount
        elif self.stat_type == "max_hp":
            self.player.max_hp += self.boost_amount
            self.player.hp += self.boost_amount  # 当前血量也相应增加
        elif self.stat_type == "max_mp":
            self.player.max_mp += self.boost_amount
            self.player.mp += self.boost_amount
        else:
            return f"未知的属性类型：{self.stat_type}"

        if self in self.player.inventory:
            self.player.inventory.remove(self)
        return f"使用了{self.name}，{self.stat_type}提升了{self.boost_amount}"


def create_default_items():
    """创建默认物品列表"""
    items = {
        "health_potion": HealingItem(
            name="简易生命药水",
            description="可以回复30点血量，很实惠，也很好用",
            price=20,
            heal_amount=30,
            icon_path=None,
        ),
        "mana_potion": ManaItem(
            name="简易魔力药水",
            description="可以回复30点魔力值，很实惠，也很好用",
            price=20,
            mana_amount=30,
            icon_path=None,
        ),
        "attack_boost": StatBoostItem(
            name="力量药水",
            description="可以在本次战斗中提升5点攻击",
            price=50,
            stat_type="attack",
            boost_amount=5,
            icon_path=None,
        ),
        "max_hp_boots": StatBoostItem(
            name="生命精华",
            description="永久性地提升10点生命值上限，是珍品中的珍品",
            price=100,
            stat_type="max_hp",
            boost_amount=10,
            icon_path=None,
        ),
        "max_mp_boots": StatBoostItem(
            name="魔力花",
            description="永久性地提升10点魔力上限，是珍品中的珍品",
            price=100,
            stat_type="max_mp",
            boost_amount=10,
            icon_path=None,
        ),
        "defense_boost": StatBoostItem(
            name="铁皮药水",
            description="本次战斗提升3点的防御力",
            price=50,
            stat_type="defense",
            boost_amount=3,
            icon_path=None,
        ),
    }
    return items



