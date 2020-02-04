import vk_api
import time
import random
import pickle
import configparser
import os
#кастом
import X_and_zero

 

def tab_format_get(config):             #составление таблицы для крестиков ноликов 
    text = ''
    

    

    for i in range(0,3):
        if config_get(config,"Game_X_and_O", str(i)+"0") == '0':
            text += ' . |'
        elif config_get(config,"Game_X_and_O", str(i)+"0") == '1':
            text += 'X|'
        elif config_get(config,"Game_X_and_O", str(i)+"0") == '2':
            text += '0|'

        if config_get(config,"Game_X_and_O", str(i)+"1") == '0':
            text += ' . |'
        elif config_get(config,"Game_X_and_O", str(i)+"1") == '1':
            text += 'X|'
        elif config_get(config,"Game_X_and_O", str(i)+"1") == '2':
            text += '0|'

        if config_get(config,"Game_X_and_O", str(i)+"2") == '0':
            text += ' . '
        elif config_get(config,"Game_X_and_O", str(i)+"2") == '1':
            text += 'X'
        elif config_get(config,"Game_X_and_O", str(i)+"2") == '2':
            text += '0'
        text += "\n"
    text += "\n"
    


    return text  

def tab_format_tab_get(config):
    tab = [
        [
            int(config_get(config,"Game_X_and_O", "00", "0")),
            int(config_get(config,"Game_X_and_O", "01", "0")),
            int(config_get(config,"Game_X_and_O", "02", "0"))
        ],[
            int(config_get(config,"Game_X_and_O", "10", "0")),
            int(config_get(config,"Game_X_and_O", "11", "0")),
            int(config_get(config,"Game_X_and_O", "12", "0"))
        ],[
            int(config_get(config,"Game_X_and_O", "20", "0")),
            int(config_get(config,"Game_X_and_O", "21", "0")),
            int(config_get(config,"Game_X_and_O", "22", "0"))
        ]]
    return tab

def new_config(path,id):
    config = configparser.ConfigParser()

    config.add_section("Info")
    config.set("Info","id",str(id))
    try:
        info_users = vk.method('users.get',{'user_ids': id })
    except Exception as e:
        print("ERRORE в взятии о пользователе: ",e)
    else:
        pass
    config.set("Info","first_name", info_users[0]['first_name'])
    config.set("Info","last_name", info_users[0]['last_name'])
    config.set("Info","bugs", "0")

    config.add_section("Settings")
    config.set("Settings", "status", "user")

    config.add_section("Game_X_and_O")
    config.set("Game_X_and_O", "player", "1")
    config.set("Game_X_and_O", "00", "0")
    config.set("Game_X_and_O", "01", "0")
    config.set("Game_X_and_O", "02", "0")

    config.set("Game_X_and_O", "10", "0")
    config.set("Game_X_and_O", "11", "0")
    config.set("Game_X_and_O", "12", "0")

    config.set("Game_X_and_O", "20", "0")
    config.set("Game_X_and_O", "21", "0")
    config.set("Game_X_and_O", "22", "0")

    config.add_section("Menu select")
    config.set("Menu select", "select", "menu")
    
    with open(path, "w") as config_file:
        config.write(config_file)

def config_get(config,section,option,option_default = -1):
    
    if config.has_section(str(section)):
        if config.has_option(str(section),str(option)):
            pass
        else:
            config.set(str(section),str(option),str(option_default))

            with open(path, "w") as config_file:
                config.write(config_file)

    else:
        config.add_section(str(section))
        config.set(str(section),str(option),str(option_default))

        with open(path, "w") as config_file:
            config.write(config_file)
    return config.get(section,option)

def message_to_admin(message, message_from = "BOT"):
    if len(message) > 4000:
        text_message_out = message[0:4000]
    
    message = "Cообщение от " + message_from + "\n" + time.ctime() + "\n" + message
    

    k = 0
    flag_message_send = True
    while flag_message_send == True:

        try:
                send_otvet = vk.method("messages.send", {"peer_id":158661601,"message":message,"random_id":random.randint(-9223372036854775800, 9223372036854775800)})
                time.sleep(5)
                    
        except Exception as e:
                print("ERRORE при отсылкии сообщений to admin: ",e)
                time.sleep(2)
                k = k + 1
                if k > 20:        #если сообщение не отправляется 
                    break
        else:      
            print(time.ctime() , ' отправлено сообщение to admin: ' , message)
            flag_message_send = False

def get_argument(message):
    message_list = message.split(" ")
    i = 0

    for i in range(len(message_list) - 1, 0 , -1):
        if message_list[i] == '':
            del message_list[i]

    return message_list


__version__ = '0.1'
__path__ = r"D:\Данные VK BOT"


int_in_tab = {1:"00",2:"01",3:"02",4:"10",5:"11",6:"12",7:"20",8:"21",9:"22"}

print ("запуск программы")

vk= vk_api.VkApi(token = 'c34796393d7c9ef655bf04238498fb78b74632ce39b0f9f749b3b6c5c00e20fd95b62f728ba86bf7d833b')

error = True
while error:           #проверка регестрации 
    try:
        messages = vk.method('messages.getConversations',{'offset': 0 , "count": 2, "filter":"all"})
    except Exception as e:
        print("ERRORE при регистрации: ",e)
        time.sleep(5)
    else:
        print('авторизация удачна')
        error = False
        time.sleep(1)  

bot_off_on = True
bot_off_on_full = True
count_message_answered = 0

while bot_off_on_full:
    try:
        messages = vk.method('messages.getConversations',{'offset': 0 , "count": 20, "filter":"all"})
    except Exception as e:
        print("ERRORE в приёме сообщений: ",e)
        time.sleep(2)

    else:
        pass

    if "unread_count" in messages:
        print(time.ctime(),'непрочитанных',messages["unread_count"])
        unread = messages["unread_count"]
        unread_messages = vk.method('messages.getConversations',{'offset': 0 , "count": 199, "filter":"unread"})           
    else:
        unread = 0
        time.sleep(1)

    if unread > 199:
        unread = 199


    if unread > 0:
        for i in range(0, unread):
                
            id = unread_messages["items"][i]["last_message"]['from_id']
            text_message_in = unread_messages["items"][i]["last_message"]['text']
            text_message_out = 'no message >> bag'
            flag_message_send = True                                                #не на все сообщения нужно отвечать 

            print(time.ctime() , ' В ответ на ' , text_message_in , 'от ' , id)

            path = __path__+ chr(92) + str(id) + ".ini"
            
            

            if not os.path.exists(path):
                print("создаю новый профиль на " + str(id))
                new_config(path,id)
            
            if ["//выключись","//выкл","//вырубайся"].count(text_message_in.lower()) != 0:
                config = configparser.ConfigParser()
                config.read(path)

                if config_get(config,"Settings","status") == "admin":
                    if bot_off_on == True:
                        bot_off_on = False
                        text_message_out = "Выключение " + time.ctime()
                        print("Выключение " + time.ctime())
                    else:
                        text_message_out = "Бот уже выключен " + time.ctime()
                else:
                    text_message_out = "У вас не достаточно прав"

            elif text_message_in.startswith("/написать разработчику"):
                    if len(text_message_in) >= 23:
                        if len(text_message_in[23:]) > 1:
                            config = configparser.ConfigParser()
                            config.read(path)

                            message_to_admin(text_message_in,"[id{0}|{1}]".format(id, config_get(config,"Settings", "status")))
                            text_message_out = "Сообщение отправлено разработчику"
                        else:
                            text_message_out = "Введите сообщение после команды /написать разработчику"
                    else:
                        text_message_out = "Введите сообщение после команды /написать разработчику"

            elif ["//включись","//вкл","//врубайся"].count(text_message_in.lower()) != 0:
                config = configparser.ConfigParser()
                config.read(path)

                if config_get(config,"Settings","status") == "admin":
                    if bot_off_on == False:
                        bot_off_on = True
                        text_message_out = "Включение " + time.ctime()
                        print("Включение " + time.ctime())
                    else:
                        text_message_out = "Бот уже включен " + time.ctime()
                else:
                    text_message_out = "У вас не достаточно прав"

            elif ["//полностью вырубись","//полный выкл","//полностью выключайся"].count(text_message_in.lower()) != 0:
                if [158661601,138818604].count(id) != 0:
                    text_message_out = "//понял выключаюсь полностью "
                    bot_off_on_full = False
                else:
                    text_message_out = "/Access is denied/"
           
            elif ["//тест","//test","//work?"].count(text_message_in.lower()) != 0:
                if bot_off_on == True:
                    text_message_out = "Бот работает \n"
                else:
                     text_message_out = "Бот выключен \n"

                text_message_out += "\n Бот за этот сеанс ответил на {0} сообщений".format(count_message_answered)

            elif text_message_in.startswith("//добавить багов"):
                config = configparser.ConfigParser()
                config.read(path)
                if config_get(config,"Settings", "status") == "admin":
                    argument_list = get_argument(text_message_in)
                    if len(argument_list) == 4:
                        if argument_list[2].isdigit() and argument_list[3].isdigit(): 
                            path_target = __path__+ chr(92) + str(argument_list[2]) + ".ini"
                            if os.path.exists(path_target):
                                config_target = configparser.ConfigParser()
                                config_target.read(path_target)
                                text_message_out = "Меняю баги [id{0}|{1}] ".format(argument_list[2], config_get(config_target,"Settings", "status")) 
                                text_message_out += "с {0} на {1}".format(config_get(config_target,"Info", "bugs"),str(int(config_get(config_target,"Info", "bugs")) + int(argument_list[3])))
                                config.set("Info", "bugs",str(int(config_get(config_target,"Info", "bugs")) + int(argument_list[3])))
                                with open(path_target, "w") as config_file:
                                    config_target.write(config_file)
                            else:
                                text_message_out = "Про пользователя нет данных"                            
                        else:
                            text_message_out = "Неверные аргументы"
                    else:
                        text_message_out = "Неверное количество аргументов"                   
                else:
                    text_message_out = "У вас не достаточно прав"

            elif text_message_in.startswith("//убавить багов"):
                config = configparser.ConfigParser()
                config.read(path)
                if config_get(config,"Settings", "status") == "admin":
                    argument_list = get_argument(text_message_in)
                    if len(argument_list) == 4:
                        if argument_list[2].isdigit() and argument_list[3].isdigit(): 
                            path_target = __path__+ chr(92) + str(argument_list[2]) + ".ini"
                            if os.path.exists(path_target):
                                config_target = configparser.ConfigParser()
                                config_target.read(path_target)
                                text_message_out = "Меняю баги [id{0}|{1}] ".format(argument_list[2], config_get(config_target,"Settings", "status")) 
                                text_message_out += "с {0} на {1}".format(config_get(config_target,"Info", "bugs"),str(int(config_get(config_target,"Info", "bugs")) - int(argument_list[3])))
                                config.set("Info", "bugs",str(int(config_get(config_target,"Info", "bugs")) - int(argument_list[3])))
                                with open(path_target, "w") as config_file:
                                    config_target.write(config_file)
                            else:
                                text_message_out = "Про пользователя нет данных"                            
                        else:
                            text_message_out = "Неверные аргументы"
                    else:
                        text_message_out = "Неверное количество аргументов"                   
                else:
                    text_message_out = "У вас не достаточно прав"

            elif   bot_off_on == True:                                            #общественая часть 
                path = __path__+ chr(92) + str(id) + ".ini"
                config = configparser.ConfigParser()
                config.read(path)
                if ["хелп","/help","что можешь?"].count(text_message_in.lower()) != 0:
                     text_message_out = '''Я пока мало что могу :-( \n  
/профиль \n/написать разработчику (текст)  \n/тихо \n/игра (новое!)(нестабильное) \n
//выключись \n //включись \n//тест \n //добавить багов (id) (count)\n //убавить багов (id) (count)\n 
//полностью выключайся\n'''

                elif ["/кто я?","/профиль","/я"].count(text_message_in.lower()) != 0:                    

                    text_message_out = "id = " + config_get(config,"Info", "id") +'\n'
                    text_message_out += "Name = " + config_get(config,"Info", "last_name") + " " + config_get(config,"Info", "first_name") +'\n'
                    text_message_out += "\nStatys = " + config_get(config,"Settings", "status")
                    text_message_out += "\nBug = " + config_get(config,"Info", "bugs", 0)

                elif ["/по тихому","/тихо","/тиха"].count(text_message_in.lower()) != 0:
                    flag_message_send = False

                elif ["/игра","/game","/играть"].count(text_message_in.lower()) != 0:      #в разработке
                    

                    if config.has_section("Game_X_and_O"):
                        pass
                    else:
                        config.add_section("Game_X_and_O")
                    config.set("Game_X_and_O", "player", "1")
                    config.set("Game_X_and_O", "00", "0")
                    config.set("Game_X_and_O", "01", "0")
                    config.set("Game_X_and_O", "02", "0")

                    config.set("Game_X_and_O", "10", "0")
                    config.set("Game_X_and_O", "11", "0")
                    config.set("Game_X_and_O", "12", "0")

                    config.set("Game_X_and_O", "20", "0")
                    config.set("Game_X_and_O", "21", "0")
                    config.set("Game_X_and_O", "22", "0")

                    if config.has_section("Menu select"):
                        pass
                    else:
                        config.add_section("Menu select")
                    config.set("Menu select", "select", "game")

                    text_message_out = tab_format_get(config)      
                    text_message_out += '\n \nВведите число клетки в которую хотите поставить X \n 1|2|3 \n 4|5|6 \n 7|8|9 '
                    text_message_out += "\n \nДля выхода из игры наберите /выход"

                    with open(path, "w") as config_file:
                        config.write(config_file)

                elif text_message_in.lower().startswith("/выход"):

                    if config.has_section("Menu select"):
                        pass
                    else:
                        config.add_section("Menu select")
                    config.set("Menu select", "select", "menu")

                    text_message_out = "Хорошо, вы в меню"

                    with open(path, "w") as config_file:
                        config.write(config_file)

                elif text_message_in.isdigit() and config_get(config,"Menu select", "select", "menu") == "game":
                    

                    
                    if int(text_message_in) > 0 and int(text_message_in) < 10:
                        if config_get(config,"Game_X_and_O", int_in_tab[int(text_message_in)]) == "0":
                            config.set("Game_X_and_O", int_in_tab[int(text_message_in)], "1")
                            in_put = X_and_zero.game(tab_format_tab_get(config),2)

                            if in_put["info"] == 0:
                                config.set("Game_X_and_O", str(in_put["out"]["y"])+str(in_put["out"]["x"]), "2")
                                text_message_out = tab_format_get(config)
                            else:
                                if in_put["info"] == "1 game end" and in_put["winner"] != 0:
                                    if in_put["winner"] == 2:
                                        text_message_out = "Я выиграл, напишите /игра для того чтобы отыграться)"
                                    if in_put["winner"] == 1:
                                        text_message_out = "Ты выиграл, напишите /игра для новой игры"


                                else:
                                    text_message_out = "Ничья, напишите /игра для новой игры"                          


                        else:
                            text_message_out = "Поле занято"
                    else:
                        text_message_out = "такого поля пока нет"





                    with open(path, "w") as config_file:
                        config.write(config_file)  #нужно будет перестроить центральную структуру 

                else:
                    #if id == 138818604:
                    text_message_out = "Извините но такой команды нет \n Вы можите написать /help для вывода списка команд"                          #общественная часть 
                    #text_message_out = "такой команды нет \n Напишите /help для вывода списка команд"
            
            else:
                text_message_out = "Бот выключен"
                
               

            k = 0;
            if flag_message_send == False:
                try:
                    print("Прочитано сообщение" + str(unread_messages["items"][i]["last_message"]['id']))
                    vk.method("messages.markAsRead", {"peer_id": id})
                except Exception as e:
                    print("ERRORE при прочтений сообщений: ",e)
                    time.sleep(2)
                else:
                    pass

            while flag_message_send == True:
                if len(text_message_out) > 4095:
                    text_message_out = text_message_out[0:4095]
                    print("сообщение вышло за пределы")

                try:
                     send_otvet = vk.method("messages.send", {"peer_id":id,"message":text_message_out,"random_id":random.randint(-9223372036854775800, 9223372036854775800)})
                     time.sleep(1)
                    
                except Exception as e:
                     print("ERRORE при отсылкии сообщений: ",e)
                     time.sleep(2)
                     k = k + 1
                     if k > 5:        #если сообщение не отправляется 
                         break
                else:      
                    print(time.ctime() , ' отправлено сообщение: ' , text_message_out)
                    flag_message_send = False

            count_message_answered += 1



#нужно будет перестроить центральную структуру
