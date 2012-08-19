#coding: utf-8
from __future__ import division

import datetime
import math
from collections import Counter
import random

from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.db import models
from social_auth.backends.contrib.github import GithubBackend
from social_auth.signals import pre_update

from apps.helpers import gh, formulas



class Hero(models.Model):
    """Hero, based on github account of user"""

    user = models.OneToOneField(User, related_name='hero')

    login = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='')

    avatar_url = models.URLField(default='')
    html_url = models.URLField(default='')
    blog = models.URLField(default='')
    location = models.CharField(max_length=200,default='')
    hireable = models.BooleanField(default=False)

    public_repos = models.IntegerField(default=0)
    public_gists = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    attack_github = models.IntegerField(default=0)
    defence_github = models.IntegerField(default=0)
    attentiveness_github = models.IntegerField(default=0)
    charm_github = models.IntegerField(default=0)

    attack_own = models.IntegerField(default=0)
    defence_own = models.IntegerField(default=0)
    attentiveness_own = models.IntegerField(default=0)
    charm_own = models.IntegerField(default=0)
    
    attack_race = models.IntegerField(default=0)
    defence_race = models.IntegerField(default=0)
    attentiveness_race = models.IntegerField(default=0)
    charm_race = models.IntegerField(default=0)
    
    race = models.CharField(max_length=100, default='')

    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    power = models.IntegerField(default=0)
    army_power = models.IntegerField(default=0)
    last_update = models.DateTimeField(default=datetime.datetime(2000,1,1))

    def _get_stat(self, stat):
        """returns total value of stat by its name"""
        return getattr(self, stat+'_own')+getattr(self, stat+'_github')+getattr(self, stat+'_race')

    def get_attack(self):
        """returns total hero attack"""
        return self._get_stat('attack')

    def get_defence(self):
        """returns total hero defence"""
        return self._get_stat('defence')

    def get_attentiveness(self):
        """returns total hero attentiveness"""
        return self._get_stat('attentiveness')

    def get_charm(self):
        """returns total hero charm"""
        return self._get_stat('charm')

    def get_sum_stats(self):
        return self.get_attack()+self.get_defence()+self.get_attentiveness()+self.get_charm()

    def get_total_power(self):
        return self.power+self.army_power

    def in_battle_queue(self):
        return BattleQueue.objects.filter(hero=self).count() > 0

    def get_battle(self):
        try:
            return Battle.objects.get(Q(is_active=True),Q(hero1=self)|Q(hero2=self))
        except Exception:
            return None

    def update_from_response(self, response):
        """updates hero with info from auth response"""
        NO_MAX = 0
        PROPS_MAX = {
            'public_repos': 400,
            'followers': 8000,
            'following': 30,
            'public_gists': 200,
            'hireable': NO_MAX
        }
        HERO_PROP_LIMIT = 10
        for key, val in response.iteritems():
            if key != 'id' and not val is None and hasattr(self, key):
                prop_max = PROPS_MAX.get(key, NO_MAX)
                if prop_max==NO_MAX:
                    setattr(self, key, val)
                else:
                    setattr(self, key, formulas.scale_prop(val, HERO_PROP_LIMIT, prop_max))

    def update_race(self):
        """
        Updates race of hero (most popular race from units) and adds race bonuses.
        
        Race is set only once (after registration).
        """
        if self.race: return

        if Unit.objects.filter(hero=self).count()==0:
            self.race = 'human'
        else:
            units = Unit.objects.filter(hero=self)
            self.race = Counter([unit.race for unit in units]).most_common()[0][0]
        for stat, value in formulas.race_bonuses(self.race).items():
            setattr(self, stat+'_own', getattr(self, stat+'_own')+value)

    def update_race_bonuses(self):
        """ Recomputes race bonuses """
        for stat, value in formulas.race_bonuses(self.race, self.level).iteritems():
            setattr(self, stat+'_race', value)
            
    def get_minimal_stat(self):
        """ Returns name of the smallest hero stat.
        
        If there are several such stats, returns attacking one. If both are
        attacking or none of the minimal are attacking, returns random of them.
        """
        stats_dict = {'attack': 0, 'defence': 0, 'attentiveness': 0, 'charm': 0}
        for stat in stats_dict:
            stats_dict[stat] = self._get_stat(stat)
        min_value = min(stats_dict.itervalues())
        min_stats = [k for k in stats_dict if stats_dict[k]==min_value]
        if len(min_stats)==1:
            return min_stats[0]
        elif ('attack' in min_stats and 'attentiveness' not in min_stats):
            return 'attack'
        elif ('attack' in min_stats and 'attentiveness' not in min_stats):
            return 'attentiveness'
        else:
            return random.choice(min_stats)

    def gain_level(self):
        """ Increases hero level with all the recomputings """
        # computing Level Multiplier *before* level changing
        LM = int(math.ceil(0.1*self.level))
        self.level += 1
        self.update_race_bonuses()
        min_stat = self.get_minimal_stat()
        setattr(self, min_stat+'_own', self._get_stat(min_stat)+LM)

    def update_army(self):
        """
        updates army of hero with info of repositories in github
        if user hasn't repository, he get a unit Dummy
        """
        #todo: check for battle
        repos = gh.get_repos(self.login)
        if not repos:
            if Unit.objects.filter(hero=self).count()>0:
                return
            else:
                Unit(hero=self, name = 'Dummy').save()
                self.army_power = 0
                return

        Unit.objects.filter(hero=self).delete()

        self.army_power = 0
        for repo in repos:
            unit = Unit(hero=self)
            unit.update_from_response(repo)
            unit.save()
            self.army_power += unit.get_sum_stats_github()


    def save(self, *args, **kwargs):
        self.attack_github = 1+int(self.public_repos/2)+int(self.followers/2)
        self.defence_github = self.public_repos+int(self.public_gists/2)
        self.attentiveness_github = 1+self.following+int(self.followers/2)
        self.charm_github = self.followers+int(self.hireable)

        self.power = self.get_sum_stats()

        super(Hero, self).save(*args, **kwargs)


class Unit(models.Model):
    """member of army of hero, based on repositories of user"""

    hero = models.ForeignKey(Hero, related_name='units')

    name = models.CharField(max_length=200)
    custom_name = models.CharField(max_length=200)

    html_url = models.URLField(default='')
    language = models.CharField(max_length=100, default='')

    forks = models.IntegerField(default=0)
    watchers = models.IntegerField(default=0)
    open_issues = models.IntegerField(default=0)

    race = models.CharField(max_length=100, default='')

    attack_github = models.IntegerField(default=0)
    defence_github = models.IntegerField(default=0)
    attentiveness_github = models.IntegerField(default=0)
    charm_github = models.IntegerField(default=0)

    life = models.IntegerField(default=0)

    battle_target = models.ForeignKey('self', null=True, default=None)

    def _get_stat(self, stat):
        """returns total value of stat by its name"""
        return getattr(self, stat+'_github') + getattr(self.hero, 'get_'+stat)()

    def get_attack(self):
        """returns total hero attack"""
        return self._get_stat('attack')

    def get_defence(self):
        """returns total hero defence"""
        return self._get_stat('defence')

    def get_attentiveness(self):
        """returns total hero attentiveness"""
        return self._get_stat('attentiveness')

    def get_charm(self):
        """returns total hero charm"""
        return self._get_stat('charm')

    def get_sum_stats_github(self):
        return self.attack_github+self.defence_github+self.attentiveness_github+self.charm_github

    def get_max_life(self):
        return self.get_defence()*2


    def update_from_response(self, response):
        """updates hero with info from auth response"""
        UNIT_PROP_LIMIT = 20
        PROPS_MAX = {
            'forks': 5000,
            'watchers': 17000,
            'open_issues': 600,
        }
        for key, val in response.items():
            if key != 'id' and not val is None and hasattr(self, key):
                if key in PROPS_MAX:
                    setattr(self, key, formulas.scale_prop(val, UNIT_PROP_LIMIT, PROPS_MAX[key]))
                else:
                    setattr(self, key, val)

    def save(self, *args, **kwargs):
        self.attack_github = int(self.forks/2)
        self.defence_github = self.forks+int(self.watchers/4.0)
        self.attentiveness_github = int(self.watchers/2.0)
        self.charm_github = int(self.watchers/2)+int(self.open_issues/4.0)

        self.race = formulas.lang_to_race(self.language)

        if not self.custom_name:
            self.custom_name = self.name

        super(Unit, self).save(*args, **kwargs)



class BattleQueue(models.Model):
    """Queue of heroes, waiting battle"""
    hero = models.ForeignKey(Hero)
    date = models.DateTimeField()

class Battle(models.Model):
    """battle betwen two heroes"""

    hero1 = models.ForeignKey(Hero, related_name='battles1')
    hero2 = models.ForeignKey(Hero, related_name='battles2')

    hero1_moved = models.BooleanField(default=False)
    hero2_moved = models.BooleanField(default=False)

    date = models.DateTimeField()

    is_active = models.BooleanField()
    round = models.SmallIntegerField(default=1)
    winner = models.ForeignKey(Hero, related_name='winned_battles', null=True, default=None)

    def get_opponent(self, hero):
        if self.hero1==hero:
            return self.hero2
        elif self.hero2==hero:
            return self.hero1
        else:
            return None

    def is_moved(self, hero):
        if self.hero1==hero:
            return self.hero1_moved
        elif self.hero2==hero:
            return self.hero2_moved
        else:
            return False

    def set_moved(self, hero, val):
        if self.hero1==hero:
            self.hero1_moved = val
        elif self.hero2==hero:
            self.hero2_moved = val




class Spell(models.Model):
    """a spell that `hero` can cast"""

    hero = models.ForeignKey(Hero, related_name='spells')

    type = models.CharField(max_length=200)
    cnt = models.IntegerField(default=1)
    



def social_auth_update_user(sender, user, response, details, **kwargs):

    try:
        hero = Hero.objects.get(user=user)
        created = False
    except Exception:
        hero = Hero(user=user)
        created = True

    hero.update_from_response(response)
    hero.save()

    if created:
        hero.update_army()
        hero.update_race()
        hero.save()


    return True

pre_update.connect(social_auth_update_user, sender=GithubBackend)

