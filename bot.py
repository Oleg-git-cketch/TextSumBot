import telebot
import database as db
import TextSum as ts

bot = telebot.TeleBot('7952352811:AAEqgtz9v94gFEWoFnLHiTEZYGI2Q7AJylQ')


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    if db.check_count(user_id):
        bot.send_message(user_id, 'Напишите текст, и я создам краткое резюме!')
        bot.register_next_step_handler(message, summarize_text)
    else:
        db.register(user_id)
        bot.send_message(user_id, 'Напишите текст, и я создам краткое резюме!')
        bot.register_next_step_handler(message, summarize_text)


def summarize_text(message):
    user_id = message.from_user.id
    user_text = message.text

    if db.check_count(user_id) <= 5:
        try:
            summarized_text = ts.sumextract(user_text, n=3)

            bot.send_message(user_id, f"Краткое содержание:\n{summarized_text}")

            db.add_count(user_id)
            bot.register_next_step_handler(message, summarize_text)
        except Exception as e:
            bot.send_message(user_id, f"Произошла ошибка: {e}. Попробуйте снова.")
            bot.register_next_step_handler(message, summarize_text)
    else:
        bot.send_message(user_id, 'Похоже, что вы истратили все токены.\n'
                                  'Оплатите подписку или дождитесь следующего месяца.')


bot.polling(non_stop=True)
