### All View Classes
import discord
import webPageFunctions
import botFunctionsEvents as botFunc
import botClassModalsEvents as botMod
import asyncio

#1 view for Proposing the event
class initialized_event(discord.ui.View):
    def __init__(self, guild, matching_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None
        self.matching_event = matching_event
        self.guild=guild

async def disable_buttons(self, interaction: discord.Interaction):
    # Disable all buttons in the view for the interacting user
    for item in self.children:
        if isinstance(item, discord.ui.Button):
            item.disabled = True

        
    # IamIn button
    @discord.ui.button(label='Lets do it', style=discord.ButtonStyle.green,custom_id='IN')      
    async def IamIN_button(self,  interaction:discord.Interaction, button: discord.ui.Button):

        # dataset refresh
        matching_event=botFunc.dataset_refresh(updateFlag=1,new_data=self.matching_event['name'],dateUSERID=interaction.user.id,timeUSER=interaction.user)

        # get the channel
        guild = interaction.guild
        channel_name = f"{matching_event['name']}"
        new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)

        # if 2 participants, create channel, send author the options
        if matching_event['num_participants'] == 2:
            if not new_channel:
                new_channel = await guild.create_text_channel(channel_name)
                await new_channel.set_permissions(guild.default_role, read_messages=False)
                # Grant read permissions to participants
                for participant_name in self.matching_event['participant_names']:
                    participant = discord.utils.get(guild.members, name=participant_name)
                    if participant:
                        await new_channel.set_permissions(participant, read_messages=True)
            author = discord.utils.get(guild.members, id=int(matching_event['author']))
            if author:
                dm_channel = await author.create_dm()
            view2 = joined_event(guild,matching_event)
            title_text = self.matching_event['name']
            underline_text = '\n' + '_' * len(title_text)  # Create underlining with underscores
            e = discord.Embed(
                title=f"Event Name: {matching_event['name']}{underline_text}",
                description='Somebody joined! Next stage:',
                color=0x7289da
                )
            await dm_channel.send(embed=e, view=view2)
        else:
            if not new_channel:
                new_channel = await guild.create_text_channel(channel_name)
                await new_channel.set_permissions(guild.default_role, read_messages=False)
                
            participant_name= str(interaction.user)
            participant = discord.utils.get(guild.members, name=participant_name)
            if participant:
                await new_channel.set_permissions(participant, read_messages=True)


        # Send the message with buttons and view
        await self.disable_buttons(interaction)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send('See you there!', ephemeral=True)

    # SendMe
    @discord.ui.button(label='See details', style=discord.ButtonStyle.gray,custom_id='SE')
    async def sendMe_button(self,  interaction:discord.Interaction, button: discord.ui.Button):

        # send the description of the event from DM
        guild = interaction.guild
        userINTRCTN = discord.utils.get(guild.members, id=interaction.user.id)
        if userINTRCTN:
            dm_channel = await userINTRCTN.create_dm()
        title_text = self.matching_event['name']
        underline_text = '\n' + '_' * len(title_text)  # Create underlining with underscores
        e = discord.Embed(
            title=f"{title_text}{underline_text}",
            description=f"Details: {self.matching_event['description']} ",
            color=0x7289da
            )
        await dm_channel.send(embed=e)

        # Send the message with buttons and view
        await interaction.response.edit_message(view=self)
        await interaction.followup.send('Check your DM!', ephemeral=True)




#2 view for Author Decisions
class joined_event(discord.ui.View):
    def __init__(self, guild, matching_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None
        self.matching_event = matching_event
        self.guild=guild

    async def disable_buttons(self):
        # Disable all buttons in the view
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

                    
    # set the time button
    @discord.ui.button(style=discord.ButtonStyle.green, custom_id='set_time', label='Set Time')
    async def set_time_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 1

     
        await interaction.response.send_message('Creating link for setting up the time (This can take a while)')

        # generate the links
        [public_link, admin_link]=webPageFunctions.create_poll(self.matching_event)
        
        # Send the public link to all participants
        for participant_name in self.matching_event['participant_ids']:
            user = discord.utils.get(self.guild.members, id=int(participant_name))
            if user:
                await user.send(f"Public Link for the poll: {public_link}")

        # Send the admin link to the author of the message
        author = discord.utils.get(self.guild.members, id=int(self.matching_event['author']))
        if author:
            await author.send(f'Admin Link for the poll: {admin_link}')
            await author.send("**Call the command:** ```/date_time``` ** to register the date and time**")
                
 

        # Disable the buttons and update the message
        await self.disable_buttons()
        await interaction.message.edit(view=self)



    # edit button
    @discord.ui.button(style=discord.ButtonStyle.gray, custom_id='edit', label='Edit')
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 1
        oldevname=self.matching_event['name']


        # ask for a new event
        await interaction.response.send_modal(botMod.edit_event())

        

        await asyncio.sleep(300)
        guild = self.guild
        channel_name = 'eventhorizon'
        channel1 = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)
        await botFunc.delete_given_event(discord.Interaction,channel1=channel1, followup= interaction.followup, eventname=oldevname,replaceflag=1,guild=guild)




        
        # Disable the buttons and update the message
        await self.disable_buttons()
        await interaction.message.edit(view=self)


    @discord.ui.button(style=discord.ButtonStyle.red, custom_id='cancel', label='Cancel')
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 1
        new_data = {
        'name':self.matching_event['name'],
        'interactionUserID':interaction.user.id
        }
        new_data=botFunc.dataset_refresh(updateFlag=4,new_data=new_data)
        
        # check for errors
        if new_data==0:
            return await interaction.followup.send(f"No event found with the name '{self.matching_event['name']}'.")
        if new_data==1:
            return await interaction.followup.send("You do not have permission to use this feature.")

        guild = self.guild
        channel_name = 'eventhorizon'
        channel1 = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)
        await botFunc.delete_given_event(discord.Interaction,channel1=channel1, followup= interaction.followup, eventname=self.matching_event['name'])

        # delete text channel
        channel_name = self.matching_event['name']
        new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)
        if  new_channel:
            await new_channel.delete()



        # Disable the buttons and update the message
        await self.disable_buttons()
        await interaction.message.edit(view=self)
        await interaction.response.send_message(f"Event '{self.matching_event['name']}' has been canceled.")


#1 view for Proposing the event
class initialized_event2(discord.ui.View):
    def __init__(self, guild, matching_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None
        self.matching_event = matching_event
        self.guild=guild

    async def disable_buttons(self):
        # Disable all buttons in the view
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        
    # IamIn button
    @discord.ui.button(label='Join!', style=discord.ButtonStyle.green,custom_id='IN')      
    async def IamIN_button(self,  interaction:discord.Interaction, button: discord.ui.Button):

        #button.disabled=True

        # dataset refresh
        matching_event=botFunc.dataset_refresh(updateFlag=1,new_data=self.matching_event['name'],dateUSERID=interaction.user.id,timeUSER=interaction.user)

        # get the channel
        guild = interaction.guild
        channel_name = f"{matching_event['name']}"
        new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)

        # if 2 participants, create channel, send author the options

        if not new_channel:
            new_channel = await guild.create_text_channel(channel_name)
            await new_channel.set_permissions(guild.default_role, read_messages=False)
           
        participant_name= str(interaction.user)
        participant = discord.utils.get(guild.members, name=participant_name)
        if participant:
            await new_channel.set_permissions(participant, read_messages=True)


        # Send the message with buttons and view
        await self.disable_buttons(interaction)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send('See you there!', ephemeral=True)

    # SendMe
    @discord.ui.button(label='See details', style=discord.ButtonStyle.gray,custom_id='SE')
    async def sendMe_button(self,  interaction:discord.Interaction, button: discord.ui.Button):

        # send the description of the event from DM
        guild = interaction.guild
        userINTRCTN = discord.utils.get(guild.members, id=interaction.user.id)
        if userINTRCTN:
            dm_channel = await userINTRCTN.create_dm()
        title_text = self.matching_event['name']
        underline_text = '\n' + '_' * len(title_text)  # Create underlining with underscores
        e = discord.Embed(
            title=f"{title_text}{underline_text}",
            description=f"Description: {self.matching_event['description']} ",
            color=0x7289da
            )
        await dm_channel.send(embed=e)

        # Send the message with buttons and view
        await interaction.response.edit_message(view=self)
        await interaction.followup.send('Check your DM!', ephemeral=True)


