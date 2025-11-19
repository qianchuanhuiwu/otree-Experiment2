from otree.api import *
import random

doc = """
投資信頼ゲーム
"""

class C(BaseConstants):
    NAME_IN_URL = 'trust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    ENDOWMENT = cu(10)
    
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    give_amount=models.CurrencyField(
        choices=currency_range(cu(0),cu(10),cu(1)),
        label='あなたは経営者にいくら投資しますか。',
    )

    back_amount=models.CurrencyField(
        label='投資家にいくら返戻しますか。',
    )

    multiplier = models.IntegerField()

    show_multiplier = models.BooleanField(
        label='投資家に収益率を開示しますか？',
        choices=[[True, '開示する'], [False, '開示しない']],
    )
    
    previous_info_shown = models.BooleanField(
        label='前ラウンドまでの情報を投資家に開示しますか？',
        choices=[[True, '開示する'], [False, '開示しない']],
        initial=False,
        blank=True
    )

class Player(BasePlayer):
    pass

#FUNCTIONS
def creating_session(subsession):
    subsession.group_randomly(fixed_id_in_group=True)
    
    for group in subsession.get_groups():
        group.multiplier = random.choice([3,5])

def compute(group:Group):
    p1=group.get_player_by_id(1)    #投資家
    p2=group.get_player_by_id(2)    #経営者
    p1.payoff=C.ENDOWMENT-group.give_amount+group.back_amount   #投資家の利得
    p2.payoff=group.give_amount*group.multiplier-group.back_amount  #k経営者の利得
    
def back_amount_choices(group:Group):
    max_amount = group.give_amount*group.multiplier
    return currency_range(cu(0),max_amount,cu(1))
    
# PAGES
class inst(Page):
     @staticmethod
     def is_displayed(player:Player):
        return player.round_number == 1

class Page1(Page):
     @staticmethod
     def is_displayed(player:Player):
        return player.round_number == 1

class Page1_2(Page):
    pass

class Page1_5(Page):
    form_model = 'group'
    form_fields = ['previous_info_shown']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.round_number > 1

class Page2_5(Page):
    form_model = 'group'
    form_fields = ['show_multiplier']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

class Page2_6(WaitPage):
    pass

class Page2(Page):
    form_model='group'
    form_fields=['give_amount']

    @staticmethod
    def is_displayed(player:Player):
        return player.id_in_group==1

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        partner = group.get_player_by_id(2)
        previous_rounds_info = []
        if player.round_number > 1 and group.previous_info_shown:
            for r in range(1, player.round_number):
                past_group = player.in_round(r).group
                previous_rounds_info.append({
                    'round': r,
                    'give_amount': past_group.give_amount,
                    'multiplier': past_group.multiplier,
                    'back_amount': past_group.back_amount
                })
                
        return dict(
            show_multiplier=group.show_multiplier,
            multiplier=group.multiplier if group.show_multiplier else None,
            previous_info_shown=group.previous_info_shown,
            previous_rounds_info=previous_rounds_info
        )


class Page3(WaitPage):
    pass

class Page4(Page):
    form_model='group'
    form_fields=['back_amount']

    @staticmethod
    def is_displayed(player:Player):
        return player.id_in_group==2

    @staticmethod
    def vars_for_template(player:Player):
        group = player.group
        return dict(
            multi_amount = group.give_amount*group.multiplier
    )

class Page5(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        compute(group)  # 利得計算

        for p in group.get_players():
            # participant.vars['history'] を初期化
            if 'history' not in p.participant.vars:
                p.participant.vars['history'] = []

            # 今ラウンドの情報を追加
            g = p.group
            p.participant.vars['history'].append({
                'round': g.round_number,
                'give_amount': g.give_amount,
                'back_amount': g.back_amount,
                'multiplier': g.multiplier
            })

class Page6(Page):
    @staticmethod
    def vars_for_template(player:Player):
        group = player.group
        return dict(
        multi_amount = group.give_amount*group.multiplier,
        multiplier = group.multiplier,
        give_amount = group.give_amount,
        back_amount = group.back_amount,
        payoff = player.payoff
       )
        


page_sequence = [inst,Page1,Page1_2,Page1_5,Page2_5,Page2_6,Page2,Page3,Page4,Page5,Page6]
