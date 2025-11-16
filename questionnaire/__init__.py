from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q_gender = models.CharField(
        initial=None,
        choices=['男性','女性','無回答'],
        verbose_name='性別をお答えください',
        widget=widgets.RadioSelect)
    
    q_age = models.IntegerField(
        initial=None,
        verbose_name='年齢をお答えください',
        choices=range(15,30)
    )

# PAGES
class page1(Page):
    form_model='player'
    form_fields=[
        'q_gender',
        'q_age'
    ]


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [page1]
