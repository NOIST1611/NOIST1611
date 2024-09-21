import random
import disnake
from disnake.ext import commands
from jokes import get_jokes

class Config:
    token = "MTI4NDA4NjUxMTEyOTg1ODE0Mg.G02IXW.G6tagP4V_l15pmPEN73RhCjogyUhlkHskLbVn8"
    intents = disnake.Intents.all()
    prefix = "?"
    test_guild = [1283519532480073801]
    game = disnake.Game(name="Играет в Rooms: The weird incident")
    status = disnake.Status.dnd
    embedColor = disnake.Colour.from_rgb(255, 255, 255)

Config.intents.members = True

bot = commands.Bot(command_prefix=Config.prefix, intents=Config.intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} started")
    await bot.change_presence(status=Config.status, activity=Config.game)

@bot.event
async def on_message(message):
    if message.channel.id == 1283649513805840404:
        await message.add_reaction("⭐")
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        
        thread = await message.create_thread(
            name=f"Обсуждение: {message.author.name}",
            auto_archive_duration=60,
        )
        await thread.send(f"Эта ветка автоматически создана для обсуждения работы от {message.author.mention}")


    await bot.process_commands(message)

@bot.event
async def on_member_join(member: disnake.Member):
    channel = bot.get_channel(1285938939475267586)
    role = member.guild.get_role(1283520453566009374)

    color = Config.embedColor
    embed = disnake.Embed(title="Приветствую!😃", description=f"Привет,{member.mention} приветствую тебя на сервера NOSIT STUDIO.Прочитай правила и приятного время провождения!", color=color)
    embed.set_thumbnail(member.avatar.url)

    if channel and role:
        await member.add_roles(role)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member: disnake.Member):
    channel = bot.get_channel(1285938939475267586)

    color = Config.embedColor
    embed = disnake.Embed(title="Прощай😢!", description=f"Прощай,{member.mention} надеюсь ты вернешься!", color=color)
    embed.set_thumbnail(member.avatar.url)

    if channel:
        await channel.send(embed=embed)

@bot.slash_command(name="help", description="Показьвает основную информацию о боте")
async def help_main(interaction):
    color = Config.embedColor
    embed = disnake.Embed(title="Приветствую!😃", description="Привет я бот для сервера NOSIT Studio, ты можешь посмотреть команды с помощью /info", color=color)
    embed.add_field(name="Больше обо мне 🤨", value="Аналог juniperBot и прочих ботов для сервера NOSIT Studio")
    embed.add_field(name="Версия бота 🤖", value="1.0")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="info", description="Всё команды")
async def mainInfo(interaction):
    color = Config.embedColor
    embed = disnake.Embed(title="Команды! 🤖", description="", color=color)
    embed.add_field(name="Основные Команды 💬", value="/help - показьвает основную информацию о боте")
    embed.add_field(name="Модерация 🔰", value="/kick -- исключает определенного пользователя с сервера  /timeout -- Мутит участника на определенное время  /ban -- Банит участника на сервере")
    embed.add_field(name="Развлечение 😃", value="/question -- задай вопрос боту на который он ответит")
    await interaction.response.send_message(embed=embed)

# Модерация

@bot.slash_command(name="kick", description="Кикает участника с сервера, доступно только модераторам или админам")
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(interaction, member: disnake.Member, reason="без причины"):
    color = Config.embedColor
    embed = disnake.Embed(title=f"{member.mention} был исключен", description=f"Участник {interaction.author.mention} исключил участника {member.mention} с причиной: {reason}", color=color)
    await interaction.response.send_message(embed=embed)
    await member.kick(reason=reason)

@bot.slash_command(name="timeout", description="Мутит участника на сервере, доступно только модераторам или админам")
@commands.has_permissions(moderate_members=True, administrator=True)
async def timeout(interaction, member: disnake.Member, timeout: float, reason="без причины"):
    color = Config.embedColor
    embed = disnake.Embed(title=f"{member.mention} был лишен голоса", description=f"Участник {interaction.author.mention} лишил голоса участника {member.mention} с причиной: {reason}, время наказания: {timeout}", color=color)
    await interaction.response.send_message(embed=embed)
    await member.timeout(duration=timeout, reason=reason)

@bot.slash_command(name="ban", description="Банит участника с сервера, доступно только модераторам или админам")
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(interaction, member: disnake.Member, reason="без причины"):
    color = Config.embedColor
    embed = disnake.Embed(title=f"{member.mention} был забанен", description=f"Участник {interaction.author.mention} забанил участника {member.mention} с причиной: {reason}", color=color)
    await interaction.response.send_message(embed=embed)
    await member.ban(reason=reason)

# Развлечение

@bot.slash_command(name="question", description="Отвечает на вопрос который ты напишешь")
async def question_main(interaction, question: str):
    random_number = random.choice(["Однозначно да!✨", "Однозначно нет!😫", "Незнаю🤔", "Да👌", "Нет🙁"])
    color = Config.embedColor
    embed = disnake.Embed(title=f"{question}?", description=f"Мой ответ это {random_number}", color=color)
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="joke", description="Выдает одну из 100 шуток про программистов")
async def joke(interaction):
    await interaction.response.defer()
    jokes = get_jokes()  # Получаем список шуток с помощью функции
    random_joke = random.choice(jokes)
    color = Config.embedColor
    embed = disnake.Embed(title="Аххахахахах смотри какую шутку нашёл! 😂", description=f"{random_joke}!", color=color)
    await interaction.followup.send(embed=embed)



bot.run(Config.token)
