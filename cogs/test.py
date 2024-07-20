import discord
from discord.ext import commands

import requests


class Test(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is ready!")
        await self.bot.change_presence(activity=discord.Game("Would you rather?"))
        
    @commands.command()
    async def ping(self, ctx):
        ping_embed = discord.Embed(title="Ping!", description="Latency in ms", color=discord.Color.blue())
        ping_embed.add_field(name=f"{self.bot.user.name}'s latency (ms)", value=f"{round(self.bot.latency*1000)}ms", inline=False)
        ping_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=ping_embed)
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = guild.text_channels[0]
        await channel.send(f"Hello, I'm {self.bot.user.name}! Play would you rather with me. Use !help to see my commands.")
        
    @commands.command(name='commands')
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="List of available commands", color=discord.Color.blue())
        embed.add_field(name="!ping", value="Shows the latency of the bot", inline=False)
        embed.add_field(name="!help", value="Shows this message", inline=False)
        embed.add_field(name="!play", value="Starts a game of would you rather", inline=False)
        await ctx.send(embed=embed)
    
 
    @commands.command()
    async def play(self, ctx):        
        base_url = "https://api.truthordarebot.xyz/api/wyr"
        ratings = ["pg", "pg13", "r"]

        url = base_url + "?" + "&".join([f"rating={rating}" for rating in ratings])
        print(url + "\n")
        response = requests.get(url)

        # Checking if the request was successful
        if response.status_code == 200:
            data = response.json()
            question = data.get("question")
            
            embeded_msg = discord.Embed(title=question, color=discord.Color.blue())
            embeded_msg.set_thumbnail(url=ctx.author.avatar)
            embeded_msg.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embeded_msg)

        else:
            print("Failed to retrieve data from the API")



async def setup(bot):
    await bot.add_cog(Test(bot))  