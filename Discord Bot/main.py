import discord
import ffmpeg
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
from datetime import datetime
import asyncio
import json
import os
from google.cloud import storage

intents = discord.Intents.all()
intents.members = True  # Enable the privileged `Members` intent.

bot = commands.Bot(command_prefix='!', intents=intents)

remaining_time=0

# set project name
os.environ["GCLOUD_PROJECT"] = "speedy-rhino-136121"

# set the path to the JSON file
file_path = r"remaining_time.json"

# set the name of the bucket to upload to
bucket_name = "dc-bot-bucket"

# create a storage client
storage_client = storage.Client()

# get a reference to the bucket
bucket = storage_client.bucket(bucket_name)

def create_json(file_path):
    blob = bucket.blob(file_path)
    blob.upload_from_filename(file_path)

@bot.event
async def on_ready():
    print('Papiez bedzie tanczyc')
    play_audio.start()


set_hour=21
set_minute=37

@tasks.loop(seconds=1) # Run once a day
async def play_audio():
    now = datetime.now()
    if now.hour == set_hour and now.minute == set_minute:
        channel = bot.get_channel(629259985771298838) # Replace with your channel ID
        voice = await channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('papiez-inba-refren.mp3'))
        voice.play(source)
        await bot.get_channel(629259985771298836).send("PROSZĘ PAŃSTWA PAN PAWEŁ BĘDZIE TAŃCZYŁ")
        while voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()
    else:
        remaining_time = datetime(now.year, now.month, now.day, set_hour, set_minute).replace(microsecond=0) - now.replace(microsecond=0)
        if remaining_time.seconds > 3600:
            t=3600
        else:
            t=1
        print(f"Time till inba: {remaining_time}")
        # data = {"remaining_time": remaining_time}
        # json_string = json.dumps(data, indent=4, sort_keys=True, default=str)
        # with open("remaining_time.json", "w") as outfile:
        #     outfile.write(json_string)
        # create_json(file_path)
        await asyncio.sleep(t)

@bot.command()
async def start(ctx):
    play_audio.start()
    await ctx.send('Niech inba ciagle trwa')

@bot.command()
async def stop(ctx):
    play_audio.cancel()
    await ctx.send('Papiez juz nie tanczy..')

bot.run("MTEwMDg4NjkyNTAzMzg4NTg4OA.G5s2uB.R0LaUYbbpLeeZEY0oIehkvLwnO_ZfO5OnFje-4")

