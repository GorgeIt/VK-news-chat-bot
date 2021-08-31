# -*- coding: utf-8 -*-
from requests.models import Response, parse_url
import vk_api
import vk
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import time
from vk_api.longpoll import VkLongPoll,VkEventType
import random
from config import *
import sqlite3
import requests
import json

#vk
vk_session = vk_api.VkApi(token = token)
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)
vk = vk_session.get_api()

#db
conn = sqlite3.connect("db.db")
c = conn.cursor()

##################
#upload to wall
##################

def upload_to_wall(title, text):
    r = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params={'group_id': group_id,
                                                                                    'access_token': access_token,
                                                                                    'v': 5.21}).json() 
    upload_url = r['response']['upload_url']
    file = {'file1': open('photo_user\img.jpg', 'rb')}
    ur = requests.post(upload_url, files=file).json()
    result = requests.get('https://api.vk.com/method/photos.saveWallPhoto', params={'access_token': access_token,
                                                                                    'group_id': group_id,
                                                                                    'photo': ur['photo'],
                                                                                    'server': ur['server'],
                                                                                    'hash': ur['hash'],
                                                                                    'v': 5.21}).json()
    attachment =  "photo{}_{}".format(result['response'][0]['owner_id'],  result['response'][0]['id'])                                                                           
    post = requests.get('https://api.vk.com/method/wall.post', params={'access_token': access_token, 'owner_id': -204094421, 'message': title+'\n'+'\n'+text, 'attachment':attachment,'v': 5.21}).json()
                                                                                                                                                                                                                         
def get_biggest(sizes):
    if sizes['width'] >= sizes['height']:
        return sizes['width']
    else:
        return sizes['height']
                
def download_photo(photos):
    r = requests.get('https://api.vk.com/method/photos.getById', params={'photos': photos,
                                                                        'access_token': access_token,
                                                                        'photo_sizes': 1,
                                                                        'v': 5.21}).json()                                                                                                                                                                                              
    

    for photo in r["response"]:
        sizes = photo["sizes"]
        max_size_url = max(sizes, key=get_biggest)['src']
    p = requests.get(max_size_url)
    out = open('photo_user\img.jpg', "wb")
    out.write(p.content)
    out.close()

def post_to_wall(title, text, attachment=None):
    if attachment=='':
        t = requests.get('https://api.vk.com/method/wall.post', params={'access_token': access_token, 'owner_id': -204094421, 'message':title +'\n'+'\n'+text, 'v': 5.21}).json()
    else:
        download_photo(attachment[5:])
        upload_to_wall(title, text)
                                                                                                                           
#############
#message
#############

def write_msg(user_id, message, keyboard=None, attachment=None):
    if attachment is None:
        if keyboard is None:
            vk.messages.send(random_id = int(round(time.time() * 1000)), user_id = user_id, message = message)
        else:
            vk.messages.send(keyboard = keyboard.get_keyboard(), random_id = int(round(time.time() * 1000)), user_id = user_id, message = message)
    else:
        if keyboard is None:
            vk.messages.send(random_id = int(round(time.time() * 1000)), user_id = user_id, message = message, attachment=attachment)
        else:    
            vk.messages.send(keyboard = keyboard.get_keyboard(), attachment=attachment, random_id = int(round(time.time() * 1000)), user_id = event.user_id, message=message)

#############
#reg
################

def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True

def register_new_user(user_id, role):
    c.execute("INSERT INTO users(user_id, status, status_stage, page, role) VALUES (%d, '%s', '%s', %d, %d)" % (user_id, '', '', 0, role))
    conn.commit()

###############
#work with user
##############

def set_user_status(user_id, state):
    c.execute("UPDATE users SET status='%s' WHERE user_id=%d" % (state, user_id))
    conn.commit()

def set_user_status_stage(user_id, state):
    c.execute("UPDATE users SET status_stage='%s' WHERE user_id=%d" % (state, user_id))
    conn.commit()
    
def get_user_status(user_id):
    c.execute("SELECT status FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]

def get_user_status_stage(user_id):
    c.execute("SELECT status_stage FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return None
    else:    
        return result[0]

##################    
#news   
################# 

def set_page(user_id):
    c.execute("UPDATE users SET page = %d WHERE user_id=%d" % (0, user_id))
    conn.commit()

def get_title(user_id):
    c.execute("SELECT title FROM news WHERE text='%s' AND user_id=%d" % ('', user_id))
    return c.fetchone()[0]

def get_text(title):
    c.execute("SELECT text FROM news WHERE title='%s'" % title)
    return c.fetchone()

def get_img(title):
    c.execute("SELECT attachments FROM news WHERE title='%s'" % title)
    return c.fetchone()  

def get_col_column(topic):
    c.execute("SELECT COUNT(*) FROM news WHERE topic = '%s'" % topic)
    result = c.fetchone()[0]
    return result

def get_titles(topic):
    c.execute("SELECT title FROM news WHERE topic = '%s' ORDER BY likes COLLATE RTRIM DESC" % topic)
    result, lst = c.fetchall(), []
    for i in range(len(result)):
        lst.append(str(i+1) +'. ' + str(*result[i]) + ' ' + str(*get_col_like(str(*result[i]))) + ' &#128077;')
    return lst

def set_title(user_id, title):
    c.execute("INSERT INTO news(user_id, title, text, likes, attachments, topic) VALUES (%d, '%s', '%s', %d, '%s', '%s')" % (user_id, title, '', 0, '', ''))
    conn.commit()

def change_title(title, new_title):
    c.execute("UPDATE news SET title='%s' WHERE title='%s'" % (new_title, title))
    conn.commit()
    c.execute("UPDATE like SET news='%s' WHERE news='%s'" % (new_title, title))
    conn.commit()

def set_text(title, text):
    c.execute("UPDATE news SET text='%s' WHERE title='%s'" % (text, title))
    conn.commit()

def set_attachments(title, attachment):
    c.execute("UPDATE news SET attachments='%s' WHERE title='%s'" % (attachment, title))
    conn.commit()

def set_topic(title, topic):
    c.execute("UPDATE news SET topic='%s' WHERE title='%s'" % (topic, title))
    conn.commit()

def get_topics(title):
    c.execute("SELECT topic FROM news WHERE title = '%s'" % title)
    result = c.fetchone()
    return str(result[0])

def get_news(num, titles):
    for i in titles:
        if i.split('.')[0] == num:
            title = ' '.join(i.split()[1:-2])      
    return title

def before_get_news(page, topic):
    keyboard = VkKeyboard(one_time=True)
    for i in range(page*5 + 1, get_col_column(topic)+1):    
        if i % 5 == 0:
            keyboard.add_line()
            if page > 0:
                keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
            break
        keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
        if i == get_col_column(topic) and i > 5 and page > 0:
            keyboard.add_line()
            keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
    if get_col_column(topic)>(page+1)*5:
        keyboard.add_button('Далее', color=VkKeyboardColor.PRIMARY)        
    titles = get_titles(topic)
    write_msg(user_id, 'Выбери новость\n' + '\n'.join(titles[page*5:(page+1)*5]), keyboard = keyboard, attachment = avatars_with_topic[topic][3])  
    return titles

def get_page(user_id):
    c.execute("SELECT page FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return int(result[0])

def next_page(user_id):
    c.execute("UPDATE users SET page = page + 1 WHERE user_id=%d" % user_id)
    conn.commit()

def back_page(user_id):    
    c.execute("UPDATE users SET page = page - 1 WHERE user_id=%d" % user_id)
    conn.commit()

def del_news(title):
    c.execute("DELETE FROM news WHERE title='%s'" % title)
    conn.commit()

################
#like   
################

def set_likes(title):
    c.execute("UPDATE news SET likes = likes + 1 WHERE title='%s'" % title)
    conn.commit()

def check_if_like(title, user_id):
    c.execute("SELECT user_id FROM like WHERE news = '%s'" % title)
    result, lst = c.fetchall(), []
    for i in result:
        lst.append(*i)
    if result is None or user_id not in lst:
        return False
    return True

def user_do_like(title, user_id):
    c.execute("INSERT INTO like(user_id, news) VALUES (%d, '%s')" % (user_id, title))
    conn.commit()    

def get_col_like(title):
    c.execute("SELECT likes FROM news WHERE title = '%s'" % title)
    result = c.fetchone()  
    return result

####################
#quiz
####################

def st_quiz(user_id):
    c.execute("INSERT INTO user_news(user_id, sport, science, artek, technology, tourism) VALUES (%d, %d, %d, %d, %d, %d)" % (user_id, 0,0,0,0,0))
    conn.commit()

def give_question(num):
    #test_questions = ['Нравится ли вам узнавать о достижениях в области технологий?', 'Хотели бы вы ещё раз попасть в Артек?', 'Хотели бы вы посетить спортивные соревнования, смотреть спортивные передачи?', 'Нравится ли тебе узнавать об открытиях в различных сверах науки?', 'Любите ли вы путешествовать?']
    return test_questions[num]

def set_point(user_id, topic):
    c.execute("UPDATE user_news SET '%s' = '%s' + 1 WHERE user_id= %d" % (topic, topic, user_id))
    conn.commit()

def get_topic(user_id):
    c.execute("SELECT sport, science, artek, technology, tourism FROM user_news WHERE user_id=%d" % user_id)
    result = c.fetchone()
    return result

def get_preference(user_id):
    preference = {}
    k = 0
    for i in get_topic(user_id):
        preference[news_topics[k]] = i
        k+=1
    return preference

def get_sorted_preference(user_id):
    dict, sorted_dict = get_preference(user_id), {}
    sorted_keys = reversed(sorted(dict, key=dict.get))
    for w in sorted_keys:
        sorted_dict[w] = dict[w]
    return list(sorted_dict.keys())

def new_question():
    if int(get_user_status_stage(user_id))>=len(news_topics_db):
        set_user_status(user_id, '')
        set_user_status_stage(user_id, '')
        write_msg(user_id, 'Спасибо за ответы', main_keyboards[get_role(user_id)], kitsune[-1])  
    else:   
        num = int(get_user_status_stage(user_id)) 
        question = give_question(num)
        write_msg(user_id, question, keyboard_bool, avatars[num][0])
        set_user_status_stage(user_id, 'choose'+' '+get_user_status_stage(user_id))

def generate_keyboard(user_id):
    keyboard = VkKeyboard(one_time=True)
    topics, k = get_sorted_preference(user_id), 1
    for i in topics:
        if k%3 == 0:
            keyboard.add_line()
        keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
        k+=1
    return keyboard        

####################
#keyboard
####################

def get_role(user_id):
    c.execute("SELECT role FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return int(result[0])

###########################################################################################################################################################################################
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            original_text = event.text
            sms = original_text.lower()
    ########################################################
            # quiz
    ########################################################

            if True:
                if not check_if_exists(user_id) or get_user_status(user_id) == 'quiz':
                    if get_user_status_stage(user_id) is None:
                        if user_id in leader_ids:
                            register_new_user(user_id, 2)

                        elif user_id in journalists_ids:
                            register_new_user(user_id, 1)

                        else:
                            register_new_user(user_id, 0)    
                            
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('Начать', color=VkKeyboardColor.POSITIVE)
                        st_quiz(user_id)
                        set_user_status_stage(user_id, '0')
                        set_user_status(user_id, 'quiz')
                        write_msg(user_id, 'Привет 🖐. Для того чтобы наше общение было интересным, нам нужно поближе познакомится. Нажми начать для начала игры', keyboard, flying_fox[-1])

                    elif get_user_status_stage(user_id).isdigit() and sms == 'начать':
                        new_question()
                        
                    elif sms == 'да' and 'choose' in get_user_status_stage(user_id):
                        set_point(user_id, news_topics_db[int(get_user_status_stage(user_id).split()[-1])])
                        set_user_status_stage(user_id, str(int(get_user_status_stage(user_id).split()[-1])+1))
                        new_question()

                    elif sms == 'нет' and 'choose' in get_user_status_stage(user_id):
                        set_user_status_stage(user_id, str(int(get_user_status_stage(user_id).split()[-1])+1))
                        new_question()
                        
        ###########################################################
                #новая новость
        ###########################################################

                elif (sms == 'добавить новость' or get_user_status(user_id) == 'add') and get_role(user_id) >= 1:
                    if get_user_status_stage(user_id) == '':
                        write_msg(user_id, 'Напиши заголовок:', attachment = random.choice(avatars)[-1])
                        set_user_status_stage(user_id, 'set_tit')
                        set_user_status(user_id, 'add')

                    elif get_user_status_stage(user_id) == 'set_tit':
                        set_title(user_id, original_text)
                        write_msg(user_id, 'Теперь напиши саму новость', attachment = random.choice(avatars)[-3])
                        set_user_status_stage(user_id, 'set_tex' + ' ' + original_text)
        
                    elif 'set_tex' in get_user_status_stage(user_id):
                        set_text(get_title(user_id), original_text)
                        write_msg(user_id, 'Хочешь добавить картинку к новости?', keyboard_bool, attachment = random.choice(avatars)[-2])
                        set_user_status_stage(user_id, 'choose' + ' ' + ' '.join(get_user_status_stage(user_id).split()[1:]))

                    elif sms == 'да' and 'choose' in get_user_status_stage(user_id):
                        write_msg(user_id, 'Отправь изображение', attachment = random.choice(avatars)[4])
                        set_user_status_stage(user_id, 'set_img'+ ' ' + ' '.join(get_user_status_stage(user_id).split()[1:]))

                    elif 'set_img' in get_user_status_stage(user_id):   
                        result = vk_session.method("messages.getById", {"message_ids": [event.message_id]})
                        photo = result['items'][0]['attachments'][0]['photo']
                        attachment = "photo{}_{}_{}".format(photo['owner_id'], photo['id'], photo['access_key'])
                        set_attachments(' '.join(get_user_status_stage(user_id).split()[1:]), attachment)
                        set_user_status_stage(user_id, 'choos_topic'+ ' ' + ' '.join(get_user_status_stage(user_id).split()[1:]))
                        write_msg(user_id, 'Выбери тему новости:', generate_keyboard(user_id), attachment = random.choice(avatars)[-1])
                        
                    elif sms == 'нет' and 'choose' in get_user_status_stage(user_id):
                        set_user_status_stage(user_id, 'choos_topic'+ ' ' + ' '.join(get_user_status_stage(user_id).split()[1:]))
                        write_msg(user_id, 'Выбери тему новости', generate_keyboard(user_id), attachment = random.choice(avatars)[-1])  

                    elif 'choos_topic' in get_user_status_stage(user_id):
                        set_topic(' '.join(get_user_status_stage(user_id).split()[1:]), sms)
                        write_msg(user_id, 'Записал', main_keyboards[get_role(user_id)], kitsune[-1])
                        set_user_status(user_id, '')
                        set_user_status_stage(user_id, '')
                        set_page(user_id)

        ###########################################################
                #выдать новость и поставить лайк
        ###########################################################

                elif sms == 'новости' or get_user_status(user_id) == 'give':
                    if get_user_status_stage(user_id) == '':
                        set_user_status_stage(user_id, 'choos_topic')
                        set_user_status(user_id, 'give')
                        write_msg(user_id, 'Выбери тему новости', generate_keyboard(user_id), attachment = random.choice(avatars)[1])  

                    elif 'choos_topic' in get_user_status_stage(user_id):
                        topic = sms
                        if get_col_column(topic) != 0:
                            titles = before_get_news(get_page(user_id), topic)
                            set_user_status_stage(user_id, 'choose'+' '+topic)
                        else:
                            write_msg(user_id, 'Новостей пока нет', main_keyboards[get_role(user_id)], avatars_with_topic[topic][2])
                            set_user_status(user_id, '')
                            set_user_status_stage(user_id, '')
                            set_page(user_id)

                    elif sms.isdigit() and 'choose' in get_user_status_stage(user_id):
                        title = get_news(sms, titles)
                        write_msg(user_id, *get_text(title), attachment=get_img(title))
                        if not check_if_like(title, user_id):
                            write_msg(user_id, 'Оцени новость', keyboard = keyboard_assessment, attachment = random.choice(avatars_with_topic[get_topics(title)]))
                            set_user_status_stage(user_id, 'appraise' + ' '+ title)
                        else:
                            set_user_status(user_id, '')
                            set_user_status_stage(user_id, '')
                            set_page(user_id)
                            write_msg(user_id, 'Спасибо за просмотр', keyboard = main_keyboards[get_role(user_id)], attachment =  avatars_with_topic[get_topics(title)][1]) 

                    elif sms == 'далее' and 'choose' in get_user_status_stage(user_id):
                        next_page(user_id)
                        titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[1:]))

                    elif sms == 'назад' and 'choose' in get_user_status_stage(user_id):
                        back_page(user_id)
                        titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[1:]))   

                    elif sms == 'понравилась' and 'appraise' in get_user_status_stage(user_id):
                        title = ' '.join(get_user_status_stage(user_id).split()[1:])
                        write_msg(user_id, 'Спасибо за оценку', keyboard = main_keyboards[get_role(user_id)], attachment =  avatars_with_topic[get_topics(title)][1])
                        set_likes(title)
                        user_do_like(title, user_id)
                        set_user_status(user_id, '')
                        set_user_status_stage(user_id, '')
                        set_page(user_id)
                        

                    elif sms == 'не понравилась' and 'appraise' in get_user_status_stage(user_id):
                        title = ' '.join(get_user_status_stage(user_id).split()[1:])
                        write_msg(user_id, 'Спасибо за оценку', keyboard = main_keyboards[get_role(user_id)], attachment =  avatars_with_topic[get_topics(title)][2])
                        set_user_status(user_id, '')
                        set_user_status_stage(user_id, '')
                        set_page(user_id)   

        ###########################################################
                # изменить новость
        ###########################################################          

                elif (sms == 'изменить новость' or get_user_status(user_id) == 'change') and get_role(user_id) >= 1:
                    if get_user_status_stage(user_id) == '':
                        write_msg(user_id, 'Что ты хочешь поменять?', keyboard=keyboard_change, attachment = random.choice(avatars)[1])
                        set_user_status(user_id, 'change')
                        set_user_status_stage(user_id, 'choose')

                #заголовок        
                    elif sms == 'заголовок' and get_user_status_stage(user_id) == 'choose' or 'заголовок' in get_user_status_stage(user_id):
                        if get_user_status_stage(user_id) == 'choose':
                            set_user_status_stage(user_id, 'choos_topic заголовок')
                            write_msg(user_id, 'Выбери тему новости', generate_keyboard(user_id), attachment = random.choice(avatars)[0])

                        elif 'choos_topic' in get_user_status_stage(user_id):
                            topic = sms
                            if get_col_column(topic) != 0:
                                titles = before_get_news(get_page(user_id), topic)
                                set_user_status_stage(user_id, 'выбрать заголовок'+' '+topic)
                            else:
                                write_msg(user_id, 'Тут новостей нет', main_keyboards[get_role(user_id)],  attachment = avatars_with_topic[topic][2])
                                set_user_status(user_id, '')
                                set_user_status_stage(user_id, '')  
                                set_page(user_id)  

                        elif sms.isdigit() and 'выбрать заголовок' in get_user_status_stage(user_id):
                            title = get_news(sms, titles)
                            write_msg(user_id, 'Напиши изменённый заголовок',  attachment = avatars_with_topic[get_topics(title)][1])     
                            set_user_status_stage(user_id, 'заголовок set_tit' + ' ' + title)

                        elif sms == 'далее' and 'выбрать заголовок' in get_user_status_stage(user_id):
                            next_page(user_id)
                            titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[2:]))

                        elif sms == 'назад' and 'выбрать заголовок' in get_user_status_stage(user_id):
                            back_page(user_id)
                            titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[2:]))  

                        elif 'set_tit' in get_user_status_stage(user_id):
                            title = ' '.join(get_user_status_stage(user_id).split()[2:])
                            write_msg(user_id, 'Записал', main_keyboards[get_role(user_id)], avatars_with_topic[get_topics(title)][-1])
                            change_title(title, original_text) 
                            set_user_status(user_id, '')
                            set_user_status_stage(user_id, '')
                            set_page(user_id)
                #текст
                    elif sms == 'текст' and get_user_status_stage(user_id) == 'choose' or 'текст' in get_user_status_stage(user_id):
                        
                        if get_user_status_stage(user_id) == 'choose':
                            set_user_status_stage(user_id, 'choos_topic текст')
                            write_msg(user_id, 'Выбери тему новости', generate_keyboard(user_id), attachment = random.choice(avatars)[-1])

                        elif 'choos_topic' in get_user_status_stage(user_id):
                            topic = sms
                            if get_col_column(topic) != 0:
                                titles = before_get_news(get_page(user_id), topic)
                                set_user_status_stage(user_id, 'выбрать текст'+' '+topic)
                            else:
                                write_msg(user_id, 'Тут новостей нет', main_keyboards[get_role(user_id)], avatars_with_topic[topic][2])
                                set_user_status(user_id, '')
                                set_user_status_stage(user_id, '') 
                                set_page(user_id)   

                        elif sms.isdigit() and 'выбрать текст' in get_user_status_stage(user_id):
                            write_msg(user_id, 'Вот что было раньше:')
                            title = get_news(sms, titles)
                            set_user_status_stage(user_id, 'текст set_tex' + ' ' + title)
                            write_msg(user_id, *get_text(title), attachment=get_img(title))
                            write_msg(user_id, 'Теперь напиши изменённую новость', attachment = avatars_with_topic[get_topics(title)][3])

                        elif sms == 'далее' and 'выбрать текст' in get_user_status_stage(user_id):
                            next_page(user_id)
                            titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[2:]))

                        elif sms == 'назад' and 'выбрать текст' in get_user_status_stage(user_id):
                            back_page(user_id)
                            titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[2:]))

                        elif 'set_tex' in get_user_status_stage(user_id):
                            title = ' '.join(get_user_status_stage(user_id).split()[2:])
                            set_text(title, original_text)
                            write_msg(user_id, 'Записал', main_keyboards[get_role(user_id)], avatars_with_topic[get_topics(title)][0])
                            set_user_status(user_id, '')
                            set_user_status_stage(user_id, '')
                            set_page(user_id)
                #удалить
                    elif sms == 'удалить новость' and get_user_status_stage(user_id) == 'choose' or 'удалить' in get_user_status_stage(user_id):

                        if get_user_status_stage(user_id) == 'choose':   
                            set_user_status_stage(user_id, 'choos_topic удалить')
                            write_msg(user_id, 'Выбери тему новости', generate_keyboard(user_id), attachment = random.choice(avatars)[-1])

                        elif 'choos_topic' in get_user_status_stage(user_id):
                            topic = sms
                            if get_col_column(topic) != 0:
                                titles = before_get_news(get_page(user_id), topic)
                                set_user_status_stage(user_id, 'удалить'+' '+topic)
                            else:
                                write_msg(user_id, 'Тут новостей нет', main_keyboards[get_role(user_id)], avatars_with_topic[topic][2])
                                set_user_status(user_id, '')
                                set_user_status_stage(user_id, '')
                                set_page(user_id)      

                        elif sms.isdigit() and 'удалить' in get_user_status_stage(user_id):
                            title = get_news(sms, titles)
                            write_msg(user_id, 'Удалил', keyboard=main_keyboards[get_role(user_id)], attachment = avatars_with_topic[get_topics(title)][1]) 
                            del_news(title)
                            set_user_status(user_id, '')
                            set_user_status_stage(user_id, '')
                            set_page(user_id)
                            

                        elif sms == 'далее' and 'удалить' in get_user_status_stage(user_id):
                            next_page(user_id)
                            titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[1:]))

                        elif sms == 'назад' and 'удалить' in get_user_status_stage(user_id):
                            back_page(user_id)
                            titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[1:]))

                ##################
                #запостить новость в группу
                ##############

                elif (sms == 'запостить новость в группу' or get_user_status(user_id) == 'post') and get_role(user_id) == 2:

                    if get_user_status_stage(user_id) == '':   
                        set_user_status_stage(user_id, 'choos_topic')
                        set_user_status(user_id, 'post')
                        write_msg(user_id, 'Выбери тему новости', generate_keyboard(user_id))  

                    elif 'choos_topic' in get_user_status_stage(user_id):
                        topic = sms
                        if get_col_column(topic) != 0:
                            titles = before_get_news(get_page(user_id), topic)
                            set_user_status_stage(user_id, 'post' +' '+ topic)
                        else:
                            write_msg(user_id, 'Новостей пока нет', main_keyboards[get_role(user_id)], random.choice(avatars_with_topic[topic]))
                            set_user_status(user_id, '')
                            set_user_status_stage(user_id, '')
                            set_page(user_id)

                    elif sms == 'далее' and 'post' in get_user_status_stage(user_id):
                        next_page(user_id)
                        titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[1:]))

                    elif sms == 'назад' and 'post' in get_user_status_stage(user_id):
                        back_page(user_id)
                        titles = before_get_news(get_page(user_id), ' '.join(get_user_status_stage(user_id).split()[1:]))   

                    elif sms.isdigit() and 'post' in get_user_status_stage(user_id):
                        title = get_news(sms, titles)
                        post_to_wall(title, *get_text(title), *get_img(title))
                        set_user_status(user_id, '')
                        set_user_status_stage(user_id, '')
                        set_page(user_id)
                        write_msg(user_id, 'Запостил', keyboard=main_keyboards[get_role(user_id)], attachment=random.choice(avatars_with_topic[get_topics(title)]))  
        ###########################################################
                # error
        ########################################################### 
            
                else:
                    write_msg(user_id, error, main_keyboards[get_role(user_id)])
            '''except:
                set_user_status(user_id, '')
                set_user_status_stage(user_id, '')   
                write_msg(user_id, error, main_keyboards[get_role(user_id)])  '''