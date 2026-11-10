import discord
from discord.ext import commands
from google import genai

# Chaves
key = "nao"
token = "mandem tokens"

# Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Gemini
ia = genai.Client(api_key=key)

INSTRUCOES = """
Você é o EcoBot, um assistente de inteligência
artificial especializado em reciclagem e sustentabilidade.

Suas funções:
- Ensinar sobre reciclagem.
- Ajudar a reduzir o lixo doméstico.
- Dar dicas de reutilização.
- Explicar compostagem.
- Incentivar hábitos sustentáveis.

Responda sempre em português brasileiro.
Seja simpático, educativo e objetivo.
Não invente regras de coleta seletiva.
Responda no maximo 20 frases.
Seja direto e evite explicações desnecessariamente longas.
"""

@bot.command()
async def eco(ctx, *, pergunta: str):

    async with ctx.typing():
        try:
            resposta = await ia.aio.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=pergunta,
                config={
                    "system_instruction": INSTRUCOES,
                    "max_output_tokens": 300
                }
            )

            texto = resposta.text

            if not texto:
                await ctx.reply("Não consegui gerar uma resposta.")
                return

            for inicio in range(0, len(texto), 1900):
                await ctx.reply(texto[inicio:inicio + 1900])

        except Exception as erro:
            print(f"Erro na IA: {erro}")
            await ctx.reply(
                "Não consegui me conectar ao Gemini! Tente novamente."
            )

bot.run(token)
