def run_discord_bot():
    import discord
    from discord.ext import commands
    import random
    from discord import app_commands
    import traceback
    import json
    from datetime import datetime
    import uuid
    from discord.ui import Button, View
    from discord import ButtonStyle
    import webPageFunctions

    print(discord.__version__)
    


    TOKEN = 'MTE5MzY0NzkwMTE3NjQ5NjMwMQ.Gk-6Cy.MCLpjdPjLv4rCTMil3Pj1f9O8SIWMV7FzT-Xw8'
    
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    intents.messages = True
    description = '''An example bot to showcase the discord.ext.commands extension
    module.

    There are a number of utility commands being showcased here.'''

    bot = commands.Bot(command_prefix='?', description=description, intents=intents)


    @bot.event
    async def on_ready():
        try:
            s = await bot.tree.sync()
            print(f'Synced {len(s)} commands')
        except Exception as e:
            print(f'Error syncing commands: {e}')
    
        print(f'Logged in as {bot.user.name}')

         # Fetch the designated channel for events by name
        channel = bot.get_channel(1195073936380133486)
        if not channel:
            print('Could not find the events channel.')
            return

        # Read existing data from the file
        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            print('No events file found.')
            return

        # Get existing messages in the channel
        async for message in channel.history(limit=None):
            if message.author == bot.user and message.embeds:
                embed = message.embeds[0]

                # Check if the label in the embed matches any label in the file
                if embed.title:
                    title = embed.title
                    print(f"{title}")
                    matching_event = next((event for event in events_data if 'name' in event and event['name'] == title), None)

                    # If no matching event is found, delete the message
                    if not matching_event:
                        await message.delete()
                        print(f'Deleted event: {title}')
            else:
                await message.delete()


        print('Refresh complete.')


        
    @bot.tree.command(name='initiate')
    async def initiate(interaction: discord.Interaction):
        await interaction.response.send_modal(event())




    class event(discord.ui.Modal, title='Event'):
# 
        name_Event = discord.ui.TextInput(
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
            label='Your email for time scheduling',
            required=True,
        )

        async def on_submit(self, interaction: discord.Interaction):
            # Create a dictionary to store event details
            event_data = {
                'event_id': str(uuid.uuid4()),  # Generate a random UUID for the event ID
                'name': self.name_Event.value,
                'description': self.description_event.value,
                'duration': self.duration_event.value,
                'emailAu': self.email_event.value,
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
                
            view = event_post()
            channel= discord.utils.get(interaction.guild.channels,name='events')
            e = discord.Embed(title=self.name_Event, description=self.duration_event)
            e.set_author(name=interaction.user,icon_url=interaction.user.avatar)
            await channel.send(embed=e,view=view)
            await interaction.response.send_message(f'Got it!', ephemeral=True)

             
        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

            # Make sure we know what the error actually is
            traceback.print_exception(type(error), error, error.__traceback__)


            
    

    # Define a simple View that gives us a confirmation menu
    class event_post(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None


        
            
        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='IamIN!', style=discord.ButtonStyle.green,custom_id='IN')
        
        async def button_callback(self,  interaction:discord.Interaction, button: discord.ui.Button):

            #button.disabled=True
            # Read existing data from the file
            try:
                with open('events.json', 'r') as file:
                    events_data = json.load(file)
            except FileNotFoundError:
                return await interaction.message.channel.send('No events file found.')

            interaction_embed_title = interaction.message.embeds[0].title
            matching_event = next((event for event in events_data if 'name' in event and event['name'] == interaction_embed_title), None)
            matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == interaction_embed_title), None)
            removed_event = events_data.pop(matching_index)
            matching_event['num_participants'] += 1
            matching_event['participant_names'].append(str(interaction.user))
            matching_event['participant_ids'].append(str(interaction.user.id))

            # Append the new event to the list
            events_data.append(matching_event)
            

            # Save the updated data back to the file
            with open('events.json', 'w') as file:
                json.dump(events_data, file, indent=2)


            # Check if the number of participants is greater than one
            if matching_event['num_participants'] > 1:
                # Create a new text channel
                guild = interaction.guild
                channel_name = f"{matching_event['name']}"
                new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)

            if not new_channel:
                new_channel = await guild.create_text_channel(channel_name)

            # Grant read permissions to participants
            for participant_name in matching_event['participant_names']:
                participant = discord.utils.get(guild.members, name=participant_name)
                if participant:
                    await new_channel.set_permissions(participant, read_messages=True)

            # Set read permissions for @everyone to False
                await new_channel.set_permissions(guild.default_role, read_messages=False)

            # Send a direct message to the author with buttons
            author = discord.utils.get(guild.members, id=int(matching_event['author']))
            if author:
                dm_channel = await author.create_dm()



            view2 = NextStage1(guild,matching_event)
            e = discord.Embed(title=matching_event['name'], description='Even Created! Next Stage:')


            # Send the message with buttons and view
            await dm_channel.send(embed=e, view=view2)

            await interaction.response.edit_message(view=self)
            await interaction.message.channel.send('Button clicked! Event data updated.!')

    class NextStage1(discord.ui.View):
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

                    

        @discord.ui.button(style=discord.ButtonStyle.green, custom_id='set_time', label='Set Time')
        async def set_time_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.value = 1
            await interaction.response.send_message('Set Time button clicked!')
            [public_link, admin_link]=webPageFunctions.create_poll(self.matching_event)
        
            # Disable the buttons and update the message
            await self.disable_buttons()

            # Send the public link to all participants
            for participant_name in self.matching_event['participant_ids']:
                user = discord.utils.get(self.guild.members, id=int(participant_name))
                if user:
                    await user.send(f"Public Link for the poll: {public_link}")

            # Send the admin link to the author of the message
            author = discord.utils.get(self.guild.members, id=int(self.matching_event['author']))
            if author:
                await author.send(f"Admin Link for the poll: {admin_link}")

            await interaction.message.edit(view=self)




        @discord.ui.button(style=discord.ButtonStyle.gray, custom_id='edit', label='Edit')
        async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.value = 1
            await interaction.response.send_modal(edt_event())

            # Disable the buttons and update the message
            await self.disable_buttons()
            await interaction.message.edit(view=self)


        @discord.ui.button(style=discord.ButtonStyle.red, custom_id='cancel', label='Cancel')
        async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.value = 1
            await interaction.response.send_message('Please confirm the name of the event you want to cancel.')
            # Wait for user input
            try:
                user_input = await bot.wait_for('message', check=lambda m: m.author.id == interaction.user.id, timeout=60)
                self.event_name = user_input.content.strip()
            except asyncio.TimeoutError:
                await interaction.followup.send('No response received. Cancel operation aborted.')
                return

            # Add your cancellation logic directly here
            # For example, you can use the event_name to perform the cancellation
            try:
                with open('events.json', 'r') as file:
                    events_data = json.load(file)
            except FileNotFoundError:
                return await interaction.followup.send('No events file found.')

            matching_event = next((event for event in events_data if 'name' in event and event['name'] == self.event_name), None)
            matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == self.event_name), None)

            if matching_event:
                removed_event = events_data.pop(matching_index)

                # Save the updated data back to the file
                with open('events.json', 'w') as file:
                    json.dump(events_data, file, indent=2)

                await interaction.followup.send(f'Event "{self.event_name}" has been canceled.')

            await refresh_events(interaction, followup=interaction.followup)


            # Disable the buttons and update the message
            await self.disable_buttons()
            await interaction.message.edit(view=self)
        
    @bot.tree.command(name='refresh')
    async def _refresh(interaction: discord.Interaction):
        await refresh_events(interaction)


    async def refresh_events(interaction: discord.Interaction, followup: discord.Message = None):
        # Get the designated channel for events
        channel1 = bot.get_channel(1195073936380133486)

        if followup:
            await interaction.followup.send('Starting')
        else:
            await interaction.response.send_message('Starting')

        if not channel1:
            if followup:
                return await interaction.followup.send('Could not find the events channel.')
            else:
                return await interaction.followup.send('Could not find the events channel.')

        # Read existing data from the file
        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            if followup:
                return await interaction.followup.send('No events file found.')
            else:
                return await interaction.followup.send('No events file found.')

        # Get existing messages in the channel
        async for message in channel1.history(limit=None):
            if message.author == bot.user and message.embeds:
                embed = message.embeds[0]

                # Check if the label in the embed matches any label in the file
                if embed.title:
                    title = embed.title
                    print(f"{title}")
                    matching_event = next((event for event in events_data if 'name' in event and event['name'] == title), None)

                    # If no matching event is found, delete the message
                    if not matching_event:
                        await message.delete()
                        if followup:
                            await interaction.followup.send(f'Deleted event: {title}')
                        else:
                            await interaction.followup.send(f'Deleted event: {title}')
            else:
                await message.delete()

        if followup:
            await interaction.followup.send('Refresh complete.')
        else:
            await interaction.followup.send('Refresh complete.')



    @bot.tree.command(name='delete_event')
    async def delete_event(interaction: discord.Interaction):
        try:
            # Read existing events from the file
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            return await interaction.response.send_message('No events file found.')

        # Extract event names from the data
        event_names = [event['name'] for event in events_data]

        # Respond with the list of event names
        await interaction.response.send_message(f'Events available for deletion: {", ".join(event_names)}\n\nPlease enter the name of the event you want to delete.', ephemeral=True)

        # Wait for user input
        try:
            response = await bot.wait_for(
                'message',
                check=lambda msg: msg.author == interaction.user and msg.channel == interaction.channel,
                timeout=60.0  # Adjust the timeout as needed
            )
        except asyncio.TimeoutError:
            return await interaction.followup.send('Timed out. Deletion canceled.', ephemeral=True)

        # Find the matching event in the data
        event_name_to_delete = response.content
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == event_name_to_delete), None)

        if matching_event:
            # Remove the matching event from the data
            events_data.remove(matching_event)

            # Save the updated data back to the file
            with open('events.json', 'w') as file:
                json.dump(events_data, file, indent=2)

            await interaction.followup.send(f'Event "{event_name_to_delete}" deleted successfully!', ephemeral=True)
        else:
            await interaction.followup.send(f'No matching event found with the name "{event_name_to_delete}". Deletion canceled.', ephemeral=True)


    class edt_event(discord.ui.Modal, title='Event'):

        old_name_Event = discord.ui.TextInput(
            label='Old Event Name',
            required=True,
        )
# 
        name_Event = discord.ui.TextInput(
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
            label='Your email for time scheduling',
            required=True,
        )

        async def on_submit(self, interaction: discord.Interaction):
            # Load existing events from the file
            try:
                with open('events.json', 'r') as file:
                    events_data = json.load(file)
            except FileNotFoundError:
                events_data = []

            old_event_name = self.old_name_Event.value
            events_data = [event for event in events_data if event.get('name') != old_event_name]
            
            # Create a dictionary to store event details
            new_event_data = {
                'event_id': str(uuid.uuid4()),  # Generate a random UUID for the event ID
                'name': self.name_Event.value,
                'description': self.description_event.value,
                'duration': self.duration_event.value,
                'emailAu': self.email_event.value,
                'author': str(interaction.user.id),
                'author_avatar': str(interaction.user.avatar),
                'timestamp': datetime.utcnow().isoformat(),  # Adding UTC timestamp
                'num_participants': 1,  # Starting with 1 participant (the author)
                'participant_names': [str(interaction.user)],  # Include author's name in the list
                'participant_ids': [str(interaction.user.id)],  # Include author's name in the list
            }



            # Append the new event to the list
            events_data.append(new_event_data)

            # Save the updated list to the JSON file
            with open('events.json', 'w') as file:
                json.dump(events_data, file, indent=2)
                

            await interaction.response.send_message(f'Got it!', ephemeral=True)

    @bot.tree.command(name='date_time')
    async def date_time(interaction: discord.Interaction):
        await interaction.response.send_modal(setTIME())





    class setTIME(discord.ui.Modal, title='Event'):

        name_Event = discord.ui.TextInput(
            label='Event Name',
            required=True,
        )

        dateUS = discord.ui.TextInput(
            label='date',
            required=True,
        )
# 
        timeUS = discord.ui.TextInput(
            label='Time',
            required=True,
        )

   

        async def on_submit(self, interaction: discord.Interaction):
            # Load existing events from the file
            try:
                with open('events.json', 'r') as file:
                    events_data = json.load(file)
            except FileNotFoundError:
                events_data = []

            name_event = self.name_Event.value
            dateUS = self.dateUS.value
            timeUS = self.timeUS.value
            await interaction.response.send_message(f'Got it!', ephemeral=True)

      
            matching_event = next((event for event in events_data if 'name' in event and event['name'] == name_event), None)
            matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == name_event), None)

            
            if not matching_event:
                return await interaction.followup.send(f"No event found with the name '{name_event}'.")

            if str(interaction.user.id) not in matching_event['author']:
                return await interaction.followup.send("You do not have permission to use this command.")


            removed_event = events_data.pop(matching_index)


            # Update the date and time of the matching event
            matching_event['date'] = f'{dateUS}'
            matching_event['time'] = f'{timeUS}'


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

    # Define a simple View that gives us a confirmation menu
    class event_post2(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None


        
            
        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Join!', style=discord.ButtonStyle.green,custom_id='IN')
        
        async def button_callback(self,  interaction:discord.Interaction, button: discord.ui.Button):

            button.disabled=True
            # Read existing data from the file
            try:
                with open('events.json', 'r') as file:
                    events_data = json.load(file)
            except FileNotFoundError:
                return await interaction.message.channel.send('No events file found.')

            interaction_embed_title = interaction.message.embeds[0].title
            matching_event = next((event for event in events_data if 'name' in event and event['name'] == interaction_embed_title), None)
            matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == interaction_embed_title), None)
            removed_event = events_data.pop(matching_index)
            matching_event['num_participants'] += 1
            matching_event['participant_names'].append(str(interaction.user))
            matching_event['participant_ids'].append(str(interaction.user.id))

            # Append the new event to the list
            events_data.append(matching_event)
            

            # Save the updated data back to the file
            with open('events.json', 'w') as file:
                json.dump(events_data, file, indent=2)


            # Check if the number of participants is greater than one
            if matching_event['num_participants'] > 1:
                # Create a new text channel
                guild = interaction.guild
                channel_name = f"{matching_event['name']}"
                new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)

            if not new_channel:
                new_channel = await guild.create_text_channel(channel_name)

            # Grant read permissions to participants
            for participant_name in matching_event['participant_names']:
                participant = discord.utils.get(guild.members, name=participant_name)
                if participant:
                    await new_channel.set_permissions(participant, read_messages=True)

            # Set read permissions for @everyone to False
                await new_channel.set_permissions(guild.default_role, read_messages=False)

           
            await interaction.response.edit_message(view=self)
            await interaction.message.channel.send('Button clicked! Event data updated.!')

           

            



    bot.run(TOKEN)
    
