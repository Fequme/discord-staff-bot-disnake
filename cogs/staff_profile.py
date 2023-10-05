import disnake
from disnake.ext import commands
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from config import *
import requests
from io import BytesIO
import asyncio

class profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="staff")
    async def staff(self, inter):
        pass

    @staff.sub_command(
        name='profile',
        description='Посмотреть стафф профиль'
    )
    async def profile(self, inter, пользователь: disnake.Member = None):
        if пользователь == None:
            пользователь = inter.user
        global user
        user = пользователь
        if STAFF_ROLE in [role.id for role in пользователь.roles]:
            await inter.response.defer()
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            font_o = ImageFont.truetype("assets/name.ttf", size=25)
            font_s = ImageFont.truetype("assets/status.ttf", size=35)
            if пользователь.avatar is None:
                 url1 = Q_IMAGE
            else:
                 url1 = пользователь.avatar.url
            response = requests.get(url1)
            avatar = Image.open(BytesIO(response.content))
            avatar = avatar.resize((225, 225), Image.ANTIALIAS)
            mask = Image.new("L", avatar.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 225, 225), fill=255)
            user_card = Image.open('assets/profile.png')

            cursor.execute("SELECT points FROM users WHERE user_id = ?", (пользователь.id,))
            result = cursor.fetchone()

            points = result[0]
            cursor.execute("SELECT warn FROM users WHERE user_id = ?", (пользователь.id,))
            result2 = cursor.fetchone()
            warns = result2[0]
            cursor.execute("SELECT time FROM users WHERE user_id = ?", (пользователь.id,))
            result3 = cursor.fetchone()
            online = result3[0]
            cursor.execute("SELECT otpysk FROM users WHERE user_id = ?", (пользователь.id,))
            result4 = cursor.fetchone()
            otpysk = result4[0]
            cursor.execute("SELECT role FROM users WHERE user_id = ?", (пользователь.id,))
            result5 = cursor.fetchone()
            rab = result5[0]

            minutes = int(online % 60)
            hour = int(online // 60)
            if hour < 1:
                hour = 0
            if minutes < 1 or minutes >= 60:
                minutes = 0
            maxx = PRED

            idraw = ImageDraw.Draw(user_card)

            idraw.text((130, 200), str(f'{hour}ч. {minutes}м.'), (255, 255, 255), font=font_o)
            idraw.text((670, 200), str(points), (255, 255, 255), font=font_o)
            idraw.text((620, 320), str(f'{warns} из {maxx}'), (255, 255, 255), font=font_o)
            idraw.text((350, 460), str(f'{rab}'), (255, 255, 255), font=font_o)
            if otpysk > 0:
                idraw.text((130, 320), str(f'ещё {otpysk} дней'), (255, 255, 255), font=font_o)
            else:
                idraw.text((130, 320), str(f'Не в отпуске'), (255, 255, 255), font=font_o)

            user_card.paste(avatar, (317, 112), mask)
            user_card.save('assets/profile_file.png', quality=95)
            file = disnake.File("assets/profile_file.png", filename="profile.png")
            view = disnake.ui.View()
            if CURATOR in [role.id for role in inter.user.roles] or \
                ADMIN in [role.id for role in inter.user.roles]:
                view.add_item(disnake.ui.Button(label="Выдать поинты", style=disnake.ButtonStyle.gray, custom_id="points"))
            else:
                view.add_item(disnake.ui.Button(label="Выдать поинты", style=disnake.ButtonStyle.gray, custom_id="points", disabled=True))
            if CURATOR in [role.id for role in inter.user.roles] or \
                ADMIN in [role.id for role in inter.user.roles]:
                view.add_item(disnake.ui.Button(label="Забрать поинты", style=disnake.ButtonStyle.gray, custom_id="upoints"))
            else:
                view.add_item(disnake.ui.Button(label="Забрать поинты", style=disnake.ButtonStyle.gray, custom_id="upoints", disabled=True))
            if пользователь.id == inter.user.id:
                view.add_item(disnake.ui.Button(label="Взять отпуск", style=disnake.ButtonStyle.gray, custom_id="otpesk"))
            else:
                view.add_item(disnake.ui.Button(label="Взять отпуск", style=disnake.ButtonStyle.gray, custom_id="otpesk", disabled=True))
            view.add_item(disnake.ui.Button(label="Выйти", style=disnake.ButtonStyle.red, custom_id="back"))
            await inter.send(file=file, view=view)
        else:
            embed = disnake.Embed(description="Пользователь **не является** участником стаффа", color=0x2b2d31)
            if пользователь.avatar is None:
                 embed.set_thumbnail(url=Q_IMAGE)
            else:
                 embed.set_thumbnail(url=пользователь.avatar.url)
            embed.set_author(name="Ой, ошибка", icon_url=f"{IMAGE}")
            await inter.send(embed=embed, ephemeral=True)
        conn.commit()
        conn.close()


    @staff.sub_command(name="top", description="Топ-10 по поинтам")
    async def top(self, inter):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        pointss = self.client.get_emoji(POINTSS)
        cursor.execute("SELECT user_id, points FROM users ORDER BY points DESC LIMIT 10")
        top_users = cursor.fetchall()

        embed = disnake.Embed(title="Топ-10 участников по поинтам", color=0x2b2d31)

        if top_users:
            for index, (user_id, points) in enumerate(top_users[:3], start=1):
                user = self.client.get_user(user_id)
                embed.add_field(name=f"{index}. {user.name}", value=f"{points} {pointss}", inline=True)

            if len(top_users) > 3:
                other_users_info = "\n".join([f"{index+3}. {self.client.get_user(user_id).name} - {points} {pointss}" for index, (user_id, points) in enumerate(top_users[3:], start=3)])
                embed.add_field(name="Остальные места", value=other_users_info, inline=True)
                embed.set_thumbnail(url=inter.guild.icon.url)
        else:
            embed.add_field(name="Нет данных", value="Нет данных для отображения топ-10.", inline=True)
            embed.set_thumbnail(url=inter.guild.icon.url)
        conn.commit()
        conn.close()
        await inter.send(embed=embed)
        

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            otp = disnake.utils.get(inter.guild.roles, id = OTPYSK)
            if inter.data.custom_id == "back":
                await inter.message.delete()
            if inter.data.custom_id == "otpesk":
                embed = disnake.Embed(description="Выберите, на какой **срок** вы хотите **взять** отпуск", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                embed.set_footer(text="Цена 1 дня отпуска - 100 поинтов!")
                view = disnake.ui.View()
                cursor.execute("SELECT points FROM users WHERE user_id = ?", (user.id,))
                result3 = cursor.fetchone()
                points = result3[0]
                if points >= 100:
                    view.add_item(disnake.ui.Button(label="1 день", style=disnake.ButtonStyle.gray, custom_id="one"))
                else:
                    view.add_item(disnake.ui.Button(label="1 день", style=disnake.ButtonStyle.gray, custom_id="one", disabled=True))
                if points >= 200:
                    view.add_item(disnake.ui.Button(label="2 дня", style=disnake.ButtonStyle.gray, custom_id="two"))
                else:
                    view.add_item(disnake.ui.Button(label="2 дня", style=disnake.ButtonStyle.gray, custom_id="two", disabled=True))
                if points >= 300:
                    view.add_item(disnake.ui.Button(label="3 дня", style=disnake.ButtonStyle.gray, custom_id="tre"))
                else:
                    view.add_item(disnake.ui.Button(label="3 дня", style=disnake.ButtonStyle.gray, custom_id="tre", disabled=True))
                if points >= 700:
                    view.add_item(disnake.ui.Button(label="7 дней", style=disnake.ButtonStyle.gray, custom_id="week"))
                else:
                    view.add_item(disnake.ui.Button(label="7 дней", style=disnake.ButtonStyle.gray, custom_id="week", disabled=True))
                view.add_item(disnake.ui.Button(label="Выйти", style=disnake.ButtonStyle.red, custom_id="back"))
                await inter.send(embed=embed, view=view)
            conn.commit()

            # ОТПУСКИ

            if inter.data.custom_id == "one":
                pointss = self.client.get_emoji(POINTSS)
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **взять** отпуск на **1** день?\nЦена **100** {pointss}", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="dada"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="nono"))
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()
            
            if inter.data.custom_id == "two":
                pointss = self.client.get_emoji(POINTSS)
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **взять** отпуск на **2** деня?\nЦена **200** {pointss}", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="dadada"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="nono"))
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "tre":
                pointss = self.client.get_emoji(POINTSS)
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **взять** отпуск на **3** деня?\nЦена **300** {pointss}", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="dadadada"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="nono"))
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "week":
                pointss = self.client.get_emoji(POINTSS)
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **взять** отпуск на **7** дней?\nЦена **700** {pointss}", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="dadadadada"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="nono"))
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "dada":
                embed = disnake.Embed(description="Вы **успешно** вышли в отпуск на **1** день!",  color=0x2b2d31)
                cursor.execute("UPDATE users SET points = points - 100, otpysk = otpysk + 1 WHERE user_id = ?", (user.id,))
                embed.set_footer(text=f"Возвращайтесь послезавтра")
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed)
                await user.add_roles(otp)
                conn.commit()

            if inter.data.custom_id == "dadada":
                embed = disnake.Embed(description="Вы **успешно** вышли в отпуск на **2** деня!",  color=0x2b2d31)
                cursor.execute("UPDATE users SET points = points - 200, otpysk = otpysk + 2 WHERE user_id = ?", (user.id,))
                embed.set_footer(text=f"Возвращайтесь через 2 дня")
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed)
                await user.add_roles(otp)
                conn.commit()

            if inter.data.custom_id == "dadadada":
                embed = disnake.Embed(description="Вы **успешно** вышли в отпуск на **3** деня!",  color=0x2b2d31)
                cursor.execute("UPDATE users SET points = points - 300, otpysk = otpysk + 3 WHERE user_id = ?", (user.id,))
                embed.set_footer(text=f"Возвращайтесь через 3 дня")
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed)
                await user.add_roles(otp)
                conn.commit()

            if inter.data.custom_id == "dadadadada":
                embed = disnake.Embed(description="Вы **успешно** вышли в отпуск на **7** дней!",  color=0x2b2d31)
                cursor.execute("UPDATE users SET points = points - 700, otpysk = otpysk + 7 WHERE user_id = ?", (user.id,))
                embed.set_footer(text=f"Возвращайтесь через 7 дней")
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Отпуск", icon_url=f"{IMAGE}")
                await inter.send(embed=embed)
                await user.add_roles(otp)
                conn.commit()


            # ВЫДАЧА / СНЯТИЕ ПОИНТОВ

            if inter.data.custom_id == "points":
                embed = disnake.Embed(description=f"Выберите, сколько **поинтов** стаффа вы хотите **выдать** пользователю {user.mention}", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Выдача поинтов", icon_url=f"{IMAGE}")
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="100", style=disnake.ButtonStyle.gray, custom_id="sto"))
                view.add_item(disnake.ui.Button(label="200", style=disnake.ButtonStyle.gray, custom_id="dve"))
                view.add_item(disnake.ui.Button(label="250", style=disnake.ButtonStyle.gray, custom_id="dvep"))
                view.add_item(disnake.ui.Button(label="Другое", style=disnake.ButtonStyle.gray, custom_id="givvee"))
                await inter.send(embed=embed, view=view)

            if inter.data.custom_id == "upoints":
                embed = disnake.Embed(description=f"Выберите, сколько **поинтов** стаффа вы хотите **забрыть** у пользователя {user.mention}", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Снятие поинтов", icon_url=f"{IMAGE}")
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="100", style=disnake.ButtonStyle.gray, custom_id="сто"))
                view.add_item(disnake.ui.Button(label="200", style=disnake.ButtonStyle.gray, custom_id="две"))
                view.add_item(disnake.ui.Button(label="250", style=disnake.ButtonStyle.gray, custom_id="двес"))
                view.add_item(disnake.ui.Button(label="Другое", style=disnake.ButtonStyle.gray, custom_id="другое"))
                await inter.send(embed=embed, view=view)

            if inter.data.custom_id == "givvee":
                def check(m):
                    return m.author == inter.author and m.channel == inter.channel
                await inter.send("Введите количество баллов (только цифры):", ephemeral=True)

                try:
                    msg = await self.client.wait_for('message', check=check, timeout=30.0)
                    points = int(msg.content)

                    await msg.delete()
                    user_id = user.id
                    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
                    conn.commit()
                    await inter.send(f"Поинты ({points}) были добавлены для пользователя {user.mention}", ephemeral=True)
                except ValueError:
                    await inter.send("Вы ввели некорректное значение. Введите только цифры.")
                except asyncio.TimeoutError:
                    await inter.send("Время ожидания истекло.")
        
            if inter.data.custom_id == "sto":
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **выдать** поинты стаффа **100**", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="да"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="нет"))
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "dve":
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **выдать** поинты стаффа **200**", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="дада"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="нет"))
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "dvep":
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **выдать** поинты стаффа **250**", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="дадада"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="нет"))
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "да":
                await inter.message.delete(delay=5)
                cursor.execute("UPDATE users SET points = points + 100 WHERE user_id = ?", (user.id,))
                embed = disnake.Embed(description=f"Вы **успешно** выдали **100** поинтов стаффа пользователю.", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, ephemeral=True)
                conn.commit()

            if inter.data.custom_id == "дада":
                await inter.message.delete(delay=5)
                cursor.execute("UPDATE users SET points = points + 200 WHERE user_id = ?", (user.id,))
                embed = disnake.Embed(description=f"Вы **успешно** выдали **200** поинтов стаффа пользователю.", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, ephemeral=True)
                conn.commit()

            if inter.data.custom_id == "дадада":
                await inter.message.delete(delay=5)
                cursor.execute("UPDATE users SET points = points + 250 WHERE user_id = ?", (user.id,))
                embed = disnake.Embed(description=f"Вы **успешно** выдали **250** поинтов стаффа пользователю.", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, ephemeral=True)
                conn.commit()

            if inter.data.custom_id == "нет":
                await inter.message.delete()
    
            if inter.data.custom_id == "nono":
                await inter.message.delete()

            if inter.data.custom_id == "сто":
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **забрать** поинты стаффа **100**", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="dad"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="нет"))
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "две":
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **забрать** поинты стаффа **200**", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="dadd"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="нет"))
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "двес":
                embed = disnake.Embed(description=f"Вы **уверены** что хотите **забрать** поинты стаффа **250**", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daddd"))
                view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="нет"))
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, view=view)
                conn.commit()

            if inter.data.custom_id == "dad":
                await inter.message.delete(delay=5)
                cursor.execute("UPDATE users SET points = points - 100 WHERE user_id = ?", (user.id,))
                embed = disnake.Embed(description=f"Вы **успешно** забрали **100** поинтов стаффа пользователю.", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, ephemeral=True)
                conn.commit()

            if inter.data.custom_id == "dadd":
                await inter.message.delete(delay=5)
                cursor.execute("UPDATE users SET points = points - 200 WHERE user_id = ?", (user.id,))
                embed = disnake.Embed(description=f"Вы **успешно** забрали **200** поинтов стаффа пользователю.", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, ephemeral=True)
                conn.commit()

            if inter.data.custom_id == "daddd":
                await inter.message.delete(delay=5)
                cursor.execute("UPDATE users SET points = points - 250 WHERE user_id = ?", (user.id,))
                embed = disnake.Embed(description=f"Вы **успешно** забрали **250** поинтов стаффа пользователю.", color=0x2b2d31)
                if user.avatar is None:
                     embed.set_thumbnail(url=Q_IMAGE)
                else:
                     embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Поинты", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, ephemeral=True)
                conn.commit()

            if inter.data.custom_id == "другое":
                def check(m):
                    return m.author == inter.author and m.channel == inter.channel
                await inter.send("Введите количество баллов (только цифры):", ephemeral=True)

                try:
                    msg = await self.client.wait_for('message', check=check, timeout=30.0)
                    points = int(msg.content)

                    await msg.delete()
                    user_id = user.id
                    cursor.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (points, user_id))
                    conn.commit()
                    await inter.send(f"Поинты ({points}) были забраны для пользователя {user.mention}", ephemeral=True)
                except ValueError:
                    await inter.send("Вы ввели некорректное значение. Введите только цифры.")
                except asyncio.TimeoutError:
                    await inter.send("Время ожидания истекло.")

def setup(client):
    client.add_cog(profile(client))
    print("Стафф: `профиль` включён")