import discord
import json
from datetime import datetime
import uuid
from discord.ui import Button, View
from discord import ButtonStyle
import webPageFunctions
import botClassViewEvents as botView
import botFunctionsEvents as botFunc

### All Modal Classes

#1 modal for event initiation
class event_intiate(discord.ui.Modal, title='Initiate An Event!'):
    name_event = discord.ui.TextInput(
        label='Event Name',
        required=True,
    )
    
    description_event = discord.ui.TextInput(
        label='DescrIbe the event',
        style=discord.TextStyle.long,
        required=True,
        max_length=300,
    )

    duration_event = discord.ui.TextInput(
        label='ApproxImate Duration',
        required=True,    
    )

    fix_datetime_checkbox = discord.ui.TextInput(
            label='FIx Date and TIme?',
            placeholder='YES?',
            required=False,
        )

    email_event = discord.ui.TextInput(
        label='Your emaIl',
        required=False,
        placeholder='user@example.com',
    )


    async def on_submit(self, interaction: discord.Interaction):

        # Defaults
        if not self.email_event.value:
            # Assign a default value if it's empty
            var_email = "experiment.cgmd@gmail.com"
        else:
            var_email = self.email_event.value
        if not self.fix_datetime_checkbox:
            var_datetime = "No"
        else:
            var_datetime = self.fix_datetime_checkbox

        # Errors
        if "@" not in var_email:
            await interaction.response.send_message("Invalid email format. Please enter a valid email address.", ephemeral=True)
            return

        # Check if the user wants to fix date and time
        string2= 'yes'
        string1= str(var_datetime)
        fix_datetime = string1.casefold() == string2.casefold()

        # Stage of event
        stageOFevent=1

        
        # Create a dictionary to store event details
        event_data = {
            'event_id': str(uuid.uuid4()),  # Generate a random UUID for the event ID
            'name': self.name_event.value,
            'description': self.description_event.value,
            'duration': self.duration_event.value,
            'emailAu': var_email,
            'author': str(interaction.user.id),
            'author_avatar': str(interaction.user.avatar),
            'timestamp': datetime.utcnow().isoformat(),  # Adding UTC timestamp
            'num_participants': 1,  # Starting with 1 participant (the author)
            'participant_names': [str(interaction.user)],  # Include author's name in the list
            'participant_ids': [str(interaction.user.id)],  # Include author's name in the list
            'fix_datetime': fix_datetime,
            'stage_event': stageOFevent,
        }

        # dataset refresh
        new_data=botFunc.dataset_refresh(updateFlag=0,new_data=event_data)

        # check for errors
        if new_data==-2:
            return await interaction.followup.send(f"The name '{name_event}' is already taken.")
        elif new_data==-1:
            return await interaction.followup.send('Failed to find the database!')
        elif new_data==0:
            return await interaction.followup.send(f"No event found with the name '{name_event}'.")
        elif new_data==1:
            return await interaction.followup.send("You do not have permission to use this feature.")



        # If datetime, just send the buttons that will send the modal!
        # If datetime not, initialize the event post in the channel!
        guild = interaction.guild
        if fix_datetime:
            author = discord.utils.get(guild.members, id=int(new_data['author']))
            if author:
                dm_channel = await author.create_dm()
            await dm_channel.send("**NEXT STEP: Call the /date_time command to register the date and time**")

        else:
            view2 = botView.initialized_event(guild,new_data)    
            channel= discord.utils.get(guild.channels,name='events')
            title_text = self.name_event.value
            underline_text = '\n' + '_' * len(title_text)  # Create underlining with underscores

            e = discord.Embed(
                title=f"{title_text}{underline_text}",
                description=f'Duration: {self.duration_event.value} Hours',
                color=0x7289da
                )
            e.set_author(name=interaction.user,icon_url=interaction.user.avatar)
            await channel.send(embed=e,view=view2)
            
        await interaction.response.send_message(f'Got it!', ephemeral=True)
        

             
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)


#2 modal for setting the time
class setTime(discord.ui.Modal, title='Decide the TIME!'):

    name_event = discord.ui.TextInput(
        label='Event Name',
        required=True,
    )

    dateUS = discord.ui.TextInput(
        label='date',
        required=True,
        placeholder='DD.MM.YYYY',
    )

    timeUS = discord.ui.TextInput(
        label='Time',
        required=True,
        placeholder='HH.MM UTC+X',
    )


    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Got it!', ephemeral=True)
        new_data = {
        'name':self.name_event.value,
        'interactionUserID':interaction.user.id
        }
        # dataset refresh
        new_data=botFunc.dataset_refresh(updateFlag=2,new_data=new_data,dateUSERID=self.dateUS.value,timeUSER=self.timeUS.value)

        # check for errors
        if new_data==-2:
            return await interaction.followup.send(f"The name '{name_event}' is already taken.")
        elif new_data==-1:
            return await interaction.followup.send('Failed to find the database!')
        elif new_data==0:
            return await interaction.followup.send(f"No event found with the name '{name_event}'.")
        elif new_data==1:
            return await interaction.followup.send("You do not have permission to use this feature.")


        # Clear the previous message
        guild = interaction.guild
        channel= discord.utils.get(guild.channels,name='events')
        await botFunc.delete_given_event(discord.Interaction,channel1=channel, followup= interaction.followup, eventname=new_data['name'])

    
        # Post new message?
        view = botView.initialized_event2(guild,new_data)
        title_text = new_data['name']
        underline_text = '\n' + '_' * len(title_text)  # Create underlining with underscores

        e = discord.Embed(
            title=f"{title_text}{underline_text}",
            description=f"Duration: {new_data['duration']} Hours",
            color=0x7289da
            )
        e.add_field(name="date", value=f"{new_data['date']}", inline=True)
        e.add_field(name="time", value=f"{new_data['time']}", inline=True)
        e.set_author(name=interaction.user,icon_url=interaction.user.avatar)
        await channel.send(embed=e,view=view)


             
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

#3 modal for editing the event

class edit_event(discord.ui.Modal, title='Event'):

    old_name_event = discord.ui.TextInput(
        label='Old Event Name',
        required=True,
    )
# 
    name_event = discord.ui.TextInput(
        label='Event Name',
        required=True,
    )
    
    description_event = discord.ui.TextInput(
        label='Describe the event',
        style=discord.TextStyle.long,
        required=True,
        max_length=300,
    )

    duration_event = discord.ui.TextInput(
        label='Approximate Duration',
        required=True,    
    )

    email_event = discord.ui.TextInput(
        label='Your email',
        required=False,
        placeholder='user@example.com',
    )


    async def on_submit(self, interaction: discord.Interaction):
        
        
        # Defaults
        if not self.email_event.value:
            # Assign a default value if it's empty
            var_email = "experiment.cgmd@gmail.com"
        else:
            var_email = self.email_event.value


        # Errors
        if "@" not in var_email:
            await interaction.response.send_message("Invalid email format. Please enter a valid email address.", ephemeral=True)
            return
        


        
        # Create a dictionary to store event details
        event_data = {
            'event_id': str(uuid.uuid4()),  # Generate a random UUID for the event ID
            'name': self.name_event.value,
            'old_name': self.old_name_event.value,
            'description': self.description_event.value,
            'duration': self.duration_event.value,
            'emailAu': var_email,
            'author': str(interaction.user.id),
            'author_avatar': str(interaction.user.avatar),
            'timestamp': datetime.utcnow().isoformat(),  # Adding UTC timestamp
            'interactionUserID':interaction.user.id
        }
        

        # dataset refresh
        new_data=botFunc.dataset_refresh(updateFlag=3,new_data=event_data)
        
        # check for errors
        if new_data==-2:
            return await interaction.followup.send(f"The name '{name_event}' is already taken.")
        elif new_data==-1:
            return await interaction.followup.send('Failed to find the database!')
        elif new_data==0:
            return await interaction.followup.send(f"No event found with the name '{name_event}'.")
        elif new_data==1:
            return await interaction.followup.send("You do not have permission to use this feature.")

            
        await interaction.response.send_message(f'Got it!', ephemeral=True)
        

             
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)


