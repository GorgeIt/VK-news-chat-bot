import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

#autorization
token = '3a652617f47ddfe7f67e68159b2f4d4f96ac635f2df2f96c852041a71e5cf160df8510e00aa53f30e045c'

#message
error = 'Не очень понял. Надо попробовать нажать на кнопку'
#gifs
gif = ['doc-204094421_591876928', 'doc-204094421_591875488', 'doc-204094421_591876947', 'doc-204094421_591876979', 'doc-204094421_591876992']

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
#5
keyboard_test = VkKeyboard(one_time=True)
keyboard_test.add_button('Нравится', color=VkKeyboardColor.POSITIVE)
keyboard_test.add_line()
keyboard_test.add_button('Не нравится', color=VkKeyboardColor.POSITIVE)
keyboard_test.add_line()
keyboard_test.add_button('Сомневаюсь', color=VkKeyboardColor.NEGATIVE)

#var
title = ''
titles = []

#test
test_questions = ['Нравится ли вам узнавать о достижениях в области технологий?', 'Любите ли вы поиграть в компьютерные игры?', 'Хотели бы вы посетить спортивные соревнования, смотреть спортивные передачи?', 'Нравится ли тебе узнавать об открытиях в различных сверах науки?', 'Любите ли вы путешествовать?']



news_tems = ['Спорт', 'Наука', 'Видеоигры', 'Технологии', 'Туризм']

group_id = 204094421
album_id = 279713994
access_token='5684421cf58460a6b5d065102b6e09d400a7c7d99947945052e0d5790236e12e29fad2a02436b9357ee7c'

