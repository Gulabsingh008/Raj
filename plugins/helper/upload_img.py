import requests
import os, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 
from info import 

@Client.on_message(
    filters.command('imgbb')
    & (
        filters.private |
        filters.group
    )
)
async def imgbb_upload(_, msg: Message):
    if tg.FSUB:
        client = _
        message = msg
        is_participant = await get_fsub(client, message)
        if not is_participant:
            return
    replied = msg.reply_to_message
    if not replied:
        await msg.reply_text("𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙰 𝙿𝙷𝙾𝚃𝙾 𝙾𝚁 𝚅𝙸𝙳𝙴𝙾 𝚄𝙽𝙳𝙴𝚁 𝟻𝙼𝙱.")
        return
    
    if not (replied.photo or replied.video or replied.animation):
        await msg.reply_text("Please reply to a photo, video, or GIF.")
        return

    text = await msg.reply_text("<code>Downloading to My Server ...</code>", disable_web_page_preview=True)
    
    # Download the media
    media = await msg.reply_to_message.download()

    await text.edit_text("<code>Downloading Completed. Now I am Uploading to imgbb ...</code>", disable_web_page_preview=True)

    # Uploading to imgbb
    try:
        with open(media, 'rb') as file:
            response = requests.post(
                f"https://api.imgbb.com/1/upload?key={tg.IMGBB_API_KEY}",
                files={"image": file}
            )
            response_data = response.json()
            
            if response_data['success']:
                image_url = response_data['data']['url']
            else:
                raise Exception(response_data['error']['message'])
    except Exception as error:
        print(error)
        await text.edit_text(f"Error: {error}", disable_web_page_preview=True)
        return
    
    # Clean up the downloaded file
    try:
        os.remove(media)
    except Exception as error:
        print(error)

    await text.edit_text(
        text=f"<b>Link:</b>\n\n<code>{image_url}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="Open Link", url=image_url),
                InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={image_url}")
            ],
            [
                InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]
        ])
    )



def upload_image_requests(image_path):
    upload_url = "https://envs.sh"

    try:
        with open(image_path, 'rb') as file:
            files = {'file': file} 
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                return response.text.strip() 
            else:
                raise Exception(f"Upload failed with status code {response.status_code}")

    except Exception as e:
        print(f"Error during upload: {e}")
        return None


@Client.on_message(
    filters.command('upload')
    & (
        filters.private |
        filters.group
    )
)
async def upload_cmd(_, msg: Message):
    if tg.FSUB:
        client = _
        message = msg
        is_participant = await get_fsub(client, message)
        if not is_participant:
            return
    replied = msg.reply_to_message
    if not replied:
        await msg.reply_text("Reply to a photo or video under 5 MB.")
        return

    if replied.media and hasattr(replied, 'file_size'):
        if replied.file_size > 5242880:
            await msg.reply_text("File size is greater than 5 MB.")
            return

    ds_path = await replied.download()

    uploading_message = await msg.reply_text("<code>Uploading...</code>")

    try:
        ds_url = upload_image_requests(ds_path)
        if not ds_url:
            raise Exception("Failed to upload file.")
    except Exception as error:
        await uploading_message.edit_text(f"Upload failed: {error}")
        return

    try:
        os.remove(ds_path)
    except Exception as error:
        print(f"Error removing file: {error}")

    await uploading_message.edit_text(
        text=f"<b>Link :-</b>\n\n<code>{ds_url}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="Open Link", url=ds_url),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={ds_url}")
        ], [
            InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
        ]])
    )

@Client.on_callback_query()
async def callback(client: Client, query: CallbackQuery): 
    if query.data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
