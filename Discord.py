import random
import discord
from discord.ext import commands
import re

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=("!", "/"), intents=intents)

# @bot.command(name='r', description="Roll a number")
# async def r(ctx, dice_notation):

#     dice_notation = str(dice_notation)

#     user = ctx.author

#     notation = [x for x in dice_notation]

#     if not notation[0].isdigit():
#         dice_notation = "1" + dice_notation
#         try:
#             num_dice, num_sides = map(int, dice_notation.split("d"))
#         except ValueError:
#             raise ValueError("Invalid dice notation: {}".format(dice_notation))
#     elif not re.search('[a-zA-Z]', dice_notation):
#         num_dice = 1
#         num_sides = int(dice_notation)
#     else:
#         try:
#             num_dice, num_sides = map(int, dice_notation.split("d"))
#         except ValueError:
#             raise ValueError("Invalid dice notation: {}".format(dice_notation))
        
#     if num_dice > 100:
#         num_dice = 100

#     rolls = [random.randint(1, num_sides) for _ in range(num_dice)]

#     sum = 0
#     for num in rolls:
#         sum += num

#     string_rolls = "[" + ", ".join(str(x) for x in rolls) + "]"

#     if user.nick:
#         nickname = user.nick
#     else:
#         nickname = user.name 
#     nickname = ctx.author.nick if ctx.author.nick else ctx.author.name

# if num_dice == 1 or num_dice == 0:
#     result = str("***"+nickname + "*** кинув `[" + str(num_sides) +"]` сторінний дайс\n\nРезультат: `" + string_rolls + "`")
# else:
#     result = str("***"+nickname + "***  кинув `["+ str(num_dice) + "]` кісток по `[" + str(num_sides) +"]` сторін\n\nРезультат: `" + string_rolls +"`\nСумма:        `["+ str(sum) + "]`")

# await ctx.message.reply(result)

# await ctx.channel.delete_messages([ctx.message])

@bot.command(name='r', description="Roll a number")
async def r(ctx, dice_notation):

    dice_notation = str(dice_notation)

    try:
        # Check if "d" is present
        if "d" in dice_notation:
            parts = dice_notation.split("d")
            # Extract number of dice (default to 1 if not present)
            num_dice = int(parts[0]) if parts[0] else 1
            # Extract number of sides
            num_sides = int(parts[1].split("+")[0])

            # Check for plus sign and extract modifier (default to 0)
            if len(parts[1].split("+")) > 1:
                modifier = int(parts[1].split("+")[1])
            else:
                modifier = 0
        else:
            # No "d" present, single number roll
            parts = dice_notation.split("+")
            num_dice = 1
            # Extract number and potential modifier (default to 0)
            num_sides = int(parts[0]) if parts[0] else 0
            if len(parts) > 1:
                modifier = int(parts[1])
            else:
                modifier = 0

        # Limit dice to 100 and sides to minimum of 1
        if num_dice > 100:
            num_dice = 100
        if num_sides < 1:
            num_sides = 1

        # rolls = [x if (x == 1 or x == num_sides) else x + modifier for x in [random.randint(1, num_sides) for _ in range(num_dice)]]
        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        sum_of_rolls = sum([x * 1.5 if x == num_sides else x for x in rolls], modifier)
        sum_of_rolls = round(sum_of_rolls) if sum_of_rolls.is_integer() else sum_of_rolls

        string_rolls = ", ".join([str(x) + ("*" if x == 1 or x == num_sides else "") for x in rolls])
        # string_rolls = string_rolls.replace("1*", "⨯").replace(f"{num_sides}*", "*")

        user = ctx.author
        nickname = ctx.author.nick if ctx.author.nick else ctx.author.name

        # Prepare result message with appropriate grammar
        dice_text = f"{num_dice}d{num_sides}" if num_dice > 1 else f"{num_sides}"
        modifier_text = f" + {modifier}" if modifier > 0 else (f" - {abs(modifier)}" if modifier < 0 else "")

        result = f"***{nickname}*** кинув `{dice_text}{modifier_text}`\n\nРезультат: `{string_rolls}`\nСумма:        `[{sum_of_rolls}]`"
        await ctx.message.reply(result)
        await ctx.channel.delete_messages([ctx.message])

    except ValueError as e:
        await ctx.message.reply(str(e))



@bot.command(name='ra', description="Roll a number")
async def ra(ctx, dice_notation):

    dice_notation = str(dice_notation)

    try:
        # Check if "d" is present
        if "d" in dice_notation:
            parts = dice_notation.split("d")
            # Extract number of dice (default to 1 if not present)
            num_dice = int(parts[0]) if parts[0] else 1
            # Extract number of sides
            num_sides = int(parts[1].split("+")[0])

            # Check for plus sign and extract modifier (default to 0)
            if len(parts[1].split("+")) > 1:
                modifier = int(parts[1].split("+")[1])
            else:
                modifier = 0
        else:
            # No "d" present, single number roll
            parts = dice_notation.split("+")
            num_dice = 1
            # Extract number and potential modifier (default to 0)
            num_sides = int(parts[0]) if parts[0] else 0
            if len(parts) > 1:
                modifier = int(parts[1])
            else:
                modifier = 0

        # Limit dice to 100 and sides to minimum of 1
        if num_dice > 100:
            num_dice = 100
        if num_sides < 1:
            num_sides = 1

        rolls = [x + modifier if (x != 1 and x != num_sides - modifier) else x for x in [random.randint(1, num_sides) for _ in range(num_dice)]]
        sum_of_rolls = sum([x * 1.5 if x == num_sides else x for x in rolls])
        sum_of_rolls = round(sum_of_rolls) if sum_of_rolls.is_integer() else sum_of_rolls

        string_rolls = ", ".join([str(x) + ("*" if x == 1 or x == num_sides else "") for x in rolls])

        user = ctx.author
        nickname = ctx.author.nick if ctx.author.nick else ctx.author.name

        # Prepare result message with appropriate grammar
        dice_text = f"{num_dice}d{num_sides}" if num_dice > 1 else f"{num_sides}"
        modifier_text = f" + {modifier}" if modifier > 0 else (f" - {abs(modifier)}" if modifier < 0 else "")

        result = f"***{nickname}*** кинув на дамаг`{dice_text}{modifier_text}`\n\nРезультат: `{string_rolls}`\nСумма:        `[{sum_of_rolls}]`"

        await ctx.message.reply(result)
        await ctx.channel.delete_messages([ctx.message])

    except ValueError as e:
        await ctx.message.reply(str(e))

@bot.command(name='slap', description="Slaps Vel's booty")
async def slap(ctx):
    result = str("Вел, вас шльопнули(Фрізеро) по дупці :3")

    await ctx.message.reply(result)

    await ctx.channel.delete_messages([ctx.message])

    # await ctx.send(rolls)

    # await ctx.message.delete()

# or:

# @commands.command()
# async def test(ctx):
#     pass

# bot.add_command(r)
with open('code.txt', 'r') as file:
    api_key = file.read().strip()
bot.run(api_key)