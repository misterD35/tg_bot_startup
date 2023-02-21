import os

import aiogram
from aiogram import Bot, types, executor, Dispatcher
import re
from markup import markup
import random


bot = aiogram.Bot(token=token)
dispatcher = aiogram.Dispatcher(bot)

chat_id = open('txt_csv/chat_id_zaprosi.txt', 'r').read()
a = 0

@dispatcher.message_handler(commands='start')
async def start(message):

    button1 = types.KeyboardButton(text="Удалить")
    button2 = types.KeyboardButton(text="Отменить")
    button3 = types.KeyboardButton(text="Заморозить")
    button4 = types.KeyboardButton(text="Переименовать")
    button5 = types.KeyboardButton(text="Покажи столбцы")
    button6 = types.KeyboardButton(text="Удали столбец")

    sp_button = [button1, button2, button3, button4]

    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(*sp_button).add(button5, button6)
    await message.answer("Выбери команду", reply_markup=keyboard1)


@dispatcher.message_handler(content_types=['text'])
async def commands(message):
    flag_cancel, flag_empty = False, False
    if message.text == "Удалить" or message.text == "Отменить" or message.text == "Заморозить" or message.text == "Переименовать" \
            or message.text == "Покажи столбцы" or message.text == "Удали столбец":
        command = None
        if message.text == "Удалить":
            command = 'delete'
        elif message.text == "Отменить":
            command = 'cancel'
            flag_cancel = True
            await message.answer("Отмена запросов в процессе разработки")
        elif message.text == "Заморозить":
            command = 'freeze'
        elif message.text == "Переименовать":
            command = 'rename'
        elif message.text == "Покажи столбцы":
            command = 'покажи столбцы'
            sp_name_column = []
            with open('txt_csv/time_num_zaprosov.csv', 'r') as r_file:  # открываем файл для чтения
                lines = r_file.readlines()  # читаем по строкам и объединяем строки как элементы списка
                if lines != [] and lines != ['\n']:
                    names = lines[0].split(
                        ",")  # разделяем первый элемент списка (1-ю строку) на подэлементы (названия столбцов)
                    for name in range(len(names)):  # прокручиваем список на длину списка названий столбцов
                        if '\n' not in names[name]:
                            combo = names[name]
                        else:
                            combo = names[name][:-1]
                        combo = combo + ' - '
                        space = False
                        for stolb_line in range(len(lines)):
                            row = lines[stolb_line].split(",")  # строка = элементы i-ой строки разделяем запятой
                            if stolb_line == 0:
                                pass
                            elif row[name] == '' or row[name] == '\n':
                                combo = combo + str(stolb_line - 1)
                                space = True
                                break
                        if space == False:
                            combo = combo + str(stolb_line)
                        combo = combo + '\n'
                        sp_name_column.append(combo)
                    f = open("txt_csv/time_num_zaprosov.csv", "rb")
                    await bot.send_document(chat_id, f, caption=''.join(map(str, sp_name_column)))
                else:
                    await message.answer(f"Пусто! \n\nЗапусти запрос в работу")

        elif message.text == "Удали столбец":   # сохраним id пользователя, который хочет удалить столбец для дальнейшего сравнения
            command = 'column_del'
            with open('txt_csv/user_id_column_del.txt', 'w') as f:
                f.write(str(message.from_user.id))

        if command != 'покажи столбцы' and flag_cancel == False:
            with open("txt_csv/command_from_tg.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                file.write(command)

            with open('txt_csv/time_num_zaprosov.csv', 'r') as r_file:  # открываем файл для чтения
                sp_name = []
                # try:
                line = r_file.readline()  # читаем по строкам и объединяем строки как элементы списка
                if line == '' or line == '\n':
                    flag_empty = True
                else:
                    names = line.split(",")  # разделяем первый элемент списка (1-ю строку) на подэлементы (названия столбцов)
                    length_line = len(line.split(","))  # определяем длину 1-ой строки (число столбцов)
                    for name in range(length_line):  # прокручиваем на кол-во линий
                        if '\n' in names[name]:  # если нашли абзац (последний столбец)
                            sp_name.append(names[name][:-1])  # добавляем в список имен 1 из названий столбцов, кроме абзаца
                        else:
                            sp_name.append(names[name])  # если абзаца нет (столбец НЕ последний) - добавляем полное название

            if command != 'column_del':
                if flag_empty == True:
                    await message.answer("Удалять, замораживать и переименовывать будем позднее")
                else:
                    await message.answer("Выбери название запроса", reply_markup=markup(sp_name))
            else:
                if flag_empty == True:
                    await message.answer("Столбцы для удаления отсутствуют")
                else:
                    await message.answer("Выбери столбец для удаления", reply_markup=markup(sp_name))


    elif message.text.lower() == 'id чата':  # запоминание чата и запись id чата в txt файл
        with open('txt_csv/chat_id_zaprosi.txt', 'w') as f:
            f.write(str(message.chat.id))
    elif message.text.lower() == 'старт соoбщений верхнее':
        await bot.delete_message(message.chat.id, message.message_id)   # удаление только что принятого сообщения
        with open('txt_csv/message_id_up.txt', 'w') as f:
            f.write(str(message.message_id+1))
        await bot.send_message(chat_id, 'Принял, стартуем(верхнее)')
        await bot.pin_chat_message(chat_id, int(open('txt_csv/message_id_up.txt', 'r').read()))
    elif message.text.lower() == 'старт соoбщений нижнее':
        await bot.delete_message(message.chat.id, message.message_id)   # удаление только что принятого сообщения
        with open('txt_csv/message_id_down.txt', 'w') as f:
            f.write(str(message.message_id+1))
        await bot.send_message(chat_id, 'Принял, стартуем(нижнее)')
        await bot.pin_chat_message(chat_id, int(open('txt_csv/message_id_down.txt', 'r').read()))
    elif message.text.lower() == '/start2':
        pass
    else:
        with open("txt_csv/command_from_tg.txt", "r", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
            sp_commands = file.readline()
            sp_commands = f'{sp_commands}, {message.text}'
        with open("txt_csv/commands_for_ocherednost_tg.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
            file.write(sp_commands)
        sp_response = ['Новое название внес в базу данных']
        random_index = random.randint(0, len(sp_response) - 1)
        await bot.send_message(chat_id, sp_response[random_index])


@dispatcher.callback_query_handler(lambda call: True)  # на основе док-та markup
async def osnova_callback(call):   # call - это сообщение пользователя в кнопке, которую он нажал
    if call.data.find("Оставляем") == 0:   # если нашли "Оставляем"
        await bot.edit_message_text('Удаление столбца отменено', message_id=call.message.message_id, chat_id=call.message.chat.id)
    elif call.data.find("Удаляем") == 0:   # если нашли "Удаляем"
        id_old_message = open('txt_csv/user_id_column_del.txt', 'r').read()
        if int(call.from_user.id) == int(id_old_message):   # если id пользователя совпадает
            sp_del_or_not = ['Удаляем', 'Оставляем']

            with open('txt_csv/ochered.txt', "r",
                      encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                sp = file.readlines()

            for t in range(len(sp)):  # прокручиваем цикл на длину списка
                sp[t] = sp[t].replace("\n", '')  # заменяем абзац "\n" на пустоту

            with open("txt_csv/sp_name_command.txt", "r", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                names_from_file = file.readlines()

            sp_name_command = []    # наполняем список всеми значениями, содержащими имя запроса
            if names_from_file != []:
                itog_name = None    # вытаскиваем имя запроса без номера
                for q in range(len(names_from_file[0])):
                    if names_from_file[0][q].isdigit() is True:
                        itog_name = names_from_file[0][:q]
                        break

                flag_status, flag_digit = False, False
                for k in range(len(sp)):  # прокручиваем цикл на длину списка
                    if flag_status == True and itog_name in sp[k]:
                        if ('в работе' in sp[k] or 'в ожидании' in sp[k]) and itog_name in sp[k]:
                            index1 = sp[k].index('-')
                            for j in range(index1 + 2, len(sp[k]) - 1):
                                if sp[k][j].isdigit() == True and sp[k][index1 + 2:j] == itog_name:
                                    flag_digit = True
                                elif sp[k][j] == ' ' and flag_digit == True:
                                    sp_name_command.append(sp[k][index1 + 2:j])
                                    break
                    elif sp[k] == 'СТАТУС ЯЧЕЕК:':  # если натыкаемся на список ячеек
                        flag_status = True

            await bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)   # удалить предыдущее сообщение и написать новое (ниже)
            if names_from_file != []:
                await call.message.answer(f"Необходимо подтверждение другого пользователя или отмена \n \nВНИМАНИЕ!!! Будут удалены следующие запросы в работе и в ожидании: {sp_name_command}", reply_markup=markup(sp_del_or_not))
            else:
                await call.message.answer(f"Необходимо подтверждение другого пользователя или отмена \n \nВНИМАНИЕ!!! Запросов в работе и в ожидании нет", reply_markup=markup(sp_del_or_not))

        else:   # если id пользователя НЕ совпадает
            with open("txt_csv/command_from_tg.txt", "r", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                sp_commands = file.readline()

            with open("txt_csv/commands_for_ocherednost_tg.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                file.write(sp_commands)

            await bot.edit_message_text(f'Команду "{sp_commands}" принял', message_id=call.message.message_id, chat_id=call.message.chat.id)    # редактируем сообщение

    elif re.findall('[0-9]+', call.data) != []:    # если в ответе пользователя содержатся числа (запрос номером)
        with open("txt_csv/command_from_tg.txt", "r", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
            sp_commands = file.readline()
            if sp_commands == 'rename':   # если команда rename
                with open("txt_csv/command_from_tg.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                    sp_commands = sp_commands + ' ' + str(call.data)   # добавляем к rename имя запроса (ответ пользователя в тг)
                    file.write(sp_commands)   # запись в файл
                await bot.edit_message_text('Введи новое название запроса', message_id=call.message.message_id, chat_id=call.message.chat.id)   # исправляем сообщение
            elif sp_commands == 'delete':   # если команда delete
                path = os.getcwd() + '\\zaprosi_v_rabote_ozhidanii'
                flag_zapros_found = False
                files = os.listdir(path)  # список названий файлов в директории (без путей)
                for file in files:
                    if flag_zapros_found == True:
                        break
                    elif 'delete' in file:  # если готово удаление
                        file = path + f'\\' + file
                        with open(file, "r", encoding='utf-8') as f:  # читаем файл по строкам и заносим каждую строку в список
                            sp = f.readlines()
                        for stroka_sp in sp:
                            words = stroka_sp.split()
                            if words[3] == call.data:
                                flag_zapros_found = True
                                break
                if flag_zapros_found == False:   # если НЕ нашли
                    sp_commands = str(sp_commands + ' ' + str(call.data))   # прибавляем к delete имя запроса (call.data)
                    with open("txt_csv/commands_for_ocherednost_tg.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим строку в список
                        file.write(sp_commands)
                    await bot.edit_message_text(f'Команду "{sp_commands}" принял!', message_id=call.message.message_id, chat_id=call.message.chat.id)  # исправляем сообщение
                else:   # если нашли - ПОВТОР
                    await bot.edit_message_text(f'Повторный запрос {call.data} скоро будет удален', message_id=call.message.message_id, chat_id=call.message.chat.id)  # исправляем сообщение
            else:   # команды, кроме rename\delete
                sp_commands = str(sp_commands + ' ' + str(call.data))
                await bot.edit_message_text(f'Команду "{sp_commands}" принял', message_id=call.message.message_id, chat_id=call.message.chat.id)  # исправляем сообщение
                with open("txt_csv/commands_for_ocherednost_tg.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим строку в список
                    file.write(sp_commands)

    else:   # если ответ пользователя имя запроса без букв
        with open('txt_csv/time_num_zaprosov.csv', 'r') as r_file:  # открываем файл для чтения
            sp_name = []
            lines = r_file.readlines()[0]  # читаем по строкам и объединяем строки как элементы списка
            names = lines.split(",")  # разделяем первый элемент списка (1-ю строку) на подэлементы (названия столбцов)
            length_lines = len(lines.split(","))  # определяем длину 1-ой строки (число столбцов)
            for name in range(length_lines):  # прокручиваем на кол-во линий
                if '\n' in names[name]:  # если нашли абзац (последний столбец)
                    sp_name.append(names[name][:-1])  # добавляем в список имен 1 из названий столбцов, кроме абзаца
                else:
                    sp_name.append(names[name])  # если абзаца нет (столбец НЕ последний) - добавляем полное название

        with open('txt_csv/ochered.txt', "r", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
            sp = file.readlines()

        for i in range(len(sp)):  # прокручиваем цикл на длину списка
            sp[i] = sp[i].replace("\n", '')  # заменяем абзац "\n" на пустоту

        with open("txt_csv/command_from_tg.txt", "r", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
            sp_commands = file.readline()

        for i in sp_name:
            if call.data == i:   # если содержание кнопки, нажатой пользователем, = одному из элементов списка имен
                sp_name_command = []    # далее ищем имя запроса с числом
                flag_status, flag_digit = False, False
                if sp_commands == "cancel":
                    for k in range(len(sp)):  # прокручиваем цикл на длину списка
                        if flag_status == True and i in sp[k]:
                            if ('в работе' in sp[k] or 'в ожидании' in sp[k]) and i in sp[k]:
                                flag_digit = False
                                index1 = sp[k].index('-')
                                for j in range(index1 + 2, len(sp[k]) - 1):
                                    if sp[k][j].isdigit() == True and sp[k][index1 + 2:j] == i:
                                        flag_digit = True
                                    elif sp[k][j] == ' ' and flag_digit == True:
                                        sp_name_command.append(sp[k][index1 + 2:j])
                                        break
                        elif sp[k] == 'СТАТУС ЯЧЕЕК:':  # если натыкаемся на список ячеек
                            flag_status = True
                elif sp_commands == "delete":

                    for k in range(len(sp)):  # прокручиваем цикл на длину списка
                        if flag_status == True and i in sp[k]:
                            if 'ожидает удаления' in sp[k] or 'в заморозке' in sp[k]:
                                flag_digit = False
                                index1 = sp[k].index('-')
                                for j in range(index1 + 2, len(sp[k]) - 1):
                                    if sp[k][j].isdigit() == True and sp[k][index1 + 2:j] == i:
                                        flag_digit = True
                                    elif sp[k][j] == ' ' and flag_digit == True:
                                        sp_name_command.append(sp[k][index1 + 2:j])
                                        break
                        elif sp[k] == 'СТАТУС ЯЧЕЕК:':  # если натыкаемся на список ячеек
                            flag_status = True
                elif sp_commands == "freeze":
                    for k in range(len(sp)):  # прокручиваем цикл на длину списка
                        if flag_status == True and i in sp[k]:
                            if 'в работе' in sp[k] or 'в ожидании' in sp[k] or 'ожидает удаления' in sp[k]:
                                flag_digit = False
                                index1 = sp[k].index('-')
                                for j in range(index1 + 2, len(sp[k]) - 1):
                                    if sp[k][j].isdigit() == True and sp[k][index1 + 2:j] == i:
                                        flag_digit = True
                                    elif sp[k][j] == ' ' and flag_digit == True:
                                        sp_name_command.append(sp[k][index1 + 2:j])
                                        break
                        elif sp[k] == 'СТАТУС ЯЧЕЕК:':  # если натыкаемся на список ячеек
                            flag_status = True
                elif sp_commands == "rename":
                    for k in range(len(sp)):  # прокручиваем цикл на длину списка
                        if flag_status == True and i in sp[k]:
                            flag_digit = False
                            index1 = sp[k].index('-')
                            for j in range(index1 + 2, len(sp[k]) - 1):
                                if sp[k][j].isdigit() == True and sp[k][index1 + 2:j] == i:
                                    flag_digit = True
                                elif sp[k][j] == ' ' and flag_digit == True:
                                    sp_name_command.append(sp[k][index1 + 2:j])
                                    break
                        elif sp[k] == 'СТАТУС ЯЧЕЕК:':  # если натыкаемся на список ячеек
                            flag_status = True
                elif sp_commands == "column_del":
                    with open("txt_csv/command_from_tg.txt", "r", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                        sp_commands = file.readline()
                        sp_commands = str(sp_commands + ' ' + str(call.data))

                    with open("txt_csv/command_from_tg.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                        file.write(sp_commands)

                    with open('txt_csv/ochered.txt', "r",
                              encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                        sp = file.readlines()

                    for t in range(len(sp)):  # прокручиваем цикл на длину списка
                        sp[t] = sp[t].replace("\n", '')  # заменяем абзац "\n" на пустоту

                    sp_name_command = []
                    flag_status = False
                    for k in range(len(sp)):  # прокручиваем цикл на длину списка
                        if flag_status == True and call.data in sp[k]:
                            flag_digit = False
                            if ('в работе' in sp[k] or 'в ожидании' in sp[k] or 'в заморозке' in sp[k] or 'ожидает удаления' in sp[k]) and call.data in sp[k]:
                                index1 = sp[k].index('-')
                                for j in range(index1 + 2, len(sp[k]) - 1):
                                    if sp[k][j].isdigit() == True and sp[k][index1 + 2:j] == call.data:
                                        flag_digit = True
                                    elif sp[k][j] == ' ' and flag_digit == True:
                                        sp_name_command.append(sp[k][index1 + 2:j])
                                        break
                        elif sp[k] == 'СТАТУС ЯЧЕЕК:':  # если натыкаемся на список ячеек
                            flag_status = True

                    with open("txt_csv/sp_name_command.txt", "w", encoding='utf-8') as file:  # читаем файл по строкам и заносим каждую строку в список
                        for name in range(len(sp_name_command)-1):  # создаем цикл, прокручиваем на длину основного списка - 1
                            file.write(f'{sp_name_command[name]},')  # сначала вносим нулевой элемент списка (первый в работе)
                        if sp_name_command != []:
                            file.write(sp_name_command[len(sp_name_command)-1])

                    sp_del_or_not = ['Удаляем', 'Оставляем']
                    if sp_name_command != []:
                        await bot.edit_message_text(f"ВНИМАНИЕ!!! Следующие запросы находятся в работе и в ожидании: {sp_name_command}. \n \nДождись завершения! Затем продублируй запрос на удаление", message_id=call.message.message_id, chat_id=call.message.chat.id)
                        # await bot.edit_message_text(f"Необходимо подтверждение другого пользователя или отмена \n \nВНИМАНИЕ!!! Будут удалены следующие запросы в работе и в ожидании: {sp_name_command}", reply_markup=markup(sp_del_or_not), message_id=call.message.message_id, chat_id=call.message.chat.id)
                    else:
                        await bot.edit_message_text(f"Необходимо подтверждение другого пользователя или отмена \n \nВНИМАНИЕ!!! Запросов в работе и в ожидании нет", reply_markup=markup(sp_del_or_not), message_id=call.message.message_id, chat_id=call.message.chat.id)

                if sp_commands == "cancel" or sp_commands == "delete" or sp_commands == "freeze" or sp_commands == "rename":
                    if sp_name_command == []:
                        await bot.send_message(chat_id, f'Запросы по команде {sp_commands.upper()} отсутствуют')   # отправляем сообщение
                    else:
                        await bot.edit_message_text("Выбери номер запроса", reply_markup=markup(sp_name_command), message_id=call.message.message_id, chat_id=call.message.chat.id)    # редактируем сообщение

print('Start')
aiogram.executor.start_polling(dispatcher)
