import disnake
from disnake.ext import commands
from config import *
from disnake.ui import Button, View
import sqlite3


class SetsAnnounce(disnake.Embed):
    def __init__(self):
        super().__init__(
            description=(
                ''
            ),
            color=disnake.Color.from_rgb(47, 49, 54),
        )
        self.set_image(url=f'{NABOR_ICON}')
        
class SetsAnnounce1(disnake.Embed):
    def __init__(self):
        super().__init__(
            description=(
                f'{TEXT}'
            ),
            color=disnake.Color.from_rgb(47, 49, 54),
        )
        self.set_image(url=f'{POLOSKA}')


class ModalsView(disnake.ui.Modal):
    def __init__(self, one):
        self.one = one
        components = [
            disnake.ui.TextInput(
                label=f"{Q1}", 
                placeholder=f"{O1}", 
                custom_id="nameage", 
                max_length=20,
            ),
            disnake.ui.TextInput(
                label=f"{Q2}", 
                placeholder=F"{O2}", 
                custom_id="primetime", 
                max_length=20,
            ),
            disnake.ui.TextInput(
                label=f"{Q3}", 
                placeholder=F"{O3}", 
                custom_id="pochemu", 
                style=disnake.TextInputStyle.paragraph,
                max_length=100,
            ),
            disnake.ui.TextInput(
                label=F"{Q4}", 
                placeholder=F"{O4}", 
                custom_id="workbefore", 
                max_length=20,
            ),
            disnake.ui.TextInput(
                label=F"{Q5}", 
                placeholder=F"{O5}", 
                custom_id="characterfield", 
                style=disnake.TextInputStyle.paragraph,
                max_length=100,
            ),
        ]
        super().__init__(title=f"Заявка на {one}", components=components)

    async def callback(self, interaction) -> None:
        embed = disnake.Embed(description="> Ваша заявка отправлена", color=0x2f3136)
        if self.one == 'Moderator':
            
            channel_id = MODER_NABOR
            channel = None
            if channel_id is not None:
                channel = disnake.utils.get(interaction.guild.text_channels, id=channel_id)
            if channel is not None:
                view = buttons()
                await channel.send(f'<@{interaction.author.id}>', embed=SetsEmbed(interaction,self.one), view=view)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                await interaction.response.send_message('Канал не найден.', ephemeral=True)
                
        if self.one == 'Support':
            channel_id = SUP_NABOR
            channel = None
            if channel_id is not None:
                channel = disnake.utils.get(interaction.guild.text_channels, id=channel_id)
            if channel is not None:
                await channel.send(f'<@{interaction.author.id}>', embed=SetsEmbed(interaction,self.one))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message('Канал не найден.', ephemeral=True)
                
        if self.one == 'TribuneMod':
            channel_id = TRI_NABOR
            channel = None
            if channel_id is not None:
                channel = disnake.utils.get(interaction.guild.text_channels, id=channel_id)
            if channel is not None:
                await channel.send(f'<@{interaction.author.id}>', embed=SetsEmbed(interaction,self.one))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message('Канал не найден.', ephemeral=True)
                
        if self.one == 'EventsMod':
            channel_id = EVENTS_NABOR
            channel = None
            if channel_id is not None:
                channel = disnake.utils.get(interaction.guild.text_channels, id=channel_id)
            if channel is not None:
                await channel.send(f'<@{interaction.author.id}>', embed=SetsEmbed(interaction,self.one))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message('Канал не найден.', ephemeral=True)
                
        if self.one == 'Creative':
            channel_id = CREATIVE_NABOR
            channel = None
            if channel_id is not None:
                channel = disnake.utils.get(interaction.guild.text_channels, id=channel_id)
            if channel is not None:
                await channel.send(f'<@{interaction.author.id}>', embed=SetsEmbed(interaction,self.one))
                await interaction.response.send_message(embed=embed,  ephemeral=True)
            else:
                await interaction.response.send_message('Канал не найден.', ephemeral=True)
                
        if self.one == 'Media':
            channel_id = MADIA_NABOR
            channel = None
            if channel_id is not None:
                channel = disnake.utils.get(interaction.guild.text_channels, id=channel_id)
            if channel is not None:
                await channel.send(f'<@{interaction.author.id}>', embed=SetsEmbed(interaction,self.one))
                await interaction.response.send_message(embed=embed,  ephemeral=True)
            else:
                await interaction.response.send_message('Канал не найден.', ephemeral=True)

class SelectSets(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @disnake.ui.select(
        custom_id='set',
        min_values=1,
        max_values=1,
        placeholder='Выберите необходимую должность',
        options=[
            disnake.SelectOption(
                label='Moderator',
                description='Подать заявку на пост Moderator',
                emoji=F'{EMO}',
                value='moder'
            ),
            disnake.SelectOption(
                label='Support',
                description='Подать заявку на пост Support',
                emoji=F'{EMO}',
                value='sup'
            ),
            disnake.SelectOption(
                label='TribuneMod',
                description='Подать заявку на пост TribuneMod',
                emoji=F'{EMO}',
                value='tribune'
            ),
            disnake.SelectOption(
                label='Events Mod',
                description='Подать заявку на пост Events Mod',
                emoji=F'{EMO}',
                value='events'
            ),
            disnake.SelectOption(
                label='Media',
                description='Подать заявку на пост Media',
                emoji=f'{EMO}',
                value='media'
            ),
            disnake.SelectOption(
                label='Creative',
                description='Подать заявку на пост Creative',
                emoji=f'{EMO}',
                value='creativ'
            ),
        ]
    )
    async def select_callback(self, select: disnake.ui.Select, inter):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        if inter.values[0] == 'moder':
            cursor.execute("INSERT INTO nabor (user_id, number) VALUES (?, ?)", (inter.author.id, 0))
            conn.commit()
            await inter.response.send_modal(modal=ModalsView('Moderator'))
        elif inter.values[0] == 'sup':
            cursor.execute("INSERT INTO nabor (user_id, number) VALUES (?, ?)", (inter.author.id, 0))
            conn.commit()
            await inter.response.send_modal(modal=ModalsView('Support'))
        elif inter.values[0] == 'tribune':
            cursor.execute("INSERT INTO nabor (user_id, number) VALUES (?, ?)", (inter.author.id, 0))
            conn.commit()
            await inter.response.send_modal(modal=ModalsView('TribuneMod'))
        elif inter.values[0] == 'events':
            cursor.execute("INSERT INTO nabor (user_id, number) VALUES (?, ?)", (inter.author.id, 0))
            conn.commit()
            await inter.response.send_modal(modal=ModalsView('EventsMod'))
        elif inter.values[0] == 'creativ':
            cursor.execute("INSERT INTO nabor (user_id, number) VALUES (?, ?)", (inter.author.id, 0))
            conn.commit()
            await inter.response.send_modal(modal=ModalsView('Creative'))
        elif inter.values[0] == 'media':
            cursor.execute("INSERT INTO nabor (user_id, number) VALUES (?, ?)", (inter.author.id, 0))
            conn.commit()
            await inter.response.send_modal(modal=ModalsView('Media'))
        else:
            pass




class SetsEmbed(disnake.Embed):
    def __init__(self, interaction, two):
        super().__init__(
            title=f"Пользователь подал заявку на роль {two}",
            description=f"ID: **{interaction.author.id}**\nПользователь: **{interaction.author.name}**\n",
            color=disnake.Color.from_rgb(47, 49, 54),
        )
        self.add_field(name=F"{Q1}", value=f"{interaction.text_values['nameage']}")
        self.add_field(name=F"{Q2}", value=f"{interaction.text_values['primetime']}", inline=False)
        self.add_field(name=f"{Q3}", value=f"{interaction.text_values['pochemu']}", inline=False)
        self.add_field(name=F"{Q4}", value=f"{interaction.text_values['workbefore']}", inline=False)
        self.add_field(name=F"{Q5}", value=f"{interaction.text_values['characterfield']}", inline=False)



class buttons(View):
    def __init__(self):
        super().__init__()


    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, custom_id="пр")
    async def yes_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        role = disnake.utils.get(interaction.guild.roles, id=SOBES_ROLE_ID)
        await interaction.response.send_message("Вы приняли заявку, теперь напишите пользователю о проведении собеседования. Роль была выдана", ephemeral=True)
        await interaction.author.add_roles(role)
        embed = disnake.Embed(description="Ваша заявка **принята**, ожидайте **ответа** когда вам назначат собеседование", color=disnake.Color.from_rgb(47, 49, 54))
        embed.set_thumbnail(url=interaction.author.avatar.url)
        embed.set_author(name="Заявка", icon_url=IMAGE)
        await interaction.author.send(embed=embed)
        cursor.execute("DELETE FROM nabor WHERE user_id = ?", (interaction.author.id,))
        conn.commit()

    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.red, custom_id="от")
    async def no_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM nabor WHERE user_id = ?", (interaction.author.id,))
        await interaction.message.delete()
        conn.commit()

    @disnake.ui.button(label="На рассмотрении", style=disnake.ButtonStyle.gray, custom_id="на")
    async def yzr_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT number FROM nabor WHERE user_id = ?", (interaction.author.id,))
        result = cursor.fetchone()
        if result[0] == 0:
            conn.commit()
            embed = disnake.Embed(description="Ваша заявка **рассматривается**, ожидайте **ответа**, если ответ не **поступит** - вас **не** приняли", color=disnake.Color.from_rgb(47, 49, 54))
            embed.set_thumbnail(url=interaction.author.avatar.url)
            embed.set_author(name="Заявка", icon_url=IMAGE)
            await interaction.author.send(embed=embed)
            await interaction.send("Отправлено")
            cursor.execute("UPDATE nabor SET number = number + 1 WHERE user_id = ?", (interaction.author.id,))
            conn.commit()
        else:
            await interaction.send("Она уже на рассмотрении", ephemeral=True)
