import random
import json
from pyrogram import Client, filters
import datetime
import config
import keyboards
import base64
from FushionBrain_AI import generate
bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my first bot"
)

def button_filter(button):
   async def func(_, __, msg):
       return msg.text == button.text
   return filters.create(func, "ButtonFilter", button=button)

@bot.on_message(filters.command("start"))
async def echo(bot, message):
    await bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEOFBln1FFzgOQ3LJagfEhCyowGzJOb3AACTAADXQWCFl6FmZFTQvEFNgQ",    reply_markup=keyboards.kb_main)
    with open("user.json", "r") as file:
        user = json.load(file)
        if str(message.from_user.id) not in user.keys():
            user[message.from_user.id] = 100
            with open("user.json", "w") as file:
                json.dump(user,file)

@bot.on_message(filters.command("image"))
async def image(bot, message):
    if len(message.text.split()) > 1:
        query = message.text.replace("/image ", "")
        await message.reply_text(f"generating image for answer '{query}', wait a minute...")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            with open(f"images/image.jpg", "wb") as file:
                file.write(image_data)
                await bot.send_photo(message.caht.id, f"images/image.jpg", reply_to_message_id=message.id)
        else:
            await message.reply_text("error 404", reply_to_message_id=message.id)
    else:
        await message.reply_text("say the answer")


@bot.on_message(filters.command("time")|button_filter(keyboards.btn_time))
async def echo(bot, message):
    date_time = datetime.datetime.now()
    await message.reply(date_time.time())

@bot.on_message(filters.command("info") | button_filter(keyboards.btn_info))
async def echo(bot, message):
    await message.reply("The command is /start = sticker")


@bot.on_message(filters.command("games") | button_filter(keyboards.btn_game))
async def game(bot, message):
    await message.reply("select game", reply_markup=keyboards.kb_game)

@bot.on_message(filters.command("back") | button_filter(keyboards.btn_back))
async def back(bot, message):
    await message.reply("back to the home", reply_markup=keyboards.kb_main)

@bot.on_message(filters.command("game") | button_filter(keyboards.btn_rps))
async def game(bot, message):
    with open("user.json", "r") as file:
        users = json.load(file)
    if users[str(message.from_user.id)] >= 10:
        await message.reply("your turn", reply_markup=keyboards.kb_rps)
    else:
         await message.reply(f"you dont have enough green paper.you have {users[str](message.from_user.id)})you most have 10 green paper")

@bot.on_message(button_filter(keyboards.btn_rock) |
                button_filter(keyboards.btn_paper) |
                button_filter(keyboards.btn_scissors) )

async def choice_rps(bot, message):
    with open("user.json", "r") as file:
        users = json.load(file)

    rock = keyboards.btn_rock.text
    paper = keyboards.btn_paper.text
    scissors = keyboards.btn_scissors.text
    user = message.text
    pc = random.choice([rock, paper, scissors])

    if user == pc:
        await message.reply("tie")
    elif (user == rock and pc == scissors) or (user == paper and pc == rock) or (user == scissors and pc == paper):
        await message.reply(f" you win. bot choice {pc}", reply_markup=keyboards.kb_game)
        users[str(message.from_user.id)] +=10
    else:
        await message.reply(f"you lose. bot choice {pc}", reply_markup=keyboards.kb_game)
        users[str(message.from_user.id)] -= 10

    with open("user.json", "w") as file:
        json.dump(users, file)

@bot.on_message(filters.command("quest") | button_filter(keyboards.btn_quest))
async def quest(bot, message):
    await message.reply_text("do you want adventures of add? is a joke :) sorry",
    reply_markup=keyboards.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(bot, query):

    if query.data == "start_quest":
        await bot.answer_callback_query(query.id, text="welcome to the quest.you liked the quest", show_alert=True)
        await query.message.reply_text("you enter in the house and you have 3 doors: left door, center door and right door. in which door do you enter?", reply_markup=keyboards.inline_kb_choice)
    elif query.data == "left_door":
        await query.message.reply_text("you enter in the left door, you find zombie and one diamond sword.what would you do?", reply_markup=keyboards.inline_kb_left_door)
    elif query.data == "sword":
        await bot.answer_callback_query(query.id, text="you take the sword and kill the zombie. you win", show_alert=True)
    elif query.data == "escape":
        await bot.answer_callback_query(query.id, text="you try to escape but zombie cath you. you lose", show_alert=True)
    elif query.data == "center_door":
        await query.message.reply_text("you enter in a white room, the door closes behind you.What would you do?", reply_markup=keyboards.inline_kb_center_door)
    elif query.data == "fate":
        await bot.answer_callback_query(query.id, text="you stake here for ever", show_alert=True)
    elif query.data == "scream":
        await bot.answer_callback_query(query.id, text="nothing happened,you stake here for ever", show_alert=True)
    elif query.data == "right_door":
        await query.message.reply_text("you enter in a right door, the gas starts to come out of the house.What would you do?", reply_markup=keyboards.inline_kb_right_door)
    elif query.data == "mask":
        await bot.answer_callback_query(query.id, text="you escape from the house.  you win", show_alert=True)
    elif query.data == "nose":
        await bot.answer_callback_query(query.id, text="why do you did this. you lose", show_alert=True)
    await query.message.delete()

bot.run()