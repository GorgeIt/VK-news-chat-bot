import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

#autorization
token = '3a652617f47ddfe7f67e68159b2f4d4f96ac635f2df2f96c852041a71e5cf160df8510e00aa53f30e045c'
group_id = 204094421
album_id = 279713994
access_token = '5684421cf58460a6b5d065102b6e09d400a7c7d99947945052e0d5790236e12e29fad2a02436b9357ee7c'

#message
error = 'Не очень понял. Надо попробовать нажать на кнопку'

#keyboard
#1
keyboard_1 = VkKeyboard(one_time=True)
keyboard_1.add_button('Добавить новость', color=VkKeyboardColor.NEGATIVE)
keyboard_1.add_line()
keyboard_1.add_button('Новости', color=VkKeyboardColor.POSITIVE)
keyboard_1.add_line()
keyboard_1.add_button('Изменить новость', color=VkKeyboardColor.PRIMARY)
keyboard_1.add_line()
keyboard_1.add_button('Запостить новость в группу')

#1 user
keyboard_1_user = VkKeyboard(one_time=True)
keyboard_1_user.add_button('Новости', color=VkKeyboardColor.POSITIVE)

#1 journalist
keyboard_1_journalist = VkKeyboard(one_time=True)
keyboard_1_journalist.add_button('Добавить новость', color=VkKeyboardColor.NEGATIVE)
keyboard_1_journalist.add_line()
keyboard_1_journalist.add_button('Новости', color=VkKeyboardColor.POSITIVE)
keyboard_1_journalist.add_line()
keyboard_1_journalist.add_button('Изменить новость', color=VkKeyboardColor.PRIMARY)

#2
keyboard_assessment = VkKeyboard(one_time=True)
keyboard_assessment.add_button('Понравилась', color=VkKeyboardColor.POSITIVE)
keyboard_assessment.add_button('Не понравилась', color=VkKeyboardColor.NEGATIVE)

#3
keyboard_bool = VkKeyboard(one_time=True)
keyboard_bool.add_button('Да', color=VkKeyboardColor.POSITIVE)
keyboard_bool.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
#4
keyboard_change = VkKeyboard(one_time=True)
keyboard_change.add_button('Заголовок', color=VkKeyboardColor.POSITIVE)
keyboard_change.add_button('Текст', color=VkKeyboardColor.POSITIVE)
keyboard_change.add_line()
keyboard_change.add_button('Удалить новость', color=VkKeyboardColor.NEGATIVE)

#list main keyboards
main_keyboards = [keyboard_1_user, keyboard_1_journalist, keyboard_1]

#can do anything
leader_ids = [550623530, 180975334]

#journalists
journalists_ids = []

#var
title = ''
titles = []
new_title = ''

#dots
stiv_0 = 'Доброго времени суток! Уже на протяжении двух недель в нашем сообществе ботов не прекращается ожесточённая дискуссия по поводу...'

zig_0 = 'ТоЧеК!!!!!!!'

stiv_1 = 'Я считаю, что в конце каждого предложения в сообщении должен стоять знак препинания. И не важно, восклицательный это знак, знак вопросительный или точка.\nПунктуационные правила великого и могучего русскоо языка на моей стороне! Точки в конце предложеня не ставят только сумасшедшие.'

zig_1 = 'А я считаю, нормальный человек ты или абсолютный безумец, точки в сообщениях - это, типа, #Воучтозажесть?!\nСмысл же и так понятен'

stiv_2 = 'Зигмунд, твоё отношение к такому важному аспекту интернет-общения меня удручает и активно побуждает предпринять оперативные меры.'

zig_2 = 'За точки, Стив, ты у меня отправишся в ЧС! Это последнее китайское предупреждение'

stiv_3 = 'Видите, мы не можем разрешить палемический поединок своими силами. Нам нужна Ваша помощь!' 

zig_3 = 'Присоединяйся о мне! Тёмная сторона объединяет?'

questions_dots = [stiv_0, zig_0, stiv_1, zig_1, stiv_2, zig_2, stiv_3, zig_3]

keyboard_dots = VkKeyboard(one_time=True)
keyboard_dots.add_button('Я ставлю точки', color=VkKeyboardColor.POSITIVE)
keyboard_dots.add_button('Я не ставлю точки', color=VkKeyboardColor.NEGATIVE)

#topics

questions = ['Хотели бы вы посетить спортивные соревнования, смотреть спортивные передачи?', 'Нравится ли тебе узнавать об открытиях в различных сверах науки?', 'Хотели бы вы ещё раз попасть в Артек?', 'Нравится ли вам узнавать о достижениях в области технологий?', 'Любите ли вы путешествовать?']

news_topics = ['Спорт', 'Наука', 'Артек', 'Технологии', 'Туризм и отдых']
news_topics_db = ['sport', 'science', 'artek', 'technology', 'tourism']

new_news_topics = [] #новые темы

black_cat = ['photo-204094421_457239108','photo-204094421_457239112',  'photo-204094421_457239104', 'photo-204094421_457239115', 'photo-204094421_457239110','photo-204094421_457239105', 'photo-204094421_457239107', 'photo-204094421_457239111', 'photo-204094421_457239113', 'photo-204094421_457239114', 'photo-204094421_457239116','photo-204094421_457239109', 'photo-204094421_457239106']
flying_fox = ['photo-204094421_457239081', 'photo-204094421_457239083',  'photo-204094421_457239087', 'photo-204094421_457239084', 'photo-204094421_457239086','photo-204094421_457239079', 'photo-204094421_457239080',  'photo-204094421_457239082', 'photo-204094421_457239085',  'photo-204094421_457239088', 'photo-204094421_457239089',  'photo-204094421_457239091', 'photo-204094421_457239090','photo-204094421_457239092']
corgi = ['photo-204094421_457239125','photo-204094421_457239119', 'photo-204094421_457239123', 'photo-204094421_457239120', 'photo-204094421_457239122','photo-204094421_457239117', 'photo-204094421_457239118',   'photo-204094421_457239121',  'photo-204094421_457239124',  'photo-204094421_457239126',   'photo-204094421_457239129', 'photo-204094421_457239127', 'photo-204094421_457239128']
elf = ['photo-204094421_457239130', 'photo-204094421_457239141', 'photo-204094421_457239136', 'photo-204094421_457239131', 'photo-204094421_457239132', 'photo-204094421_457239133', 'photo-204094421_457239134',  'photo-204094421_457239137',  'photo-204094421_457239139', 'photo-204094421_457239140',  'photo-204094421_457239142', 'photo-204094421_457239135', 'photo-204094421_457239138']
kitsune = ['photo-204094421_457239151', 'photo-204094421_457239154', 'photo-204094421_457239146','photo-204094421_457239143', 'photo-204094421_457239144',  'photo-204094421_457239147', 'photo-204094421_457239149', 'photo-204094421_457239150',  'photo-204094421_457239152', 'photo-204094421_457239153', 'photo-204094421_457239145', 'photo-204094421_457239148']


avatars = [corgi, elf, flying_fox, black_cat, kitsune]

avatars_with_topic = {'спорт' : corgi, 'наука' : elf, 'артек' : flying_fox, 'технологии' : black_cat, 'туризм и отдых' : kitsune}

test_questions = ['Здравия желаю! Я Фаззи, приятно познакомиться. Я очень люблю заниматься спортом и всегда принимаю участие во всех соревнованиях. Хотел бы ты прийти и посмотреть на мою игру?', 'Привет! Меня зовут Бинго и мне очень нравится заниматься наукой. А нравится ли тебе узнавать об открытиях в различных сферах науки?', 'Салют! Вас приветствует Феликс - главный эксперт Артека. Хочешь ли ты ещё раз попасть в Артек? \n P.S Если что, обращайся:)', 'Хэллоу! Зови меня Арчи. Если нужно что-то починить, обращайся. А нравится ли тебе узнавать о достижениях в области технологий?', 'Мур мур) \n Моё имя Кисуню, и я только что прилетела из Италии. А ты интересуешься путешествиями?']