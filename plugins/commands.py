import os, requests
import logging
import random
import asyncio
import string
import pytz
from datetime import timedelta
from datetime import datetime as dt
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, get_bad_files, unpack_new_file_id
from database.users_chats_db import db
from info import UPI_PAY_LOGS, ADMINS, THREE_VERIFY_GAP, LOG_CHANNEL, USERNAME, VERIFY_IMG, IS_VERIFY, FILE_CAPTION, AUTH_CHANNEL, SHORTENER_WEBSITE, SHORTENER_API, SHORTENER_WEBSITE2, SHORTENER_API2, LOG_API_CHANNEL, TWO_VERIFY_GAP, QR_CODE, DELETE_TIME
from utils import get_settings,get_seconds, save_group_settings, is_req_subscribed, get_size, get_shortlink, is_check_admin, get_status, temp, get_readable_time
import re
import base64
from info import *
import traceback
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("fsub"))
async def force_subscribe(client, message):
    m = await message.reply_text("Wait im checking...")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("This command is only for groups!")
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("Only group admins can use this command!")
    try: 
        toFsub = message.command[1]
    except IndexError:
        return await m.edit("Usage: /fsub CHAT_ID")
    if not toFsub.startswith("-100"):
        toFsub = '-100'+toFsub
    if not toFsub[1:].isdigit() or len(toFsub) != 14:
        return await m.edit("CHAT_ID isn't valid!")
    toFsub = int(toFsub)
    if toFsub == message.chat.id:
        return await m.edit("It seems like you're attempting to enable force subscription for this chat ID. Please use a different chat ID !")
    if not await is_check_admin(client, toFsub, client.me.id):
        return await m.edit("I need to be an admin in the given chat to perform this action!\nMake me admin in your Target chat and try again.")
    try:
        await db.setFsub(grpID=message.chat.id, fsubID=toFsub)
        return await m.edit(f"Successfully added force subscribe to {toFsub} in {message.chat.title}")
    except Exception as e:
        logger.exception(e)
        return await m.edit(f"Something went wrong ! Try again later or report in Support Group @bisal_files_talk")

@Client.on_message(filters.command("del_fsub"))
async def del_force_subscribe(client, message):
    m = await message.reply_text("Wait im checking...")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("This command is only for groups!")
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("Only group admins can use this command!")
    ifDeleted =await db.delFsub(message.chat.id)
    if ifDeleted:
        return await m.edit(f"Successfully removed force subscribe for - {message.chat.title}\nTo add again use <code>/fsub YOUR_FSUB_CHAT_ID</code>")
    else:
        return await m.edit(f"Force subscribe not found in {message.chat.title}")

@Client.on_message(filters.command("show_fsub"))
async def show_fsub(client, message):
    m = await message.reply_text("Wait im checking...")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("This command is only for groups!")
    # check if commad is given by admin or not
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("Only group admins can use this command!")
    fsub = await db.getFsub(message.chat.id)
    if fsub:
        #now gen a invite link
        invite_link = await client.export_chat_invite_link(fsub)
        await m.edit(f"Force subscribe is set to {fsub}\n<a href={invite_link}>Channel Link Link</a>" ,disable_web_page_preview=True)
    else:
        await m.edit(f"Force subscribe is not set in {message.chat.title}")
        

@Client.on_message(filters.command("bought") & filters.private)
async def bought(client, message):
    msg = await message.reply('Wait im checking...')
    replyed = message.reply_to_message
    if not replyed:
        await msg.edit("<b>Please reply with the screenshot of your payment for the premium purchase to proceed.\n\nFor example, first upload your screenshot, then reply to it using the '/bought' command</b>")
    if replyed and replyed.photo:
        await client.send_photo(
            photo=replyed.photo.file_id,
            chat_id=UPI_PAY_LOGS,
            caption=f'<b>User - {message.from_user.mention}\nUser id - <code>{message.from_user.id}</code>\nusername - <code>{message.from_user.username}</code>\nUser Name - <code>{message.from_user.first_name}</code></b>',
            reply_markup=InlineKeyboardMarkup(
                [
                    
                    [
                        InlineKeyboardButton(
                            "Close", callback_data="close_data"
                        )
                    ]
                    
                ]
            )
        )
        await msg.edit_text('<b>Your screenshot has been sent to Admins</b>')

@Client.on_message(filters.command("premium") & filters.user(ADMINS))
async def add_premium(client, message):
    try:
        _, user_id, time, *custom_message = message.text.split(" ", 3)
        custom_message = "**Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴘᴜʀᴄʜᴀsɪɴɢ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ᴘᴀᴄᴋᴀɢᴇ. Nᴏᴡ, ʟᴇᴠᴇʀᴀɢᴇ ɪᴛs ғᴜʟʟ ᴘᴏᴛᴇɴᴛɪᴀʟ**" if not custom_message else " ".join(custom_message)
        time_zone = dt.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y : %I:%M:%S %p")
        user = await client.get_users(user_id)
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = dt.now() + timedelta(seconds=seconds)
            user_data = {"id": user.id, "expiry_time": expiry_time}
            await db.update_user(user_data)
            data = await db.get_user(user.id)
            expiry = data.get("expiry_time")
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  :  %I:%M:%S %p")
            await message.reply_text(f"<b><u>Premium Access Added To The User</u>\n\n👤 User: {user.mention}\n\n🪪 User id: <code>{user_id}</code>\n\n⏰ Premium Access: {time}\n\n🎩 Joining : {current_time}\n\n⌛️ Expiry: {expiry_str_in_ist}.\n\n<code>{custom_message}</code></b>", disable_web_page_preview=True)
            await client.send_message(chat_id=user_id, text=f"<b>ʜɪɪ {user.mention},\n\n<u>ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ</u> 😀\n\nᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss - {time}\n\n⏰ ᴊᴏɪɴɪɴɢ - {current_time}\n\n⌛️ ᴇxᴘɪʀᴇ ɪɴ - {expiry_str_in_ist}\n\n<code>{custom_message}</code></b>", disable_web_page_preview=True)
            await client.send_message(LOG_CHANNEL, text=f"#Added_Premium\n\n👤 User - {user.mention}\n\n🪪 User Id - <code>{user_id}</code>\n\n⏰ Premium Access - {time}\n\n🎩 Joining - {current_time}\n\n⌛️ Expiry - {expiry_str_in_ist}\n\n<code>{custom_message}</code>", disable_web_page_preview=True)
        else:
            await message.reply_text("<b>⚠️ Invalid Format, Use This Format - <code>/add_premium 1030335104 1day</code>\n\n<u>Time Format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code>\n\nChange As Your Wish Like 2, 3, 4, 5 etc....</b>")
    except ValueError:
        await message.reply_text("<b>⚠️ Invalid Format, Use This Format - <code>/add_premium 1030335104 1day</code>\n\n<u>Time Format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code>\n\nChange As Your Wish Like 2, 3, 4, 5 etc....</b>")
    except Exception as e:
        traceback.print_exc()
        await message.reply_text(f"error - {e}")

@Client.on_message(filters.command("m_grp") & filters.user(ADMINS))
async def m_grp(client, message):
    msg = await message.reply("wait i'm checking..")
    try:
        link =  message.command[1]
        await msg.edit('checking ypur link..')
        url_pattern = r'^https?://(?:www\.)?\S+$'
        if re.match(url_pattern, link):
            await msg.edit('hmm..link is valid..😚')
            await db.get_set_mgrp(link)
            await msg.edit('link is saved in my db..😚')
            await asyncio.sleep(5)
            await msg.delete()
            await message.delete()
    except IndexError:
        await msg.edit('Send me your grp link with the command')
        await msg.delete()
        await message.delete()
        
@Client.on_message(filters.command("start") & filters.incoming)
async def start(client:Client, message): 
    m = message
    user_id = m.from_user.id
    if len(m.command) == 2 and m.command[1].startswith('notcopy'):
        _, userid, verify_id, file_id = m.command[1].split("_", 3)
        user_id = int(userid)
        grp_id = temp.CHAT.get(user_id, 0)
        settings = await get_settings(grp_id)         
        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("<b>ʟɪɴᴋ ᴇxᴘɪʀᴇᴅ ᴛʀʏ ᴀɢᴀɪɴ...</b>")
            return  
        ist_timezone = pytz.timezone('Asia/Kolkata')
        if await db.user_verified(user_id):
            key = "third_time_verified"
        else:
            key = "second_time_verified" if await db.is_user_verified(user_id) else "last_verified"
        current_time = dt.now(tz=ist_timezone)
        result = await db.update_notcopy_user(user_id, {key:current_time})
        await db.update_verify_id_info(user_id, verify_id, {"verified":True})
        if key == "third_time_verified": 
            num = 3 
        else: 
            num =  2 if key == "second_time_verified" else 1 
        if key == "third_time_verified": 
            msg = script.THIRDT_VERIFY_COMPLETE_TEXT
        else:
            msg = script.SECOND_VERIFY_COMPLETE_TEXT if key == "second_time_verified" else script.VERIFY_COMPLETE_TEXT
        await client.send_message(settings['log'], script.VERIFIED_LOG_TEXT.format(m.from_user.mention, user_id, dt.now(pytz.timezone('Asia/Kolkata')).strftime('%d %B %Y'), num))
        btn = [[
            InlineKeyboardButton("‼️ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ꜰɪʟᴇ ‼️", url=f"https://telegram.me/{temp.U_NAME}?start=file_{grp_id}_{file_id}"),
        ]]
        reply_markup=InlineKeyboardMarkup(btn)
        await m.reply_photo(
            photo=(VERIFY_IMG),
            caption=msg.format(message.from_user.mention, get_readable_time(TWO_VERIFY_GAP)),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return 
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        status = get_status()
        aks=await message.reply_text(f"<b>🔥 ʏᴇs {status},\nʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ??</b>")
        await asyncio.sleep(600)
        await aks.delete()
        await m.delete()
        if (str(message.chat.id)).startswith("-100") and not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            group_link = await message.chat.export_invite_link()
            user = message.from_user.mention if message.from_user else "Dear" 
            await client.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(temp.B_LINK, message.chat.title, message.chat.id, message.chat.username, group_link, total, user))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.NEW_USER_TXT.format(temp.B_LINK, message.from_user.id, message.from_user.mention))
        try: 
            refData = message.command[1]
            if refData and refData.split("-", 1)[0] == "SbBotz":
                Fullref = refData.split("-", 1)
                refUserId = int(Fullref[1])
                await db.update_point(refUserId)
                newPoint = await db.get_point(refUserId)
                if AUTH_CHANNEL and await is_req_subscribed(client, message):
                        buttons = [[
                            InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
                            ],[
                            InlineKeyboardButton('⚙ ꜰᴇᴀᴛᴜʀᴇs', callback_data='features'),
                            InlineKeyboardButton('ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ 🎉', callback_data='premium'),
                            ],
                            [
                            InlineKeyboardButton('• ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ғʀᴇᴇ •', callback_data=f'free_premium#{message.from_user.id}')
                            ],
                            [
                            InlineKeyboardButton('• ʏᴏᴜʀ ᴘᴏɪɴᴛs •', callback_data=f'point#{message.from_user.id}'),
                            InlineKeyboardButton('• ᴀʙᴏᴜᴛ •', callback_data='about')
                            ],
                            [
                            InlineKeyboardButton('💸 ᴇᴀʀɴ ᴍᴏɴᴇʏ ᴡɪᴛʜ ʙᴏᴛ 💸', callback_data='earn')
                            ]]
                        reply_markup = InlineKeyboardMarkup(buttons)
                        await message.reply_photo(photo=START_IMG, caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
                            reply_markup=reply_markup,
                            parse_mode=enums.ParseMode.HTML)
                try: 
                    if newPoint == 0:
                        await client.send_message(refUserId , script.REF_PREMEUM.format(message.from_user.mention() , PREMIUM_POINT))
                    else: 
                        await client.send_message(refUserId , script.REF_START.format(message.from_user.mention() , newPoint))
                except : pass
        except Exception as e:
            traceback.print_exc()
            pass
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
        ],[
            InlineKeyboardButton('⚙ ꜰᴇᴀᴛᴜʀᴇs', callback_data='features'),
            InlineKeyboardButton('ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ 🎉', callback_data='premium'),
        ],
        [
            InlineKeyboardButton('• ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ғʀᴇᴇ •', callback_data=f'free_premium#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('• ʏᴏᴜʀ ᴘᴏɪɴᴛs •', callback_data=f'point#{message.from_user.id}'),
            InlineKeyboardButton('• ᴀʙᴏᴜᴛ •', callback_data='about')
        ],
        [
            InlineKeyboardButton('💸 ᴇᴀʀɴ ᴍᴏɴᴇʏ ᴡɪᴛʜ ʙᴏᴛ 💸', callback_data='earn')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(photo=START_IMG, caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if AUTH_CHANNEL and not await is_req_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL), creates_join_request=True)
        except ChatAdminRequired:
            logger.error("Make Sure Bot Is Admin In Forcesub Channel")
            return
        btn = [[
            InlineKeyboardButton("🎗️ ᴊᴏɪɴ ɴᴏᴡ 🎗️", url=invite_link.invite_link)
        ]]

        if message.command[1] != "subscribe":
            try:
                kk, grp_id, file_id = message.command[1].split('_', 2)
                pre = 'checksubp' if kk == 'filep' else 'checksub'
                btn.append(
                    [InlineKeyboardButton("♻️ ᴛʀʏ ᴀɢᴀɪɴ ♻️", callback_data=f"checksub#{file_id}")]
                )
            except (IndexError, ValueError):
                btn.append(
                    [InlineKeyboardButton("♻️ ᴛʀʏ ᴀɢᴀɪɴ ♻️", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")]
                )
        await client.send_message(
            chat_id=message.from_user.id,
            text="🙁 ғɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴍᴏᴠɪᴇ, ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ɢᴇᴛ ɪᴛ.\n\nᴄʟɪᴄᴋ ᴊᴏɪɴ ɴᴏᴡ ʙᴜᴛᴛᴏɴ 👇",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.HTML
        )
        return

    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
        ],[
            InlineKeyboardButton('⚙ ꜰᴇᴀᴛᴜʀᴇs', callback_data='features'),
            InlineKeyboardButton('ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ 🎉', callback_data='premium'),
        ],
        [
            InlineKeyboardButton('• ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ғʀᴇᴇ •', callback_data=f'free_premium#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('• ʏᴏᴜʀ ᴘᴏɪɴᴛs •', callback_data=f'point#{message.from_user.id}'),
            InlineKeyboardButton('• ᴀʙᴏᴜᴛ •', callback_data='about')
        ],
        [
            InlineKeyboardButton('💸 ᴇᴀʀɴ ᴍᴏɴᴇʏ ᴡɪᴛʜ ʙᴏᴛ 💸', callback_data='earn')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply_photo(photo=START_IMG, caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    data = message.command[1]
    try:
        pre, grp_id, file_id = data.split('_', 2)
    except:
        pre, grp_id, file_id = "", 0, data
             
    user_id = m.from_user.id
    if not await db.has_premium_access(user_id):
        grp_id = int(grp_id)
        user_verified = await db.is_user_verified(user_id)
        settings = await get_settings(grp_id)
        is_second_shortener = await db.use_second_shortener(user_id, settings.get('verify_time', TWO_VERIFY_GAP)) 
        is_third_shortener = await db.use_third_shortener(user_id, settings.get('third_verify_time', THREE_VERIFY_GAP))
        if settings.get("is_verify", IS_VERIFY) and not user_verified or is_second_shortener or is_third_shortener:
            verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            await db.create_verify_id(user_id, verify_id)
            temp.CHAT[user_id] = grp_id
            verify = await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=notcopy_{user_id}_{verify_id}_{file_id}", grp_id, is_second_shortener, is_third_shortener)
            buttons = [[
                InlineKeyboardButton(text="♻️ ᴠᴇʀɪғʏ ♻️", url=verify)
            ],[
                InlineKeyboardButton(text="⁉️ ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ ❓", url=settings['tutorial']),
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            if await db.user_verified(user_id): 
                msg = script.THIRDT_VERIFICATION_TEXT
            else:            
                msg = script.SECOND_VERIFICATION_TEXT if is_second_shortener else script.VERIFICATION_TEXT
            d = await m.reply_text(
                text=msg.format(message.from_user.mention, get_status()),
                protect_content = False,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(300) 
            await d.delete()
            await m.delete()
            return
            
    if data and data.startswith("allfiles"):
        _, key = data.split("_", 1)
        files = temp.FILES_ID.get(key)
        if not files:
            await message.reply_text("<b>⚠️ ᴀʟʟ ꜰɪʟᴇs ɴᴏᴛ ꜰᴏᴜɴᴅ ⚠️</b>")
            return
        for file in files:
            user_id= message.from_user.id 
            grp_id = tem
