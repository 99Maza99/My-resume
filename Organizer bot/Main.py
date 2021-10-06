import discord
import os,time
from discord import channel
from discord.ext import commands,tasks
import mysql.connector
import pytz
import datetime
from datetime import timezone,timedelta
import re

def convertutc(dt, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    dt = datetime.datetime.strptime(dt,"%H:%M")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%H:%M")

    return dt


print("Please enter the following data to connect to MySql")
host = input("Host: ")
port = input("Port: ")
user = input("User: ")
password = input("Password: ")
database = input("Database: ")
token = input("Bot Token: ")
timezone = pytz.timezone("UTC")

conn = mysql.connector.connect(host=host ,user=user ,passwd=password ,database=database, port=port)


c = conn.cursor()
print(conn)


c.execute("""CREATE TABLE IF NOT EXISTS records(username TEXT(200), userid TEXT(30), title TEXT(500), date DATE, message TEXT(2000), alarm TIME)""")
conn.commit()



client = commands.Bot(command_prefix = '_')

@client.event
async def on_ready():
    print('Logged in as: '+ str(client.get_user(client.user.id)))
    print("ID: "+ str(client.user.id))
    main.start()



@tasks.loop(seconds=60)
async def main():
    print("1 minute")
    e = datetime.datetime.now(timezone)
    current = str(e.hour)+":"+str(e.minute)+":00"
    time = datetime.datetime.strptime(current,'%H:%M:%S').time()
    print(time)
    c.execute(f"""SELECT * FROM records WHERE alarm = '{time}'""")
    data = c.fetchall()
    if data != [] :
        for record in data :
            userid = record[1]
            channel = await client.fetch_user(userid)
            embedVar = discord.Embed(title="Daily alarm !!", description="Your daily alarm", color=0x00ff00)
            embedVar.add_field(name=record[1], value=record[3], inline=False)
            await channel.send(embed=embedVar)
            print("Sent to user " + record[0])


@client.command()
async def sheet(ctx) :
    await ctx.send("Hello !, please copy the following sheet, and send it after modifying whats between <> !, don't forget to use _submit before sending")
    await ctx.send("<Title of your alarm> <Message of your alarm> <Time of your alarm> <Time zone using (`Continent/Capital-of-country`)>")

@client.command()
async def submit(ctx) :
    await ctx.send("Your submission is being processed please wait")
    message = ctx.message.content
    info = re.findall('<(.+?)>',message)
    time = str(ctx.message.created_at.date())

    
    user = ctx.message.author
    userid = user.id
    
    try :
        alarm = convertutc(info[2],info[3],"UTC")
        record = (str(user) , str(userid), str(info[0]), str(time), str(info[1]), str(alarm))
        c.execute("""INSERT INTO records (username,userid,title,date,message,alarm) VALUES (%s,%s,%s,%s,%s,%s)""",record  )
        conn.commit()
        await ctx.send(f"SAVED, I'll be reminding you of {info[0]} everyday at {info[2]}")
        return
    except :
        await ctx.send("A problem occured, please make sure you followed the steps correctly ! Try using _example for more clarification !")



client.run(token)