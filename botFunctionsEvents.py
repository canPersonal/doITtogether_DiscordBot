import discord
import json
import botClassViewEvents as botView

async def delete_given_event(interaction: discord.Interaction, channel1, followup: discord.Message = None, eventname=str,replaceflag=0,guild=None):

    # Get existing messages in the channel
    async for message in channel1.history(limit=None):
        if 0 <len(message.embeds):
            embed = message.embeds[0]
            underline_text = '\n' + '_' * len(eventname)  # Create underlining with underscores
            title=f"{eventname}{underline_text}"
            # Check if the label in the embed matches any label in the file
            if embed.title==title:
                await message.delete()

        else:
            await message.delete()

    if replaceflag==1:
        # Open the data
        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            matching_event = -1

        matching_event=events_data[-1]
        print(f"matching_event['name']")
        view2 = botView.initialized_event(guild,matching_event)   
        title_text = matching_event['name']
        underline_text = '\n' + '_' * len(title_text)  # Create underlining with underscores
        e = discord.Embed(
            title=f"{title_text}{underline_text}",
            description=f"Duration: {matching_event['duration']} Hours",
            color=0x7289da
            )
        await channel1.send(embed=e,view=view2)


        author = discord.utils.get(guild.members, id=int(matching_event['author']))
        if author:
            dm_channel = await author.create_dm()
        view2 = botView.joined_event(guild,matching_event)
        title_text = matching_event['name']
        underline_text = '\n' + '_' * len(title_text)  # Create underlining with underscores
        e = discord.Embed(
            title=f"Event Name: {title_text}{underline_text}",
            description='Somebody Joined the Party! Next Stage:',
            color=0x7289da
            )
        await dm_channel.send(embed=e, view=view2)


        channel_name = eventname
        new_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)

        if new_channel:
        # New name for the channel
            new_channel_name = matching_event['name']
    
            # Editing the channel's name
            await new_channel.edit(name=new_channel_name)
            print(f"Changed text channel name to: {new_channel_name}")
        else:
            print("Text channel not found.")







def dataset_refresh(updateFlag,new_data,dateUSERID=0,timeUSER=0):
    # Open the data
    try:
        with open('events.json', 'r') as file:
            events_data = json.load(file)
    except FileNotFoundError:
        matching_event = -1


    # update because somebody joined the event
    if updateFlag  == 1:
        
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == new_data), None)
        matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == new_data), None)
        if not matching_event:
            matching_event=0
        is_participant = str(dateUSERID) in matching_event.get('participant_ids', [])
        if not is_participant
            removed_event = events_data.pop(matching_index)
            matching_event['num_participants'] += 1
            matching_event['participant_names'].append(str(timeUSER))
            matching_event['participant_ids'].append(str(dateUSERID))
            events_data.append(matching_event)
        else
            matching_event=-5
        
    elif updateFlag  == 2:
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == new_data['name']), None)
        matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == new_data['name']), None)
        if not matching_event:
            matching_event=0
        else:
            if str(new_data['interactionUserID']) not in matching_event['author']:
                matching_event=1
            else:
                removed_event = events_data.pop(matching_index)
                # Update the date and time of the matching event
                matching_event['date'] = f'{dateUSERID}'
                matching_event['time'] = f'{timeUSER}'
                matching_event['stage_event'] = 3
                # Append the new event to the list
                events_data.append(matching_event)
        
    elif updateFlag  == 3:
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == new_data['old_name']), None)
        matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == new_data['old_name']), None)
        if not matching_event:
            matching_event=0
        else:
            if str(new_data['interactionUserID']) not in matching_event['author']:
                matching_event=1
            else:
                removed_event = events_data.pop(matching_index)
                matching_event['name'] = new_data ['name']
                matching_event['duration'] = new_data ['duration']
                matching_event['description'] = new_data ['description']
                matching_event['emailAu'] = new_data ['emailAu']
                matching_event['stage_event'] = 3
                # Append the new event to the list
                events_data.append(matching_event)
        
    elif updateFlag  == 4:
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == new_data['name']), None)
        matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == new_data['name']), None)
        if not matching_event:
            matching_event=0
        else:
            if str(new_data['interactionUserID']) not in matching_event['author']:
                matching_event=1
            else:
                removed_event = events_data.pop(matching_index)
                
    elif updateFlag  == 5:
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == new_data['name']), None)
        matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == new_data['name']), None)
        if not matching_event:
            matching_event=0
        else:
            removed_event = events_data.pop(matching_index)
        
    else:
        matching_event = next((event for event in events_data if 'name' in event and event['name'] == new_data), None)
        matching_index = next((idx for idx, event in enumerate(events_data) if 'name' in event and event['name'] == new_data), None)
        if not matching_event:
            # Append the new event to the list
            events_data.append(new_data)
            matching_event=new_data
        else:
            matching_event=-2



        
    # Save the updated data back to the file
    with open('events.json', 'w') as file:
        json.dump(events_data, file, indent=2)

    return matching_event


