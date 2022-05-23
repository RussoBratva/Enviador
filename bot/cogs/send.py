from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.database import *
import os
import asyncio


def send(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    user_info = ''
    id = ''

    if not query == None:
        user_info = query.from_user
        id = str(user_info['id'])
    query2 = update.callback_query
    query_data = ''
    
    if not query2 == None:
        query_data = query2.data
    
    if not query_data == 'delete_message':
        keyboard = [[InlineKeyboardButton(f'🗑️ {button_delete_message}', callback_data='delete_message')]]
        continuar = False
        if id in donos:
            doc = update.message.document
            photo = update.message.photo
            video = update.message.video
            audio = update.message.audio
            
            texto = update.message.text

            if texto is None:
                texto = update.message.caption
                
                for command in send_command:
                    comando = '/'+command
                    if comando in texto:
                        continuar = True
                        break

            if texto.split()[0].replace('/', '') in send_command:
                if continuar or doc == None or video == None or audio == None or photo == []:
                    for command in send_command:
                        comando = '/'+command+' '
                        comando2 = '/'+command
                        texto = texto.replace(comando, '')
                        texto = texto.replace(comando2, '')
                    
                    if not texto.strip() == '' or not doc is None or not video is None or not audio is None or photo is not []:
                        contador_erro = 0
                        contador_enviado = 0

                        messages = []
                        m3 = query.bot.send_message(chat_id=id, text='📤 | *Envio de mensagem*\n\nEnviando mensagem!', parse_mode='Markdown')
                        repetidos = []
                        
                        try:
                            if len(texto) < 4000 or not doc is None or not video is None or audio is None or photo is not []: 
                                with open('temp/send.txt', 'w', encoding='UTF-8') as file:
                                    file.write('.')
                                
                                for usuario in asyncio.run(all_users_id()):
                                    try:
                                        if not str(usuario) == str(id) and not str(usuario) in repetidos:
                                            if not video is None:
                                                try:
                                                    m = query.bot.send_video(chat_id=usuario, video=update.message.video.file_id, caption=texto, parse_mode='Markdown')

                                                except:
                                                    m = query.bot.send_video(chat_id=usuario, video=update.message.video.file_id, caption=texto)

                                            elif not doc is None:
                                                try:
                                                    m = query.bot.send_document(chat_id=usuario, document=update.message.document.file_id, caption=texto, parse_mode='Markdown')

                                                except:
                                                    m = query.bot.send_document(chat_id=usuario, document=update.message.document.file_id, caption=texto)
                                            
                                            elif not audio is None:
                                                try:
                                                    m = query.bot.send_audio(chat_id=usuario, audio=update.message.audio.file_id, caption=texto, parse_mode='Markdown')

                                                except:
                                                    m = query.bot.send_audio(chat_id=usuario, audio=update.message.audio.file_id, caption=texto)

                                            elif not photo == []:
                                                try:
                                                    m = query.bot.send_photo(chat_id=usuario, photo=update.message.photo[-1].file_id, caption=texto, parse_mode='Markdown')

                                                except:
                                                    m = query.bot.send_photo(chat_id=usuario, photo=update.message.photo[-1].file_id, caption=texto)

                                            else:
                                                try:
                                                    m = query.bot.send_message(chat_id=usuario, text=texto, parse_mode='Markdown')

                                                except:
                                                    m = query.bot.send_message(chat_id=usuario.replace('*', '').replace('_', '').replace('`', ''), text=texto)

                                            messages.append(tuple((usuario, m.message_id)))
                                            contador_enviado += 1
                                            repetidos.append(str(usuario))
                                            
                                            
                                    except:
                                        contador_erro += 1

                                try:
                                    os.remove('temp/send.txt')
                                except:
                                    pass
                            
                                text = f'📤 | *Mensagem enviada*\n\nA mensagem foi enviada com sucesso!\n\n*Usuários que receberam a mensagem*: `{contador_enviado}`\n*Usuários que não receberam a mensagem*: `{contador_erro}`'
                                context.bot.edit_message_text(chat_id=id, message_id=m3.message_id, text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                id_m = m3.message_id
                                
                                if not messages == []:
                                    lista = {"message": messages, "chat_id": id, "message_id":id_m, "text": text}
                                    write_doc = json.dumps(lista, indent=4)
                                    
                                    with open(f"temp/send-{id_m}.json", "w") as file:
                                        file.write(write_doc)
                            
                            else:
                                query.bot.send_message(chat_id=id, text=f'📤 | *Envio de mensagem*\n\nA mensagem não pode passar de 4000 caracteres por motivos de limitações do Telegram! Por favor, tente reenviar a mensagem com menos texto!', parse_mode='Markdown')

                        except:
                            context.bot.edit_message_text(chat_id=id, message_id=m3.message_id, text='📤 | *Envio de mensagem*\n\nEsse erro pode ocorrer por motivos diversos, como:\n\n*Enviar vários arquivos po mensagem*\n\nTente não enviar vários arquivos ou um album anexados em uma mesma mensagem. Tente enviar 1 arquivo por mensagem!\n\n*Outros motivos*\n\nCaso o seu erro não tenha sido considerado nesta mensagem, entre em contato com o desenvolvedor do bot e vamos investigar esse erro e melhorar o bot!', parse_mode='Markdown')

                    else:
                        query.bot.send_message(chat_id=id, text=f'📤 | *Envio de mensagem*\n\nA mensagem não pode estar vazia. Tente usar o comando novamente com uma mensagem a ser enviada.', parse_mode='Markdown')

    else:
        try:
            with open(f"temp/send-{query2.message.message_id}.json", "r") as file:
                lista = json.loads(file.read())
            contagem_erros = 0
            usuarios = lista['message']
            log = ''
            for usuario in usuarios:
                try:
                    query2.bot.delete_message(chat_id=usuario[0], message_id=usuario[1])

                except:
                    contagem_erros += 1
                
                if contagem_erros > 0:
                    log = f'\n\nMas não foi possivel apagar essa mensagem de `{contagem_erros}` chat(s)'

            context.bot.edit_message_text(chat_id=query2.message.chat_id, message_id=query2.message.message_id, text=f'📤 | *Envio de mensagem*\n\nMensagem apagada!'+log, parse_mode='Markdown')
            os.remove(f"temp/send-{query2.message.message_id}.json")

        except:
            context.bot.edit_message_text(chat_id=query2.message.chat_id, message_id=query2.message.message_id, text=f'📤 | *Envio de mensagem*\n\nNão foi possível apagar essa mensagem!', parse_mode='Markdown')




