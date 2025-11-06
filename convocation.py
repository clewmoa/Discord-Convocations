import discord
from discord.ext import commands
from discord import app_commands

# ID du salon de tickets pour la convocation
TICKET_CHANNEL_ID = #ID de votre salon de tickets
CONVOCATION_CHANNEL_ID = #ID du salon de convocations

class Convocation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="convoquer", description="Convoquer un ou plusieurs membres pour un entretien.")
    @app_commands.describe(
        membre="Le premier membre à convoquer.",
        raison="La raison de la convocation.",
        membre2="Un second membre (optionnel).",
        membre3="Un troisième membre (optionnel).",
        membre4="Un quatrième membre (optionnel)."
    )
    # Vérifie si l'utilisateur a l'une des permissions de modération.
    @app_commands.default_permissions(kick_members=True, ban_members=True)      ### Permissions nécessaires pour utiliser la commande. Peut être modifié selon les besoins.
    # @app_commands.checks.has_any_role("Moderateur", "Admin") <-- Cette ligne est en commentaire car les permissions sont plus sûres
    async def convoquer(
        self,
        interaction: discord.Interaction,
        membre: discord.Member,
        raison: str,
        membre2: discord.Member = None,
        membre3: discord.Member = None,
        membre4: discord.Member = None
    ):
        
        # Création d'une liste des membres à mentionner.
        membres_a_convoquer = [membre]
        if membre2:
            membres_a_convoquer.append(membre2)
        if membre3:
            membres_a_convoquer.append(membre3)
        if membre4:
            membres_a_convoquer.append(membre4)

        # Construction de la chaîne de caractères pour les mentions.
        mentions = " ".join([m.mention for m in membres_a_convoquer])

        # Création du message d'embed.
        embed = discord.Embed(
            title="Convocation",
            description=(
                f"{mentions}, vous avez été convoqué(s) par {interaction.user.mention} pour la raison suivante : **{raison}**.\n\n"
                f"Merci d'ouvrir un ticket dans <#{TICKET_CHANNEL_ID}>."
            ),
            color=discord.Color.red()
        )
        
        dm_embed = discord.Embed(
            title="Convocation",
            description=(
                f"{interaction.user.mention} vous a convoqué pour la raison suivante : **{raison}**.\n\n"
                f"Merci d'ouvrir un ticket dans <#{TICKET_CHANNEL_ID}>."
            ),
            color=discord.Color.blue()
        )
        try:
            await membre.send(embed=dm_embed)
        except discord.Forbidden:
            # Si le membre a désactivé les MPs, le bot en informe l'utilisateur.
            await interaction.response.send_message(f"Impossible d'envoyer un message privé à {membre.mention}. Il a probablement désactivé les MPs.", ephemeral=True)
            return
        
        # 3. Répond à l'interaction pour confirmer que le message a été envoyé.
        await interaction.response.send_message("Demande envoyée !", ephemeral=True)

        # Récupère le salon de convocation
        convocation_channel = self.bot.get_channel(CONVOCATION_CHANNEL_ID)

        # Vérifie si le salon existe avant d'envoyer le message
        if convocation_channel:
            # Envoie l'embed dans le salon de convocation
            await convocation_channel.send(embed=embed)
            # Répond à l'interaction pour confirmer l'envoi
            await interaction.response.send_message("La convocation a été envoyée avec succès !", ephemeral=True)
        else:
            # Gère le cas où le salon de convocation n'est pas trouvé
            await interaction.response.send_message("Le salon de convocation est introuvable. Veuillez vérifier l'ID.", ephemeral=True)


# La fonction setup est nécessaire pour que la cog soit chargée par le bot.
async def setup(bot):
    await bot.add_cog(Convocation(bot))