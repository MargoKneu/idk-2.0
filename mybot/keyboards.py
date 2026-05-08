from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram import emoji

btn_info = KeyboardButton(f"{emoji.INFORMATION} info")
btn_time = KeyboardButton(f"{emoji.VIDEO_GAME} time")
btn_game = KeyboardButton(f"{emoji.VIDEO_GAME} game")

kb_main = ReplyKeyboardMarkup(
keyboard=[
    [btn_info, btn_time, btn_game]
],
resize_keyboard=True)

btn_rps = KeyboardButton(f"{emoji.INFORMATION} rock paper scissors")
btn_quest = KeyboardButton(f"{emoji.PERSON} quest")
btn_back = btn_profile = KeyboardButton(f"{emoji.VIDEO_GAME} back")

kb_game = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rps],
        [btn_quest, btn_back]

    ],
    resize_keyboard=True)
btn_rock = KeyboardButton(f"{emoji.ROCK} rock")
btn_paper = KeyboardButton(f"{emoji.NOTEBOOK} paper")
btn_scissors = KeyboardButton(f"{emoji.SCISSORS} scissors")

kb_rps = ReplyKeyboardMarkup(
keyboard = [
    [btn_rock, btn_paper, btn_scissors],
    [btn_back]

],
resize_keyboard = True)

inline_kb_start_quest = InlineKeyboardMarkup([
        [InlineKeyboardButton("do the quest",callback_data="start_quest")]
    ])

inline_kb_choice = InlineKeyboardMarkup([
    [InlineKeyboardButton("left door", callback_data="left_door")],
    [InlineKeyboardButton("center door", callback_data="center_door")],
    [InlineKeyboardButton("right door", callback_data="right_door")]
])

inline_kb_left_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("take the sword", callback_data="sword")],
    [InlineKeyboardButton("try escape", callback_data="escape")]
])

inline_kb_center_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("accept your fate", callback_data="fate")],
    [InlineKeyboardButton("scream", callback_data="scream")]
])

inline_kb_right_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("take the mask", callback_data="mask")],
    [InlineKeyboardButton("cover your nose", callback_data="nose")]
])
