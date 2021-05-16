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
    post = requests.get('https://api.vk.com/method/wall.post', params={'access_token': access_token, 'owner_id': -204094421, 'message':title.upper()+'\n'+'\n'+text, 'attachment':attachment,'v': 5.21}).json()
                                                                                                                                                                                                                         

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
        requests.get('https://api.vk.com/method/wall.post', params={'access_token': access_token, 'owner_id': -204094421, 'message':title.upper()+'\n'+'\n'+text, 'v': 5.21}).json()
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

def register_new_user(user_id):
    c.execute("INSERT INTO users(user_id, status, status_stage, page) VALUES (%d, '%s', '%s', %d)" % (user_id, '', '', 0))
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
    return result[0]

##################    
#news   
################# 

def get_title(user_id):
    c.execute("SELECT title FROM news WHERE text='%s' AND user_id=%d" % ('', user_id))
    return c.fetchone()[0]

def get_text(title):
    c.execute("SELECT text FROM news WHERE title='%s'" % title)
    return c.fetchone()

def get_img(title):
    c.execute("SELECT attachments FROM news WHERE title='%s'" % title)
    return c.fetchone()    

def get_col_column():
    c.execute("SELECT COUNT(*) FROM news")
    result = c.fetchone()[0]
    return result

def get_titles():
    c.execute("SELECT title FROM news ORDER BY likes COLLATE RTRIM DESC;")
    result, lst = c.fetchall(), []
    for i in range(len(result)):
        lst.append(str(i+1) +'. ' + str(*result[i]) + ' ' + str(*get_col_like(str(*result[i]))) + ' &#128077;')
    return lst

def set_title(user_id, title):
    c.execute("INSERT INTO news(user_id, title, text, likes, attachments, album) VALUES (%d, '%s', '%s', %d, '%s', '%s')" % (user_id, title, '', 0, '', ''))
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

def get_news(num, titles):
    for i in titles:
        if i.split('.')[0] == num:
            title = ' '.join(i.split()[1:-2])      
    return title

def before_get_news(page):
    keyboard = VkKeyboard(one_time=True)
    for i in range(page*5 + 1, get_col_column()+1):    
        if i % 5 == 0:
            keyboard.add_line()
            if page > 0:
                keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
            break
        keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
        if i == get_col_column() and i > 5 and page > 0:
            keyboard.add_line()
            keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
    if get_col_column()>(page+1)*5:
        keyboard.add_button('Далее', color=VkKeyboardColor.PRIMARY)        
    titles = get_titles()
    write_msg(user_id, 'Выбери новость\n' + '\n'.join(titles[page*5:(page+1)*5]), keyboard)  
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


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        sms = event.text.lower()
        if not check_if_exists(user_id):
            register_new_user(user_id)
        if sms == 'начать':
            write_msg(user_id, 'Привет', keyboard_1)       
###########################################################
        #новая новость
###########################################################
        elif sms == 'добавить новость' or get_user_status(user_id) == 'add':
            if get_user_status_stage(user_id) == '':
                write_msg(user_id, 'Напиши заголовок:')
                set_user_status_stage(user_id, 'set_tit')
                set_user_status(user_id, 'add')

            elif get_user_status_stage(user_id) == 'set_tit':
                set_title(user_id, sms)
                write_msg(user_id, 'Теперь напиши саму новость')
                set_user_status_stage(user_id, 'set_tex' + ' ' + sms)
 
            elif 'set_tex' in get_user_status_stage(user_id):
                set_text(get_title(user_id), sms)
                write_msg(user_id, 'Хочешь добавить картинку к новости?', keyboard_bool)
                set_user_status_stage(user_id, 'choose' + ' ' + get_user_status_stage(user_id).split()[-1])

            elif sms == 'да' and 'choose' in get_user_status_stage(user_id):
                write_msg(user_id, 'Отправь изображение')
                set_user_status_stage(user_id, 'set_img'+ ' ' + get_user_status_stage(user_id).split()[-1])

            elif 'set_img' in get_user_status_stage(user_id):   
                result = vk_session.method("messages.getById", {"message_ids": [event.message_id]})
                photo = result['items'][0]['attachments'][0]['photo']
                attachment = "photo{}_{}_{}".format(photo['owner_id'], photo['id'], photo['access_key'])
                set_attachments(get_user_status_stage(user_id).split()[-1], attachment)
                set_user_status(user_id, '')
                set_user_status_stage(user_id, '')
                write_msg(user_id, 'Новость записал', keyboard_1)
                
            elif sms == 'нет' and 'choose' in get_user_status_stage(user_id):
                set_user_status(user_id, '')
                set_user_status_stage(user_id, '')
                write_msg(user_id, 'Новость записал', keyboard_1)  

###########################################################
        #выдать новость и поставить лайк
###########################################################
        elif sms == 'новости' or get_user_status(user_id) == 'give':
            if get_user_status_stage(user_id) == '':
                set_user_status_stage(user_id, 'choose')
                set_user_status(user_id, 'give')
                if get_col_column() != 0:
                    titles = before_get_news(get_page(user_id))
                else:
                    write_msg(user_id, 'Новостей пока нет', keyboard_1)
                
            elif sms.isdigit() and get_user_status_stage(user_id) == 'choose':
                title = get_news(sms, titles)
                write_msg(user_id, *get_text(title), attachment=get_img(title))
                if not check_if_like(title, user_id):
                    write_msg(user_id, 'Оцени новость', keyboard = keyboard_assessment)
                    set_user_status_stage(user_id, 'appraise' + ' '+ title)
                else:
                    set_user_status(user_id, '')
                    set_user_status_stage(user_id, '')
                    write_msg(user_id, 'Спасибо за просмотр', keyboard = keyboard_1) 

            elif sms == 'далее' and get_user_status_stage(user_id) == 'choose':
                next_page(user_id)
                titles = before_get_news(get_page(user_id))
            elif sms == 'назад' and get_user_status_stage(user_id) == 'choose':
                back_page(user_id)
                titles = before_get_news(get_page(user_id))           
            elif sms == 'понравилась' and 'appraise' in get_user_status_stage(user_id):
                set_likes(get_user_status_stage(user_id).split()[-1])
                user_do_like(get_user_status_stage(user_id).split()[-1], user_id)
                set_user_status(user_id, '')
                set_user_status_stage(user_id, '')
                write_msg(user_id, 'Спасибо за оценку', keyboard = keyboard_1)
            elif sms == 'не понравилась' and 'appraise' in get_user_status_stage(user_id):
                write_msg(user_id, 'Спасибо за оценку', keyboard = keyboard_1)
                set_user_status(user_id, '')
                set_user_status_stage(user_id, '')

               

###########################################################
        # изменить новость
###########################################################          

        elif sms == 'изменить новость' or get_user_status(user_id) == 'change':
            if get_user_status_stage(user_id) == '':
                write_msg(user_id, 'Что ты хочешь поменять?', keyboard=keyboard_change)
                set_user_status(user_id, 'change')
                set_user_status_stage(user_id, 'choose')



        #заголовок        
            elif sms == 'заголовок' and get_user_status_stage(user_id) == 'choose' or 'заголовок' in get_user_status_stage(user_id):
                if get_user_status_stage(user_id) == 'choose':
                    titles = before_get_news(get_page(user_id))
                    set_user_status_stage(user_id, 'выбрать заголовок')

                elif sms.isdigit() and get_user_status_stage(user_id) == 'выбрать заголовок':
                    title = get_news(sms, titles)
                    write_msg(user_id, 'Напиши изменённый заголовок')     
                    set_user_status_stage(user_id, 'заголовок set_tit' + ' ' + title)

                elif sms == 'далее' and get_user_status_stage(user_id) == 'выбрать заголовок':
                    next_page(user_id)
                    titles = before_get_news(get_page(user_id))

                elif sms == 'назад' and get_user_status_stage(user_id) == 'выбрать заголовок':
                    back_page(user_id)
                    titles = before_get_news(get_page(user_id))  

                elif 'set_tit' in get_user_status_stage(user_id):
                    change_title(get_user_status_stage(user_id).split()[-1], sms) 
                    write_msg(user_id, 'Записал', keyboard_1)  
                    set_user_status(user_id, '')
                    set_user_status_stage(user_id, '')
        #текст
            elif sms == 'текст' and get_user_status_stage(user_id) == 'choose' or 'текст' in get_user_status_stage(user_id):
                if get_user_status_stage(user_id) == 'choose':
                    set_user_status_stage(user_id, 'выбрать текст')
                    titles = before_get_news(get_page(user_id))

                elif sms.isdigit() and get_user_status_stage(user_id) == 'выбрать текст':
                    write_msg(user_id, 'Вот что было раньше:')
                    title = get_news(sms, titles)
                    set_user_status_stage(user_id, 'текст set_tex' + ' ' + title)
                    write_msg(user_id, *get_text(title), attachment=get_img(title))
                    write_msg(user_id, 'Теперь напиши изменённую новость')

                elif sms == 'далее' and get_user_status_stage(user_id) == 'выбрать текст':
                    next_page(user_id)
                    titles = before_get_news(get_page(user_id))

                elif sms == 'назад' and get_user_status_stage(user_id) == 'выбрать текст':
                    back_page(user_id)
                    titles = before_get_news(get_page(user_id))

                elif 'set_tex' in get_user_status_stage(user_id):
                    set_text(get_user_status_stage(user_id).split()[-1], sms)
                    write_msg(user_id, 'Записал', keyboard_1)
                    set_user_status(user_id, '')
                    set_user_status_stage(user_id, '')
        #удалить
            elif sms == 'удалить новость' and get_user_status_stage(user_id) == 'choose' or 'удалить' in get_user_status_stage(user_id):
                if get_user_status_stage(user_id) == 'choose':   
                    titles = before_get_news(get_page(user_id))
                    set_user_status_stage(user_id, 'удалить')
                elif sms.isdigit() and get_user_status_stage(user_id) == 'удалить':
                    title = get_news(sms, titles)
                    del_news(title)
                    set_user_status(user_id, '')
                    set_user_status_stage(user_id, '')
                    write_msg(user_id, 'Удалил', keyboard=keyboard_1) 

                elif sms == 'далее' and get_user_status_stage(user_id) == 'удалить':
                    next_page(user_id)
                    titles = before_get_news(get_page(user_id))

                elif sms == 'назад' and get_user_status_stage(user_id) == 'удалить':
                    back_page(user_id)
                    titles = before_get_news(get_page(user_id)) 

        ##################
        #запостить новость в группу
        ##############

        elif sms == 'запостить новость в группу' or get_user_status(user_id) == 'post':
            if get_user_status_stage(user_id) == '':   
                titles = before_get_news(get_page(user_id))
                set_user_status(user_id, 'post')
                set_user_status_stage(user_id, 'post')
            elif sms == 'далее' and get_user_status_stage(user_id) == 'post':
                next_page(user_id)
                titles = before_get_news(get_page(user_id))
            elif sms == 'назад' and get_user_status_stage(user_id) == 'post':
                back_page(user_id)
                titles = before_get_news(get_page(user_id))   
            elif sms.isdigit() and get_user_status_stage(user_id) == 'post':
                title = get_news(sms, titles)
                post_to_wall(title, *get_text(title), *get_img(title))
                set_user_status(user_id, '')
                set_user_status_stage(user_id, '')
                write_msg(user_id, 'Запостил', keyboard=keyboard_1)      
###########################################################
        # error
###########################################################     
        else:
            write_msg(user_id, error, keyboard_1)  
          
