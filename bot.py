def run_discord_bot():
    import discord
    from discord.ext import commands
    import random
    from discord import app_commands
    import traceback
    import json
    from datetime import datetime
    import uuid
    


    TOKEN = 'MTE5MzY0NzkwMTE3NjQ5NjMwMQ.Gk-6Cy.MCLpjdPjLv4rCTMil3Pj1f9O8SIWMV7FzT-Xw8'
    
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
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


    @bot.event
    async def on_ready():
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

        async def on_submit(self, interaction: discord.Interaction):
            # Create a dictionary to store event details
            event_data = {
                'event_id': str(uuid.uuid4()),  # Generate a random UUID for the event ID
                'name': self.name_Event.value,
                'description': self.description_event.value,
                'duration': self.duration_event.value,
                'author': str(interaction.user),
                'author_avatar': str(interaction.user.avatar),
                'timestamp': datetime.utcnow().isoformat(),  # Adding UTC timestamp
                'num_participants': 1,  # Starting with 1 participant (the author)
                'participant_names': [str(interaction.user)],  # Include author's name in the list
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
        
        async def button_callback(self,  interaction:discord.Interaction, button: discord.ui.Button,):

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

            # Append the new event to the list
            events_data.append(matching_event)
            

            # Save the updated data back to the file
            with open('events.json', 'w') as file:
                json.dump(events_data, file, indent=2)




                await interaction.response.edit_message(view=self)
                await interaction.message.channel.send('Button clicked! Event data updated.!')
                return
            
            await interaction.message.channel.send('No matching event data found.!') 
            
 

    @bot.tree.command(name='refresh')
    async def _refresh(interaction: discord.Interaction):
        # Get the designated channel for events
        channel1 = bot.get_channel(1195073936380133486)
        if not channel1:
            return await interaction.response.send_message('Could not find the events channel.')

        # Read existing data from the file
        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            return await interaction.response.send_message('No events file found.')

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
                        await interaction.response.send_message(f'Deleted event: {title}')
            else:
                await message.delete()

        await interaction.response.send_message('Refresh complete.')




    bot.run(TOKEN)
    
