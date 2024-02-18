def run_discord_bot():

    # libraries
    import botClassModalsEvents as botMod
    import botClassViewEvents as botView
    import botFunctionsEvents as botFunc
    import discord
    from discord.ext import commands
    import json
    import asyncio

    # basic discord amenities
    print(discord.__version__)
    with open('token.json', 'r') as file:
            TOKENL = json.load(file)
    TOKENl=TOKENL[0]
    TOKEN=TOKENl['token']
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    intents.messages = True
    
    # command sign: - 
    bot = commands.Bot(command_prefix='-', intents=intents, help_command=None)

    
    # help command
    @bot.tree.command(name='help',description='Basics')
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message('Use the /initiate command to share your interest. You can use /delete_event command to delete shared interests and events.', ephemeral=True)

    # on ready
    @bot.event
    async def on_ready():
        try:
            s = await bot.tree.sync()
            print(f'Synced {len(s)} commands')
        except Exception as e:
            print(f'Error syncing commands: {e}')
    
        print(f'Logged in as {bot.user.name}')


    # initiate command  
    @bot.tree.command(name='initiate',description='Share your interest')
    async def initiate(interaction: discord.Interaction):
        await interaction.response.send_modal(botMod.event_intiate())

    # date and time command
    @bot.tree.command(name='date_time',description='Schedule the time for an event')
    async def date_time(interaction: discord.Interaction):
        await interaction.response.send_modal(botMod.setTime())


    # delete event command
    @bot.tree.command(name='delete_event',description='Delete event/interest')
    async def delete_event(interaction: discord.Interaction):
        try:
            # Read existing events from the file
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            return await interaction.response.send_message('No events file found.', ephemeral=True)

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
            return await interaction.followup.send('Timed out.', ephemeral=True)

        # event of interest
        event_name_to_delete = response.content
        
        # all events or specific
        string2= 'all'
        string1= str(event_name_to_delete)
        allevents = string1.casefold() == string2.casefold()

        # all events has to be me
        if allevents:
            if 227169936735207425 ==interaction.user.id:
                guild = interaction.guild
                # delete all with a loop
                for event in events_data:
                    event_name_to_delete2=event['name']
                    new_data = {
                        'name':event_name_to_delete2,
                        'interactionUserID':interaction.user.id
                    }
                    new_data=botFunc.dataset_refresh(updateFlag=5,new_data=new_data)
                    
                    # delete all the channels
                    channel_name = event_name_to_delete2
                    new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)
                    if  new_channel:
                        await new_channel.delete()

                # delete all messages
                channel= discord.utils.get(guild.channels,name='eventhorizon')
                # Get existing messages in the channel
                async for message in channel.history(limit=None):
                    await message.delete()
                await interaction.followup.send('ALL GONE', ephemeral=True)
                
            # not me
            else:
                return await interaction.followup.send("You do not have permission to use this feature.", ephemeral=True)

        # specific event 
        else:
            # Delete event
            new_data = {
                'name':event_name_to_delete,
                'interactionUserID':interaction.user.id
                }
            new_data=botFunc.dataset_refresh(updateFlag=4,new_data=new_data)

            # check for errors
            if new_data==0:
                return await interaction.followup.send(f"No event found with the name '{event_name_to_delete}'.", ephemeral=True)
            if new_data==1:
                return await interaction.followup.send("You are not the one that initiated the event.", ephemeral=True)

            # delete message
            guild = interaction.guild
            channel= discord.utils.get(guild.channels,name='eventhorizon')
            await botFunc.delete_given_event(discord.Interaction,channel1=channel, followup= interaction.followup, eventname=event_name_to_delete)
            
            # delete text channel
            channel_name = event_name_to_delete
            new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)
            if  new_channel:
                await new_channel.delete()

            await interaction.followup.send(f"Event '{event_name_to_delete}' has been deleted.", ephemeral=True)
        


    bot.run(TOKEN)
    
