from mygame_RPG.entities.player_skill import DamageSkill
from mygame_RPG.entities.player_skill import HealSkill
from mygame_RPG.entities.player_skill import selfDamageSkill
SKILLS = {
   "火球术" : DamageSkill("火球术",mp_cost = 20 ,damage = 40 ,description="对敌人释放火球，造成40点火球伤害") ,
   "治疗术" : HealSkill("治疗术",mp_cost = 40 , heal = 40 ,description="使用治疗术回复自己，回复40点生命值"),
   "闪电球" : DamageSkill("闪电球",mp_cost = 25,damage = 50,description="使用闪电，对敌人造成50点伤害"),
   "孤注一掷" : selfDamageSkill("孤注一掷",mp_cost=80,damage=99999,self_ratio=0.9,),

}
