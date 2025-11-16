from os import environ

SESSION_CONFIGS = [
    dict(
        name='questionnaire',
        display_name='アンケート',
        num_demo_participants=1, 
        app_sequence=['questionnaire'],
    ),
    dict(
        name='trust',
        display_name="投資信頼ゲーム",
        num_demo_participants=2,
        app_sequence=['trust'],
    )
]



SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1385553024088'
