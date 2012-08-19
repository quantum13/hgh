# coding: utf-8
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from apps.helpers.formulas import get_hit_chance, is_hits, get_damage, get_exp
from apps.main.models import Unit, HeroEffect, UnitEffect, CastingSpell, HeroLog

def check_defeat(army):
    """ Checks defeat of hero in battle or not. Hero defeated if his army is defeated"""
    return all([unit.life <= 0 for unit in army])

def battle_result_hero_defeated(battle, hero, opponent, opponent_defeated):
    """ Ends battle with loosing of one or more heroes"""

    battle.add_log_line_hero_defeated( hero.login)

    if not opponent_defeated:
        battle.winner = opponent

        opponent.wins += 1
        opponent.add_experience(get_exp(opponent, hero, True))
    else:
        opponent.losses += 1
        opponent.add_experience(get_exp(opponent, hero, False))
        battle.add_log_line_hero_defeated( opponent.login)

    hero.losses +=1
    hero.add_experience(get_exp(hero, opponent, False))

    hero.save()
    opponent.save()

    battle.is_active = False
    battle.save()


def process_move(battle, hero1, hero2, hero1_army, hero2_army):
    """ Calcs result of move """
    army_dict = dict([(unit.pk,unit) for unit in hero1_army+hero2_army])
    #casting of spells must be before direct attacks
    # only units survived after spells do attack

    defeated_units = []
    for unit in hero1_army+hero2_army:
        target = army_dict[unit.battle_target_id]
        if target.life<=0:
            continue
        if is_hits(unit.get_attack(), target.get_defence()):
            damage = get_damage(unit.get_attack(), target.get_defence())
            target.life -= damage
            battle.add_log_line_hits(unit.custom_name, target.custom_name, damage)
            if target.life<=0:
                defeated_units.append(target)
            target.changed = True
        else:
            battle.add_log_line_missing(unit.custom_name, target.custom_name)

    for unit in defeated_units:
        battle.add_log_line_unit_defeated(unit.custom_name)


    hero1_defeated = check_defeat(hero1_army)
    hero2_defeated = check_defeat(hero2_army)

    if hero1_defeated:
        battle_result_hero_defeated(battle, hero1, hero2, hero2_defeated)
    elif hero2_defeated:
        battle_result_hero_defeated(battle, hero2, hero1, hero1_defeated)
    else:
        battle.round += 1
        battle.hero1_moved = False
        battle.hero2_moved = False
        battle.add_log_line_new_round()
        battle.save()
        Unit.objects.filter(Q(hero=hero1)|Q(hero=hero2)).update(battle_target=None)
        # decreasing duration of effects and eliminating ones that ended
        HeroEffect.objects.filter(Q(hero=hero1)|Q(hero=hero2)).update(duration=F('duration')-1)
        HeroEffect.objects.filter(duration__lte=0).delete()
        UnitEffect.objects.filter(unit__in=(hero1.units.filter(life_gt = 0)|hero2.units.filter(life_gt = 0)))
        for unit in hero1_army+hero2_army:
            if hasattr(unit, 'changed'):
                unit.save()

        hero1_army = [unit for unit in hero1_army if unit.life>0]
        hero2_army = [unit for unit in hero2_army if unit.life>0]

        #CastingSpell.objects.select_related().filter(spell__in=(hero1.spells.all()|hero2.spells.all())).delete()

