import os
from telegraph import upload_file
import pyrogram
from pyrogram import filters, Client
from sample_config import Config
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, InlineQuery)

Tgraph = Client(
   "Telegra.ph Uploader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

@Tgraph.on_message(filters.photo)
async def uploadphoto(client, message):
  msg = await message.reply_text("`Téléchargement....`")
  userid = str(message.chat.id)
  img_path = (f"./DOWNLOADS/{userid}.jpg")
  img_path = await client.download_media(message=message, file_name=img_path)
  await msg.edit_text("`Téléversement.....`")
  try:
    tlink = upload_file(img_path)
  except:
    await msg.edit_text("`Une erreur est survenue`") 
  else:
    await msg.edit_text(f"https://telegra.ph{tlink[0]}")     
    os.remove(img_path) 

@Tgraph.on_message(filters.animation)
async def uploadgif(client, message):
  if(message.animation.file_size < 5242880):
    msg = await message.reply_text("`Téléchargement......`")
    userid = str(message.chat.id)
    gif_path = (f"./DOWNLOADS/{userid}.mp4")
    gif_path = await client.download_media(message=message, file_name=gif_path)
    await msg.edit_text("`Téléversement.....`")
    try:
      tlink = upload_file(gif_path)
      await msg.edit_text(f"https://telegra.ph{tlink[0]}")   
      os.remove(gif_path)   
    except:
      await msg.edit_text("Une erreur est survenue...") 
  else:
    await message.reply_text("La taille devrait etre inférieur à 5Mo")

@Tgraph.on_message(filters.video)
async def uploadvid(client, message):
  if(message.video.file_size < 5242880):
    msg = await message.reply_text("`Téléchargement`")
    userid = str(message.chat.id)
    vid_path = (f"./DOWNLOADS/{userid}.mp4")
    vid_path = await client.download_media(message=message, file_name=vid_path)
    await msg.edit_text("`Téléversement.....`")
    try:
      tlink = upload_file(vid_path)
      await msg.edit_text(f"https://telegra.ph{tlink[0]}")     
      os.remove(vid_path)   
    except:
      await msg.edit_text("Une erreur est survenue...") 
  else:
    await message.reply_text("La taille devrait etre inférieur à 5Mo")

@Tgraph.on_message(filters.command(["start"]))
async def home(client, message):
  buttons = [[
        InlineKeyboardButton('⁉ Aide', callback_data='help'),
        InlineKeyboardButton('🗑 Fermer', callback_data='close')
    ],
    [
        InlineKeyboardButton('👨‍💻 Développeur', url='http://telegram.me/A_liou'),
        InlineKeyboardButton('📦 Code source', url='https://github.com/codingtuto/Telegraph-Uploader/')
    ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await Tgraph.send_message(
        chat_id=message.chat.id,
        text="""<b>Bonjour,

Je peut uploader vos photos,vidéos et gifs pour les stocker sur le serveur public de Telegram(Telegraph).

Il vous suffit de m'envoyer une photo, une vidéo ou un gif à télécharger sur Telegra.ph.</b>""",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=message.message_id
    )

@Tgraph.on_message(filters.command(["help"]))
async def help(client, message):
  buttons = [[
        InlineKeyboardButton('🔥 Acceuil', callback_data='home'),
        InlineKeyboardButton('🗑 Fermer', callback_data='close')
    ],
    [
        InlineKeyboardButton('👨‍💻 Développeur', url='http://telegram.me/A_liou')
    ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await Tgraph.send_message(
        chat_id=message.chat.id,
        text="""Il n'y a rien de plus à savoir,

Envoyez-moi simplement une vidéo/gif/photo jusqu'à 5 Mo.

Je les téléchargerai sur Telegra.ph et vous donnerai le lien direct.""",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=message.message_id
    )                           
@Tgraph.on_callback_query()
async def button(Tgraph, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(Tgraph, update.message)
      elif "close" in cb_data:
        await update.message.delete() 
      elif "home" in cb_data:
        await update.message.delete()
        await home(Tgraph, update.message)

Tgraph.run()
