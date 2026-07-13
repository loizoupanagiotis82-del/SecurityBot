import discord


async def can_moderate(
    interaction: discord.Interaction,
    member: discord.Member
):
    if interaction.guild is None:
        return False, "❌ This command can only be used in a server."

    moderator = interaction.user

    if not isinstance(moderator, discord.Member):
        return False, "❌ Could not verify your permissions."

    if member == moderator:
        return False, "❌ You cannot moderate yourself."

    if member == interaction.guild.owner:
        return False, "❌ You cannot moderate the server owner."

    if (
        moderator != interaction.guild.owner
        and member.top_role >= moderator.top_role
    ):
        return False, "❌ That member has an equal or higher role than you."

    bot_member = interaction.guild.me

    if bot_member is None:
        return False, "❌ Could not verify my permissions."

    if member.top_role >= bot_member.top_role:
        return (
            False,
            "❌ My role must be above that member."
        )

    return True, None
