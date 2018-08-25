import discord
from discord.ext import commands
import asyncio
import os
from MUBDatabase import MUBDatabase
import time
import random

TOKEN = os.environ.get('TOKEN')
DATABASE_URL = os.environ['DATABASE_URL']
mub_db = MUBDatabase(DATABASE_URL)

client = commands.Bot(command_prefix="MUB ", case_insensitive=True)

test = mub_db.get_test()


tasks_created = False
count = 0
start_time = time.time()
id_int = 1


def add_test(test_id: int, name: str):
    mub_db.add_test(test_id, name)


def remove_test(test_id: int):
    mub_db.remove_test(test_id)


def update_test(test_id: int, name: str):
    mub_db.update_test(test_id, name)


def print_status():
    print("---- Status ------")
    print("Is closed: " + str(client.is_closed()))
    print("Is ready: " + str(client.is_ready()))
    print("Websocket: " + str(client.ws))
    print("Per server: ")
    for g in client.guilds:
        print(str(g.me.status))


def print_time():
    global start_time
    current_time = time.time()
    duration = (current_time - start_time)//1
    sec = duration % 60
    min = (duration % (60 * 60)) // 60
    hour = (duration % (24 * 60 * 60)) // (60 * 60)
    day = duration // (24 * 60 * 60)
    time_string = "Duration: "
    if day > 0:
        time_string += str(day) + " day"
        if day > 1:
            time_string += "s"
        time_string += ", "

    if hour > 0:
        time_string += str(hour) + " hour"
        if hour > 1:
            time_string += "s"
        time_string += ", "

    if min > 0:
        time_string += str(min) + " minute"
        if min > 1:
            time_string += "s"
        time_string += ", "

    if sec > 0:
        time_string += str(sec) + " second"
        if sec > 1:
            time_string += "s"

    if sec == 0:
        time_string = time_string[:-2]

    print(time_string)


async def changes():
    global id_int
    add_test(id_int, str(id_int))
    id_int += 1

    if id_int > 200:
        x = random.randrange(1, 199)
        y = random.randrange(1, 199)
        update_test(x, str(y))

    if id_int > 200:
        remove_test(id_int)


async def main_update():
    # Printing time
    print_time()

    # Printing status
    print_status()


async def background_update():
    await client.wait_until_ready()
    while not client.is_closed():
        await main_update()
        await asyncio.sleep(60)


async def faster_update():
    await client.wait_until_ready()
    while not client.is_closeD():
        await changes()
        await asyncio.sleep(1)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    await client.process_commands(message)


@client.command()
async def add(ctx, *, user):
    user = user.lower()
    add_user(user, ctx.guild.id)


@client.command()
async def remove(ctx, *, user):
    user = user.lower()
    remove_user(user, ctx.guild.id)


@client.command()
async def set_channel(ctx):
    mub_db.update_guild(ctx.guild.id, ctx.channel.id)


@client.event
async def on_ready():
    global tasks_created
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    if not tasks_created:
        client.loop.create_task(background_update())
        tasks_created = True

client.run(TOKEN)
