import logging
from aiogram import Bot, Dispatcher, executor, types
import editor
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def on_start(message: types.Message):
    await message.answer("Приветсвую! Я бот для создания демотиваторов, отправь мне картинку и добавь подпись чтобы начать. Также можно использовать команду /dem [подпись]. Бот работает в чатах.")


@dp.message_handler(commands=['dem', 'demotivate', "дем", "демотиватор"])
async def demotivator_command(message: types.Message):
    if not message.photo == []:
        id_file = await bot.get_file(message.photo[-1].file_id)
        dowloaded_file_photo = await bot.download_file(id_file.file_path)
        photo_text = message.get_args()
        if photo_text is None or photo_text == "":
            photo_text = "чечня на связи"
    else:
        if message.reply_to_message:
            if not message.reply_to_message.photo == []:
                id_file = await bot.get_file(message.reply_to_message.photo[-1].file_id)
                dowloaded_file_photo = await bot.download_file(id_file.file_path)
                photo_text = message.get_args()
                if photo_text is None or photo_text == "":
                    photo_text = "чечня на связи"
            else:
                return
        else:
            return
    img_byte = editor.add_text(dowloaded_file_photo, photo_text)
    img_byte.seek(0)

    await bot.send_photo(message.chat.id, img_byte)


@dp.message_handler(content_types=['photo', 'text'])
async def demotivator(message: types.Message):
    if message.caption:
        if message.caption.split()[0] in ['/dem', '/demotivate', "/дем", "/демотиватор"]:
            id_file = await bot.get_file(message.photo[-1].file_id)
            dowloaded_file_photo = await bot.download_file(id_file.file_path)
            photo_text = message.caption.split()
            photo_text.pop(0)
            if not photo_text:
                photo_text = "чечня на связи"
            else:
                photo_text = " ".join(photo_text)
        else:
            if not message.photo == []:
                id_file = await bot.get_file(message.photo[-1].file_id)
                dowloaded_file_photo = await bot.download_file(id_file.file_path)
                photo_text = message.caption
                if photo_text is None:
                    photo_text = "чечня на связи"
            else:
                return
    else:
        if not message.chat.type == "private":
            return
        if not message.photo:
            if message.reply_to_message:
                if not message.reply_to_message.photo == []:
                    id_file = await bot.get_file(message.reply_to_message.photo[-1].file_id)
                    dowloaded_file_photo = await bot.download_file(id_file.file_path)
                    photo_text = message.text
                    if photo_text is None:
                        return
                else:
                    return
            else:
                return
        else:
            id_file = await bot.get_file(message.photo[-1].file_id)
            dowloaded_file_photo = await bot.download_file(id_file.file_path)
            photo_text = "чечня на связи"
            
    img_byte = editor.add_text(dowloaded_file_photo, photo_text)
    img_byte.seek(0)

    await bot.send_photo(message.chat.id, img_byte)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
