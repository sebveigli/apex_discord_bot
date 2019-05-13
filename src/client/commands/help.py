VALID_COMMANDS = ["help", "h", "?", "halp", "how", "commands"]

class Help():
    @staticmethod
    def match(token):
        return token.lower() in VALID_COMMANDS
    
    @staticmethod
    async def execute(message_dispatcher):
        from client.utils.discord_embed import informational_embed

        await message_dispatcher.message.channel.send(embed=informational_embed(
            description="For the latest documentation visit http://haha.gg/help"
        ))
