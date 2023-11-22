import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')



@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(bot.get_all_channels(), guild__name='MainBot', name='general')

    welcome_message = await channel.send(
        f"Welcome {member.mention} to the server! React to choose your role:\n"
        ":computer: for Developer\n"
        ":art: for Designer\n"
        ":bar_chart: for Data Scientist"
    )
    await welcome_message.add_reaction("💻")
    await welcome_message.add_reaction("🎨")
    await welcome_message.add_reaction("📊")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member == bot.user:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    roles = {
        "💻": "Developer",
        "🎨": "Designer",
        "📊": "Data Scientist"
    }

    selected_role = roles.get(payload.emoji.name)
    if selected_role:
        role = discord.utils.get(guild.roles, name=selected_role)
        if role:
            await member.add_roles(role)
            if selected_role == "Developer":
                # developer_channel = discord.utils.get(guild.channels, id="")
                developer_channel = discord.utils.get(bot.get_all_channels(), guild__name='MainBot', name='devs')

                await developer_channel.set_permissions(member, read_messages=True)
            elif selected_role == "Designer":
                # designer_channel = discord.utils.get(guild.channels, id="")
                designer_channel = discord.utils.get(bot.get_all_channels(), guild__name='MainBot', name='designers')

                await designer_channel.set_permissions(member, read_messages=True)
            elif selected_role == "Data Scientist":
                # data_scientist_channel = discord.utils.get(guild.channels, id="")
                data_scientist_channel = discord.utils.get(bot.get_all_channels(), guild__name='MainBot', name='data')

                await data_scientist_channel.set_permissions(member, read_messages=True)
        else:
            print(f"Role '{selected_role}' not found in the server.")


@bot.command()
async def hello(ctx):
    await ctx.send("hey there!")

@bot.command()
async def kickme(ctx):
    if ctx.guild.me.guild_permissions.kick_members:
        await ctx.author.kick(reason="Kicked by bot command")
        await ctx.send(f"{ctx.author.display_name} has been kicked.")
    else:
        await ctx.send("No permission to kick users")

bot.run('to run this script, check the bot token id and paste it here')
