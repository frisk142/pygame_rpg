
class Skill: # 技能基类
    def __init__(self, name, mp_cost, description="",switch_turn=False):
        self.name = name
        self.mp_cost = mp_cost
        self.description = description
        self.switch_turn = switch_turn

    def can_use(self, user): # 检查是否有足够的魔法值
        return user.mp >= self.mp_cost

    def use(self, user, target): # 技能效果由子类实现
        raise NotImplementedError("子类必须实现 use 方法")

    def get_use_message(self, user, target):
        return f"使用了{self.name}"

class DamageSkill(Skill): # 伤害类技能
    def __init__(self, name, mp_cost, damage, description=""):
        super().__init__(name, mp_cost, description)
        self.damage = damage

    def use(self, user, target):
        if not self.can_use(user):
            return None, "MP不足"
        user.mp -= self.mp_cost
        target.hp -= self.damage
        return True, f"{self.name}造成了{self.damage}点伤害！"

    def get_use_message(self, user, target):
        return f"{self.name}造成了{self.damage}点伤害！"

class HealSkill(Skill):
    def __init__(self, name, mp_cost,heal, description="",switch_turn=False):
        super().__init__(name, mp_cost, description,switch_turn)
        self.heal = heal

    def use(self, user, target):
        if not self.can_use(user):
            return None
        user.mp -= self.mp_cost
        user.hp = min(user.hp + self.heal,user.max_hp)
        return True, f"{self.name}回复了{self.heal}点生命值"

class selfDamageSkill(DamageSkill):
    def __init__(self, name, mp_cost, damage,self_ratio,description=""):
        super().__init__(name, mp_cost, damage,description)
        self.self_ratio = self_ratio
    def use(self, user, target):
        if not self.can_use(user):
            return None,"MP不足"
        user.mp -= self.mp_cost
        target.hp -= self.damage
        user.hp = int(user.hp * (1-self.self_ratio))
        return True, f"{self.name}造成了{self.damage}伤害，但是自身也受伤了"
