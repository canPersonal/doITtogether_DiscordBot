import discord
from discord.ext import commands
from discord import app_commands
import traceback
import json
from datetime import datetime
import uuid
from discord.ui import Button, View
from discord import ButtonStyle
import webPageFunctions
import botFunctionsEvents
import asyncio

### All Modal Classes

#1 modal for event initiation
class event_intiate(discord.ui.Modal, title='Event'):
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

    fix_datetime_checkbox = discord.ui.TextInput(
            label='Fix Date and Time?',
            placeholder='If so please write:YES',
            required=False,
        )

    email_event = discord.ui.TextInput(
        label='Your email',
        required=False,
        placeholder='user@example.com',
    )

    async def on_submit(self, interaction: discord.Interaction):
        

        # Check if the user input for email is empty
        if not self.email_event.value:
            # Assign a default value if it's empty
            var_email = "experiment.cgmd@gmail.com"
        else:
            var_email = self.email_event.value

        if not self.fix_datetime_checkbox:
            var_datetime = "No"
        else:
            var_datetime = self.fix_datetime_checkbox

        # Check if the email contains the "@" symbol
        if "@" not in var_email:
            await interaction.response.send_message("Invalid email format. Please enter a valid email address.", ephemeral=True)
            return

        
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
        }

        # Load existing events from the file
        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            events_data = []

        # Append the new event to the list
        events_data.append(event_data)

        # Save the updated list to the JSON file
        with open('events.json', 'w') as file:
            json.dump(events_data, file, indent=2)

        # Check if the user wants to fix date and time
        string2= 'yes'
        string1= str(var_datetime)
        fix_datetime = string1.casefold() == string2.casefold()

        # If fixing date and time, ask the user for date and time
        if fix_datetime:
            await interaction.response.send_message(f'Call the /date_time!', ephemeral=True)
        else:
                
            view = initialized_event()
            channel= discord.utils.get(interaction.guild.channels,name='events')
            e = discord.Embed(title=self.name_event.value, description=f'Approximate Duration: {self.duration_event.value}')
            e.set_author(name=interaction.user,icon_url=interaction.user.avatar)
        
            await channel.send(embed=e,view=view)
            
        await interaction.response.send_message(f'Got it!', ephemeral=True)
        

             
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

#2 modal for setting the time
class setTime(discord.ui.Modal, title='Event'):

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
        # Load existing events from the file
        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            events_data = []

            
        # set the values
        name_event = self.name_event.value
        dateEV = self.dateUS.value
        timeEV = self.timeUS.value
        

        # check the events
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == name_event), None)
        matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == name_event), None)

            
        if not matching_event:
            return await interaction.followup.send(f"No event found with the name '{name_event}'.")

        if str(interaction.user.id) not in matching_event['author']:
            return await interaction.followup.send("You do not have permission to use this feature.")


        removed_event = events_data.pop(matching_index)


        # Update the date and time of the matching event
        matching_event['date'] = f'{dateEV}'
        matching_event['time'] = f'{timeEV}'


        # Append the new event to the list
        events_data.append(matching_event)

        # Save the updated list to the JSON file
        with open('events.json', 'w') as file:
            json.dump(events_data, file, indent=2)

        # Get the designated channel for events
        channel1 = bot.get_channel(1195073936380133486)

        if not channel1:
            return await interaction.followup.send('Could not find the events channel.')

        # Get existing messages in the channel
        async for message in channel1.history(limit=None):
            if message.author == bot.user and message.embeds:
                embed = message.embeds[0]

                # Check if the label in the embed matches any label in the file
                if embed.title==matching_event['name']:
                    title = embed.title
                    await message.delete()
                        
        view = event_post2()
            
        e = discord.Embed(title=matching_event['name'], description=matching_event['duration'])
        e.add_field(name="date", value=f"{matching_event['date']}", inline=False)
        e.add_field(name="time", value=f"{matching_event['time']}", inline=False)
        e.set_author(name=interaction.user,icon_url=interaction.user.avatar)
        await channel1.send(embed=e,view=view)
        await interaction.response.send_message(f'Got it!', ephemeral=True)


