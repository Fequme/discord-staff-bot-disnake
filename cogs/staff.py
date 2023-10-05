import disnake
from disnake.ext import commands
from config import *
import sqlite3
import asyncio

class staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='action', description='Управление персоналом сервера')
    async def action(self, inter, пользователь: disnake.Member = commands.Param(name="пользователь")):
        global user
        user = пользователь
        if UNVERIFY in [role.id for role in пользователь.roles] or \
           NEDOPYSK in [role.id for role in пользователь.roles]:
            embed = disnake.Embed(description="Вы не можете **управлять** этим пользователем, он **не прошёл** верефикацию или у него роль **недопуск**", color=0x2b2d31)
            if пользователь.avatar is None:
                 embed.set_thumbnail(url=Q_IMAGE)
            else:
                 embed.set_thumbnail(url=пользователь.avatar.url)
            embed.set_author(name="Ой, ошибка", icon_url=f"{IMAGE}")
            await inter.response.send_message(embed=embed)
        elif пользователь.id == inter.user.id:
            embed = disnake.Embed(description="Вы не можете не можете проводить **операцию** над собой", color=0x2b2d31)
            if пользователь.avatar is None:
                 embed.set_thumbnail(url=Q_IMAGE)
            else:
                 embed.set_thumbnail(url=пользователь.avatar.url)
            embed.set_author(name="Ты всегда так умом 'блещешь'?", icon_url=f"{IMAGE}")
            await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(description="Выберите **действие** которое хотите **сделать** с пользователем", color=0x2b2d31)    
            embed.set_author(name=f"Пользователь - {пользователь.name}", icon_url=f"{IMAGE}")
            if пользователь.avatar is None:
                 embed.set_thumbnail(url=Q_IMAGE)
            else:
                 embed.set_thumbnail(url=пользователь.avatar.url)
            view = disnake.ui.View()
            view.add_item(disnake.ui.Button(label="Выдача стафф ролей", style=disnake.ButtonStyle.gray, custom_id="give"))
            if STAFF_ROLE in [role.id for role in пользователь.roles]:
                view.add_item(disnake.ui.Button(label="Снятие стафф ролей", style=disnake.ButtonStyle.gray, custom_id="ungive"))
            else:
                view.add_item(disnake.ui.Button(label="Снятие стафф ролей", style=disnake.ButtonStyle.gray, custom_id="ungive", disabled=True))
            view.add_item(disnake.ui.Button(label="Выгововоры", style=disnake.ButtonStyle.green, custom_id="pred"))
            await inter.response.send_message(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            staffs = disnake.utils.get(inter.guild.roles, id = STAFF_ROLE)
            if inter.data.custom_id == "give":
                emb = disnake.Embed(description="Выберите **ветку** на которую хотите **поставить** пользователя",color=0x2f3136)
                emb.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                emb.set_footer(text="Чтобы выйти, просто нажмите кнопку ниже")
                if user.avatar is None:
                     emb.set_thumbnail(url=Q_IMAGE)
                else:
                     emb.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                if CONTROL == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="control", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CONTROLL}", style=disnake.ButtonStyle.gray, custom_id="control"))
                if MODER == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="moderator", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{MODERR}", style=disnake.ButtonStyle.gray, custom_id="moderator"))
                if EVENTS_MOD == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="events", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{EVENTS}", style=disnake.ButtonStyle.gray, custom_id="events"))
                if CLANS_STAFF == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="clans", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CLAN}", style=disnake.ButtonStyle.gray, custom_id="clans"))
                if MAFIA_MOD == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="mafia", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{MAFIA}", style=disnake.ButtonStyle.gray, custom_id="mafia"))
                if CREATIVE == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="creative", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CREATIVEE}", style=disnake.ButtonStyle.gray, custom_id="creative"))
                if SUPPORT == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="support", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{SUPPORTT}", style=disnake.ButtonStyle.gray, custom_id="support"))
                if CLOSE_MOD == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="close", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CLOSE}", style=disnake.ButtonStyle.gray, custom_id="close"))
                if TRIBUN_MOD == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="tribune", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{TRIBUNE}", style=disnake.ButtonStyle.gray, custom_id="tribune"))
                view.add_item(disnake.ui.Button(label="Выйти", style=disnake.ButtonStyle.red, custom_id="back"))
                await inter.send(embed=emb, view=view)


            if inter.data.custom_id == "control":
                if OTVE_CONTROL in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{CONTROLL}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yes"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "moderator":
                if OTVE_MODER in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{MODERR}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yess"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "events":
                if OTVE_EVENTS in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{EVENTS}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yesss"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)
                
            if inter.data.custom_id == "clans":
                if OTVE_CLANS in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{CLAN}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yessss"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "mafia":
                if OTVE_MAFIA in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{MAFIA}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yesssss"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)
    
            if inter.data.custom_id == "creative":
                if OTVE_CREATIVE in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{CREATIVE}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yessssss"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "support":
                if OTVE_SUPPORT in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{SUPPORTT}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yesssssss"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "close":
                if OTVE_CLOSE in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{CLOSE}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yessssssss"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "tribune":
                if OTVE_CLOSE in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nна должность **{TRIBUNE}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="yesssssssss"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** ставить людей **на эту ветку**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)


            # КОНТРОЛ

            if inter.data.custom_id == "yes":
                await inter.message.delete()
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{CONTROLL}"))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {CONTROLL}")
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                control = disnake.utils.get(inter.guild.roles, id = CONTROL)
                await user.add_roles(control)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # МОДЕР

            if inter.data.custom_id == "yess":
                await inter.message.delete()
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{MODERR}"))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {MODERR}")
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                moder = disnake.utils.get(inter.guild.roles, id = MODER)
                await user.add_roles(moder)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # ИВЕНТ МОД

            if inter.data.custom_id == "yesss":
                await inter.message.delete()
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{EVENTS}"))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {EVENTS}")
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                eve = disnake.utils.get(inter.guild.roles, id = EVENTS_MOD)
                await user.add_roles(eve)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # КЛАН СТАФФ

            if inter.data.custom_id == "yessss":
                await inter.message.delete()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {CLAN}")
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{CLAN}"))
                conn.commit()
                conn.close()
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                clan = disnake.utils.get(inter.guild.roles, id = CLANS_STAFF)
                await user.add_roles(clan)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # МАФИЯ МОД

            if inter.data.custom_id == "yesssss":
                await inter.message.delete()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {MAFIA}")
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{MAFIA}"))
                conn.commit()
                conn.close()
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                mafia = disnake.utils.get(inter.guild.roles, id = MAFIA_MOD)
                await user.add_roles(mafia)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # CREATIVE

            if inter.data.custom_id == "yessssss":
                await inter.message.delete()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {CREATIVEE}")
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{CREATIVEE}"))
                conn.commit()
                conn.close()
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                creative = disnake.utils.get(inter.guild.roles, id = CREATIVE)
                await user.add_roles(creative)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # SUPPORT

            if inter.data.custom_id == "yesssssss":
                await inter.message.delete()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {SUPPORTT}")
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{SUPPORTT}"))
                conn.commit()
                conn.close()
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                sup = disnake.utils.get(inter.guild.roles, id = SUPPORT)
                await user.add_roles(sup)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # CLOSE

            if inter.data.custom_id == "yessssssss":
                await inter.message.delete()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {CLOSE}")
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{CLOSE}"))
                conn.commit()
                conn.close()
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                close = disnake.utils.get(inter.guild.roles, id = CLOSE_MOD)
                await user.add_roles(close)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # tribune

            if inter.data.custom_id == "yesssssssss":
                await inter.message.delete()
                cursor.execute("INSERT INTO users (user_id, role) VALUES (?, ?)",(user.id, f"{TRIBUNE}"))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** поставили {user.mention} на должность {TRIBUNE}")
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                tri = disnake.utils.get(inter.guild.roles, id = TRIBUN_MOD)
                await user.add_roles(tri)
                await user.add_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            if inter.data.custom_id == "no":
                await inter.message.delete()
            if inter.data.custom_id == "back":
                await inter.message.delete()

            if inter.data.custom_id == "ungive":
                emb = disnake.Embed(description="Выберите **ветку** на с которой хотите **снять** пользователя",color=0x2f3136)
                emb.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                emb.set_footer(text="Чтобы выйти, просто нажмите кнопку ниже")
                if user.avatar is None:
                     emb.set_thumbnail(url=Q_IMAGE)
                else:
                     emb.set_thumbnail(url=user.avatar.url)
                view = disnake.ui.View()
                if CONTROL == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="control", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CONTROLL}", style=disnake.ButtonStyle.gray, custom_id="cont"))
                if MODER == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="moderator", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{MODERR}", style=disnake.ButtonStyle.gray, custom_id="mod"))
                if EVENTS_MOD == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="events", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{EVENTS}", style=disnake.ButtonStyle.gray, custom_id="eve"))
                if CLANS_STAFF == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="clans", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CLAN}", style=disnake.ButtonStyle.gray, custom_id="cla"))
                if MAFIA_MOD == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="mafia", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{MAFIA}", style=disnake.ButtonStyle.gray, custom_id="maf"))
                if CREATIVE == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="creative", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CREATIVEE}", style=disnake.ButtonStyle.gray, custom_id="cre"))
                if SUPPORT == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="support", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{SUPPORTT}", style=disnake.ButtonStyle.gray, custom_id="sup"))
                if CLOSE == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="close", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{CLOSE}", style=disnake.ButtonStyle.gray, custom_id="clo"))
                if TRIBUN_MOD == 123:
                    view.add_item(disnake.ui.Button(label=F"{NO}", style=disnake.ButtonStyle.gray, custom_id="tribune", disabled=True))
                else:
                    view.add_item(disnake.ui.Button(label=F"{TRIBUNE}", style=disnake.ButtonStyle.gray, custom_id="tru"))
                view.add_item(disnake.ui.Button(label="Выйти", style=disnake.ButtonStyle.red, custom_id="back"))
                await inter.send(embed=emb, view=view)

            if inter.data.custom_id == "cont":
                if OTVE_CONTROL in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{CONTROLL}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="da"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "mod":
                if OTVE_MODER in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{MODERR}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "eve":
                if OTVE_EVENTS in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{EVENTS}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daaa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)
                
            if inter.data.custom_id == "cla":
                if OTVE_CLANS in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{CLAN}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daaaa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "maf":
                if OTVE_MAFIA in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{MAFIA}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daaaa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)
    
            if inter.data.custom_id == "cre":
                if OTVE_CREATIVE in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **поставить** {user.mention}\nс должности **{CREATIVE}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daaaaa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "sup":
                if OTVE_SUPPORT in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{SUPPORTT}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daaaaaa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "clo":
                if OTVE_CLOSE in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{CLOSE}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daaaaaaa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "tru":
                if OTVE_CLOSE in [role.id for role in inter.user.roles]:
                    embed = disnake.Embed(description=f"Вы **уверены**, что хотите **снять** {user.mention}\nс должности **{TRIBUNE}**?", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    view = disnake.ui.View()
                    embed.set_author(name=f"Пользователь - {user.name}", icon_url=f"{IMAGE}")
                    view.add_item(disnake.ui.Button(label="Да", style=disnake.ButtonStyle.gray, custom_id="daaaaaaaa"))
                    view.add_item(disnake.ui.Button(label="Нет", style=disnake.ButtonStyle.gray, custom_id="no"))
                    await inter.send(embed=embed, view=view)
                else:
                    embed = disnake.Embed(description=f"Вы **не можете** снимать людей **с этой ветки**", color=0x2f3136)
                    if user.avatar is None:
                         embed.set_thumbnail(url=Q_IMAGE)
                    else:
                         embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name=f"Ой, ошибочка", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)


            # КОНТРОЛ

            if inter.data.custom_id == "da":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {CONTROLL}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                control = disnake.utils.get(inter.guild.roles, id = CONTROL)
                await user.remove_roles(control)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # МОДЕР

            if inter.data.custom_id == "daa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {MODERR}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                moder = disnake.utils.get(inter.guild.roles, id = MODER)
                await user.remove_roles(MODER)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # ИВЕНТ МОД

            if inter.data.custom_id == "daaa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {EVENTS}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                eve = disnake.utils.get(inter.guild.roles, id = EVENTS_MOD)
                await user.remove_roles(eve)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # КЛАН СТАФФ

            if inter.data.custom_id == "daaaa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {CLAN}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                clan = disnake.utils.get(inter.guild.roles, id = CLANS_STAFF)
                await user.remove_roles(clan)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # МАФИЯ МОД

            if inter.data.custom_id == "daaaaa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {MAFIA}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                mafia = disnake.utils.get(inter.guild.roles, id = MAFIA_MOD)
                await user.remove_roles(mafia)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # CREATIVE

            if inter.data.custom_id == "daaaaaa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {CREATIVEE}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                creative = disnake.utils.get(inter.guild.roles, id = CREATIVE)
                await user.remove_roles(creative)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # SUPPORT

            if inter.data.custom_id == "daaaaaaa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {SUPPORTT}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                supp = disnake.utils.get(inter.guild.roles, id = SUPPORT)
                await user.remove_roles(supp)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # CLOSE

            if inter.data.custom_id == "daaaaaaaa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {CLOSE}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                close = disnake.utils.get(inter.guild.roles, id = CLOSE_MOD)
                await user.remove_roles(close)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)

            # tribune

            if inter.data.custom_id == "daaaaaaaaa":
                await inter.message.delete()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
                conn.commit()
                conn.close()
                emb = disnake.Embed(description=f"Вы **успешно** сняли {user.mention} с должности {TRIBUNE}", color=0x2f3136)
                if user.avatar is None:
                    emb.set_thumbnail(url=Q_IMAGE)
                else:
                    emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name="Успех", icon_url=f"{IMAGE}")
                trii = disnake.utils.get(inter.guild.roles, id = TRIBUN_MOD)
                await user.remove_roles(trii)
                await user.remove_roles(staffs)
                await inter.send(embed=emb, ephemeral=True)


            # СИСТЕМА ВЫГОВОРОВ

            if inter.data.custom_id == "pred":
                embed = disnake.Embed(description="Выберите, какой **католог** вам нужен", color=0x2f3136)
                view = disnake.ui.View()
                if CURATOR in [role.id for role in inter.user.roles] or \
                MASTER in [role.id for role in inter.user.roles] or \
                ADMIN in [role.id for role in inter.user.roles]:
                    view.add_item(disnake.ui.Button(label="Выдать", style=disnake.ButtonStyle.gray, custom_id="vidat"))
                    view.add_item(disnake.ui.Button(label="Снять", style=disnake.ButtonStyle.gray, custom_id="snat"))
                else:
                    view.add_item(disnake.ui.Button(label="Выдать", style=disnake.ButtonStyle.gray, disabled=True, custom_id="vidat"))
                    view.add_item(disnake.ui.Button(label="Снять", style=disnake.ButtonStyle.gray, disabled=True, custom_id="snat"))
                view.add_item(disnake.ui.Button(label="Список выговоров", style=disnake.ButtonStyle.gray, custom_id="list"))
                if user.avatar is None:
                    embed.set_thumbnail(url=Q_IMAGE)
                else:
                    embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")
                await inter.send(embed=embed, ephemeral=True, view=view)

            if inter.data.custom_id == "vidat":
                view = disnake.ui.View()
                embed = disnake.Embed(description=f"Выберите, по какой **причине** вы хотите **выдать** выговор пользователю {user.mention}", color=0x2f3136)
                if user.avatar is None:
                    embed.set_thumbnail(url=Q_IMAGE)
                else:
                    embed.set_thumbnail(url=user.avatar.url)
                embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")
                view.add_item(disnake.ui.Button(label="Неадекват", style=disnake.ButtonStyle.gray, custom_id="neo"))
                view.add_item(disnake.ui.Button(label="Оскорбление", style=disnake.ButtonStyle.gray, custom_id="osk"))
                view.add_item(disnake.ui.Button(label="Нарушение правил", style=disnake.ButtonStyle.gray, custom_id="rule"))
                view.add_item(disnake.ui.Button(label="Другое", style=disnake.ButtonStyle.gray, custom_id="dryg"))
                await inter.send(embed=embed, view=view)

            if inter.data.custom_id == "neo":
                cursor.execute("UPDATE users SET warn = warn + 1 WHERE user_id = ?", (user.id,))
                conn.commit()
                cursor.execute("SELECT warn FROM users WHERE user_id = ?", (user.id,))
                result = cursor.fetchone()
                if result is not None:
                    warn_number = result[0]
                    real = "Неадекват"
                    conn.commit()
                    cursor.execute("INSERT INTO warn (user_id, number, real) VALUES (?, ?, ?)",
                                   (user.id, warn_number, real))
                    conn.commit()
                    conn.close()
                    embed = disnake.Embed(description=f"Вы успешно **выдали** выговор пользователю {user.mention}\n**Причина**: `Неадекват`", color=0x2f3136)
                    if user.avatar is None:
                        embed.set_thumbnail(url=Q_IMAGE)
                    else:
                        embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")                    
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    embed = disnake.Embed(description="Этот пользователь **не** участник стаффа")
                    if user.avatar is None:
                        embed.set_thumbnail(url=Q_IMAGE)
                    else:
                        embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "osk":
                cursor.execute("UPDATE users SET warn = warn + 1 WHERE user_id = ?", (user.id,))
                conn.commit()
                cursor.execute("SELECT warn FROM users WHERE user_id = ?", (user.id,))
                result = cursor.fetchone()
                if result is not None:
                    warn_number = result[0]
                    real = "Оскорбление"
                    conn.commit()
                    cursor.execute("INSERT INTO warn (user_id, number, real) VALUES (?, ?, ?)",
                                   (user.id, warn_number, real))
                    conn.commit()
                    conn.close()
                    embed = disnake.Embed(description=f"Вы успешно **выдали** выговор пользователю {user.mention}\n**Причина**: `Оскорбление`", color=0x2f3136)
                    if user.avatar is None:
                        embed.set_thumbnail(url=Q_IMAGE)
                    else:
                        embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")                    
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    embed = disnake.Embed(description="Этот пользователь **не** участник стаффа")
                    if user.avatar is None:
                        embed.set_thumbnail(url=Q_IMAGE)
                    else:
                        embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "rule":
                cursor.execute("UPDATE users SET warn = warn + 1 WHERE user_id = ?", (user.id,))
                conn.commit()
                cursor.execute("SELECT warn FROM users WHERE user_id = ?", (user.id,))
                result = cursor.fetchone()
                if result is not None:
                    warn_number = result[0]
                    real = "Нарушение правил"
                    conn.commit()
                    cursor.execute("INSERT INTO warn (user_id, number, real) VALUES (?, ?, ?)",
                                   (user.id, warn_number, real))
                    conn.commit()
                    conn.close()
                    embed = disnake.Embed(description=f"Вы успешно **выдали** выговор пользователю {user.mention}\n**Причина**: `Нарушение правил`", color=0x2f3136)
                    if user.avatar is None:
                        embed.set_thumbnail(url=Q_IMAGE)
                    else:
                        embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")                    
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    embed = disnake.Embed(description="Этот пользователь **не** участник стаффа")
                    if user.avatar is None:
                        embed.set_thumbnail(url=Q_IMAGE)
                    else:
                        embed.set_thumbnail(url=user.avatar.url)
                    embed.set_author(name="Выговоры", icon_url=f"{IMAGE}")
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "list":
                cursor.execute("SELECT number, real FROM warn WHERE user_id = ?", (user.id,))
                warning_records = cursor.fetchall()
            
                if warning_records:
                    embed = disnake.Embed(title=f"Выговоры пользователя - {user.name}", color=0x2f3136)
                    for index, (warn_number, real) in enumerate(warning_records, start=1):
                        embed.add_field(name=f"Выговор #{warn_number}", value=f"**Причина:** `{real}`", inline=False)
                    if user.avatar is None:
                        embed.set_thumbnail(url=Q_IMAGE)
                    else:
                        embed.set_thumbnail(url=user.avatar.url)
                    
                    await inter.send(embed=embed, ephemeral=True)
                else:
                    embed = disnake.Embed(description=f"У пользователя {user.mention} нет выговоров", color=0x2f3136)
                    await inter.send(embed=embed, ephemeral=True)

            if inter.data.custom_id == "dryg":
                def check(m):
                    return m.author == inter.author and m.channel == inter.channel
                await inter.send("Введите причину:", ephemeral=True)

                try:
                    user_response = await self.client.wait_for("message", check=check, timeout=60)
                    real = user_response.content

                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    user_id = user.id
                    cursor.execute("UPDATE users SET warn = warn + 1 WHERE user_id = ?", (user_id,))

                    cursor.execute("SELECT warn FROM users WHERE user_id = ?", (user_id,))
                    number = cursor.fetchone()
                    nunu = number[0]

                    cursor.execute("INSERT INTO warn (user_id, number, real) VALUES (?, ?, ?)", (user_id, nunu, real))
                    conn.commit()

                    await inter.send(f"Выговор для пользователя {user.mention} был выдан по причине `{real}`", ephemeral=True)
                except ValueError:
                    await inter.send("Вы ввели некорректное значение. Введите только цифры.")
                except asyncio.TimeoutError:
                    await inter.send("Время ожидания истекло.")

            if inter.data.custom_id == "snat":
                def check(m):
                    return m.author == inter.author and m.channel == inter.channel
                await inter.send("Введите индификатор (1/2...):", ephemeral=True)

                try:
                    user_response = await self.client.wait_for("message", check=check, timeout=60)
                    real = int(user_response.content)

                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    user_id = user.id
                    cursor.execute("UPDATE users SET warn = warn - 1 WHERE user_id = ?", (user_id,))
                    conn.commit()
                    cursor.execute("DELETE FROM warn WHERE user_id = ? AND number = ?", (user_id, real))
                    conn.commit()

                    await inter.send(f"Выговор для пользователя {user.mention} был снят", ephemeral=True)
                except ValueError:
                    await inter.send("Вы ввели некорректное значение. Введите только цифры.")
                except asyncio.TimeoutError:
                    await inter.send("Время ожидания истекло.")





def setup(client):
    client.add_cog(staff(client))
    print("Стафф: 'повышения' вкючен")