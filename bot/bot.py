from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from bot.cogs.modules.database import *
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.pix_authentication import *
from bot.cogs.modules.pix_key_check import *
from bot.cogs.estatisticas import *
from bot.cogs.ban import *
from bot.cogs.add_cc import *
from bot.cogs.troca import *
from bot.cogs.tools import *
from bot.cogs.add_credits import *
from bot.cogs.add_pix_config import *
from bot.cogs.afilliate import *
from bot.cogs.add_groups import *
from bot.cogs.buy import *
from bot.cogs.cc_main import *
from bot.cogs.delete_account import *
from bot.cogs.dynamic_buttons import *
from bot.cogs.gift import *
from bot.cogs.history import *
from bot.cogs.mix import *
from bot.cogs.profile import *
from bot.cogs.scheduled_tasks import *
from bot.cogs.search import *
from bot.cogs.send import *
from bot.cogs.start import *
from bot.cogs.add_admin import *
from bot.cogs.flags import *
from bot.cogs.users import *
from bot.cogs.delete_card import *
from bot.cogs.backup import *
import json, logging, threading, os, time


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    with open('config/config.json', 'r', encoding="utf8") as file:
        config = json.loads(file.read())
        token_bot = config['token_bot']
    
    print('\nBot online\n')

    while True:
        try:
            updater = Updater(token_bot, use_context=True)
            
           # for command in add_admin_command:
              #  updater.dispatcher.add_handler(CommandHandler(command, add_admin, run_async=True, pass_update_queue=True, pass_job_queue=True))
            
            #for command in remove_admin_command:
               # updater.dispatcher.add_handler(CommandHandler(command, remove_admin, run_async=True, pass_update_queue=True, pass_job_queue=True))
            
            for command in send_command:
                updater.dispatcher.add_handler(CommandHandler(command, send, run_async=True, pass_update_queue=True, pass_job_queue=True))
            
           # for command in start_command:
           #     updater.dispatcher.add_handler(CommandHandler(command, start, run_async=True, pass_update_queue=True, pass_job_queue=True))
            
            #for command in add_credits:
               # updater.dispatcher.add_handler(CommandHandler(command, recarregar, run_async=True, pass_update_queue=True, pass_job_queue=True))

          #  for command in add_cc:
                #updater.dispatcher.add_handler(CommandHandler(command, adicionar_cc, run_async=True, pass_update_queue=True, pass_job_queue=True))

          #  for command in card:
            #    updater.dispatcher.add_handler(CommandHandler(command, cartao, run_async=True, pass_update_queue=True, pass_job_queue=True))

            #for command in help_command_1:
            #    updater.dispatcher.add_handler(CommandHandler(command, help_command, run_async=True, pass_update_queue=True, pass_job_queue=True))

            #for command in edit_prices:
                #updater.dispatcher.add_handler(CommandHandler(command, editar_precos, run_async=True, pass_update_queue=True, pass_job_queue=True))

           # for command in gift_add:
               # updater.dispatcher.add_handler(CommandHandler(command, adicionar_gift, run_async=True, pass_update_queue=True, pass_job_queue=True))

            #for command in gift_gen_command:
               # updater.dispatcher.add_handler(CommandHandler(command, gerar_gift, run_async=True, pass_update_queue=True, pass_job_queue=True))
            
          #  for command in create_table:
                #updater.dispatcher.add_handler(CommandHandler(command, criar_mix, run_async=True, pass_update_queue=True, pass_job_queue=True))
                
           # for command in menu_pix_command:
                #updater.dispatcher.add_handler(CommandHandler(command, menu_pix, run_async=True, pass_update_queue=True, pass_job_queue=True))

            updater.dispatcher.add_handler(CommandHandler('configuracoes', flags, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('notificaraqui', add_groups, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('chk', chk, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('separador', separador, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('baixarusuarios', baixar_usuarios, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('resaldo', resaldo, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('deletarcartoes', delete_all_cards, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('deletarccs', delete_all_cards, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('backup', download_backup, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('estatisticas', estatisticas, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('relatorio', estatisticas, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('usuario', usuario, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CommandHandler('usuarios', pesquisarusuario, run_async=True, pass_update_queue=True, pass_job_queue=True))


            updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))

            updater.dispatcher.add_handler(CallbackQueryHandler(delete_all_cards, pattern='delete_cards_yes', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(delete_card, pattern='remove_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(ferramentas, pattern='ferramentas', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_mp, pattern='edit_mp', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_mp, pattern='default_mp', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_mp, pattern='delete_mp', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_gn, pattern='edit_gn', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_gn, pattern='default_gn', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_gn, pattern='delete_gn', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_key, pattern='edit_key', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_key, pattern='default_key', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(edit_key, pattern='delete_key', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(menu_pix, pattern='main_pix', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(menu_pix_criados, pattern='menu_pix_criados', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(add_key_pix_start, pattern='key_menu_pix', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(add_gn_pix_start, pattern='gn_menu_pix', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(add_mp_pix_start, pattern='mp_menu_pix', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(add_pix, pattern='menu_pix', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(add_key_pix0, pattern='criar_pix_key', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(recarregar, pattern='r_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(confirmar_compra_mix, pattern='comprarmix_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(comprar_mix, pattern='>', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(add_key_pix0, pattern='criar_pix_key', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(ban, pattern='ban_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(unban, pattern='unban_', run_async=True, pass_update_queue=True, pass_job_queue=True))

            updater.dispatcher.add_handler(CallbackQueryHandler(usuario, pattern='usuario_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(menu, pattern='termos', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(cancelar_compra, pattern='cancelar_compra', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(preco_unitaria, pattern='cancelar_edicao1', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(preco_mix, pattern='cancelar_edicao2', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(unitaria, pattern='unitaria', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(adicionar_saldo, pattern='adicionar_saldo', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(aleatoria, pattern='aleatoria', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(baixar_historico, pattern='baixar_historico', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(encerrar_conta, pattern='encerrar_conta', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(menu, pattern='main', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(historico, pattern='m3', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(informacoes, pattern='m2', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(comprar, pattern='m1', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(mix, pattern='mix', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(afiliados, pattern='afiliados', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(encerrar_conta, pattern='encerrar_conta_sim', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(preco_mix, pattern='editar_mix', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(preco_unitaria, pattern='editar_unitaria', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(editar_precos, pattern='editar_precos', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_mp', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(send, pattern='delete_message', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(add_admin_button, pattern='add_admin_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(remove_admin_button, pattern='rm_admin_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(flags, pattern='flag_', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(search, pattern='search', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(troca, pattern='troca', run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(estatisticas, pattern='stats_', run_async=True, pass_update_queue=True, pass_job_queue=True))


            conv_handler_gn = ConversationHandler(
                entry_points=[CallbackQueryHandler(add_gn_pix, pattern='criar_pix_gn', run_async=True, pass_update_queue=True, pass_job_queue=True)],
                states={
                    STEP1: [MessageHandler(Filters.document & ~Filters.command, add_gn_pix2)],
                    STEP2: [MessageHandler(Filters.text & ~Filters.command, add_gn_pix3)],
                    STEP3: [MessageHandler(Filters.text & ~Filters.command, add_gn_pix4)],
                    STEP4: [MessageHandler(Filters.text & ~Filters.command, add_gn_pix5)]
                },
                fallbacks=[CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_gn', run_async=True, pass_update_queue=True, pass_job_queue=True)],
            )

            conv_handler_mp = ConversationHandler(
                entry_points=[CallbackQueryHandler(add_mp_pix, pattern='criar_pix_mp', run_async=True, pass_update_queue=True, pass_job_queue=True)],
                states={
                    STEP1: [MessageHandler(Filters.text & ~Filters.command, add_mp_pix2)],
                },
                fallbacks=[CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_mp', run_async=True, pass_update_queue=True, pass_job_queue=True)],
            )

            conv_handler_key = ConversationHandler(
                entry_points=[CallbackQueryHandler(add_key_pix1, pattern='pix_cpf', run_async=True, pass_update_queue=True, pass_job_queue=True),
                            CallbackQueryHandler(add_key_pix1, pattern='pix_cnpj', run_async=True, pass_update_queue=True, pass_job_queue=True),
                            CallbackQueryHandler(add_key_pix1, pattern='pix_email', run_async=True, pass_update_queue=True, pass_job_queue=True),
                            CallbackQueryHandler(add_key_pix1, pattern='pix_telefone', run_async=True, pass_update_queue=True, pass_job_queue=True),
                            CallbackQueryHandler(add_key_pix1, pattern='pix_aleatoria', run_async=True, pass_update_queue=True, pass_job_queue=True)],
                states={
                    STEP1: [MessageHandler(Filters.text & ~Filters.command, add_key_pix2)],
                },
                fallbacks=[CallbackQueryHandler(cancel, pattern='cancelar_criacao_pix_key', run_async=True, pass_update_queue=True, pass_job_queue=True)],
            )

            updater.dispatcher.add_handler(conv_handler_gn)
            updater.dispatcher.add_handler(conv_handler_mp)
            updater.dispatcher.add_handler(conv_handler_key)

            send_commands_list = []
            for command in send_command:
                send_commands_list.append('/'+command)

            j = updater.job_queue
            
            try:
                j.run_repeating(payment_checker, interval=120, first=120)
            except: pass
            try:
                j.run_repeating(scheduled_tasks, interval=3600, first=3600)
            except: pass
            try:
                j.run_repeating(backup_task, interval=43200, first=43200)
            except: pass

            def shutdown():
                updater.stop()
                time.sleep(1)
                updater.start_polling(poll_interval=1.0, timeout=30, clean=None, bootstrap_retries=10, read_latency=10.0, allowed_updates=None, drop_pending_updates=True)
            
            def close_bot():
                time.sleep(60)
                while True:
                    if not os.path.isfile('temp/send.txt'):
                        threading.Thread(target=shutdown).start()
                        time.sleep(60)
            
            #j.run_repeating(close_bot, interval=1200, first=1200)

            updater.dispatcher.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), bulk_ccs, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(MessageHandler(Filters.document.mime_type("application/vnd.sqlite3"), upload_backup, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(CallbackQueryHandler(dynamic_buttons, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(MessageHandler(Filters.caption & Filters.photo, send, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(MessageHandler(Filters.caption & Filters.video, send, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(MessageHandler(Filters.caption & Filters.document, send, run_async=True, pass_update_queue=True, pass_job_queue=True))
            updater.dispatcher.add_handler(MessageHandler(Filters.caption & Filters.audio, send, run_async=True, pass_update_queue=True, pass_job_queue=True))

            updater.start_polling(poll_interval=0.5, timeout=100, clean=None, bootstrap_retries=100, read_latency=1.0, allowed_updates=None, drop_pending_updates=True)
            updater.idle()

            break

        except Exception as e:
            logging.exception(e)
            sleep(10)
            continue


