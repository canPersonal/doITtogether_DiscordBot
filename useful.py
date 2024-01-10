import discord
from discord.ext import commands
import random
import responses




async def send_message(message, user_message,is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    import discord
    from discord.ext import commands
    import random
    import responses
    from discord import app_commands
    import traceback

    TOKEN = 'MTE5MzY0NzkwMTE3NjQ5NjMwMQ.Gk-6Cy.MCLpjdPjLv4rCTMil3Pj1f9O8SIWMV7FzT-Xw8'
    
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    description = '''An example bot to showcase the discord.ext.commands extension
    module.

    There are a number of utility commands being showcased here.'''

    bot = commands.Bot(command_prefix='?', description=description, intents=intents)

    #TEST_GUILD = discord.Object(0)
    




    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')

    
    @bot.tree.command(name='ping',description='asjkasbd')
    async def ping(interaction: discord.Interaction):
        bot_latency=round(bot.latency*1000)
    # Send the modal with an instance of our `Feedback` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
        await interaction.response.send_message(f'Logged in as {bot_latency} (ID: {bot.user.id})')

            


    @bot.command()
    async def add(ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

    


    # Define a simple View that gives us a confirmation menu
    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Confirming', ephemeral=True)
            self.value = True
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Cancelling', ephemeral=True)
            self.value = False
            self.stop()




    @bot.command()
    async def ask(ctx: commands.Context):
        """Asks the user a question to confirm something."""
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await ctx.send('Do you want to continue?', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            print('Timed out...')
        elif view.value:
            print('Confirmed...')
        else:
            print('Cancelled...')

    class Feedback(discord.ui.Modal, title='Feedback'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
        name = discord.ui.TextInput(
            label='Name',
            placeholder='Your name here...',
        )

        # This is a longer, paragraph style input, where user can submit feedback
        # Unlike the name, it is not required. If filled out, however, it will
        # only accept a maximum of 300 characters, as denoted by the
        # `max_length=300` kwarg.
        feedback = discord.ui.TextInput(
            label='What do you think of this new feature?',
            style=discord.TextStyle.long,
            placeholder='Type your feedback here...',
            required=False,
            max_length=300,
        )

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

            # Make sure we know what the error actually is
            traceback.print_exception(type(error), error, error.__traceback__)

    #@bot.tree.command(name='feedback',guild=TEST_GUILD, description='Submit feedback')
    #async def feedback(interaction: discord.Interaction):
    ## Send the modal with an instance of our `Feedback` class
    ## Since modals require an interaction, they cannot be done as a response to a text command.
    ## They can only be done as a response to either an application command or a button press.
    #    await interaction.response.send_modal(Feedback())







    bot.run(TOKEN)
    
