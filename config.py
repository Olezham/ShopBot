TOKEN = '' # Токен для бота

ticket_category_id = 1254086875790970940 # ид категории где будут создаваться тикеты
feedback_chanel_id = 1254081193067151401 # ид чата для отправки отзывов
ticket_role = 1139465593507020822 # ид роли кто будет видеть тикеты (продавец)
ticket_close_role = [1139465593507020822] # ид роли которая сможет закрывать тикет(пользыватель)


ID_POST = 1238128242695602236  # ИД поста(для роли по реакции)
USER_ROLES_LIST = ()
MAX_ROLES = 3
CHANNEL_FOR_ROLES_ID = 1237732586285957183

ROLES_LIST = {  # Смайлик : Ид роли 
    "🇷🇺": 1190696242523668530,  # ru
    "🇪🇺": 1190696282495406130,  # eu
}


host = 'eu01-sql.pebblehost.com'
username = 'customer_720687_sacle'
password = 'ptp!zRw7s4nb!Q7N2!De'
db = 'customer_720687_sacle'

extensions = ['cogs.article_ru',
			  'cogs.article_eu',
			  'cogs.embed',
			  'cogs.feedback_eu',
			  'cogs.feedback_ru',
			  'cogs.t_eu',
			  'cogs.t_ru',
			  'cogs.update'
              ]