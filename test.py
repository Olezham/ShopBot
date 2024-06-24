import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO
import cv2
import numpy as np

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command(name='feed')
async def feed(ctx, stars: int):
    if 1 <= stars <= 5:
        # Get the author's avatar
        avatar_url = ctx.author.avatar.url
        response = requests.get(avatar_url)
        avatar_img = Image.open(BytesIO(response.content)).convert("RGBA")
        
        # Open the template image with OpenCV
        template_path = "ShopBot/1233.png"
        template_img = cv2.imread(template_path)
        
        # Convert the template to HSV color space
        hsv = cv2.cvtColor(template_img, cv2.COLOR_BGR2HSV)
        
        # Define the range for green color in HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        
        # Create a mask for the green areas
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour, which should be the green circle
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Find the minimum enclosing circle
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            
            # Convert to integer for use in PIL
            circle_center = (int(x), int(y))
            circle_radius = int(radius)
            
            print(f"Center: {circle_center}, Radius: {circle_radius}")
            
            # Open the template image with PIL
            template_img_pil = Image.open(template_path).convert("RGBA")
            
            # Resize avatar to fit the circle
            avatar_img = avatar_img.resize((circle_radius*3, circle_radius*3), Image.LANCZOS)
            
            # Create a circular mask
            mask = Image.new('L', (circle_radius*2, circle_radius*2), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, circle_radius*2, circle_radius*2), fill=255)

            # Apply the mask to make the avatar circular
            avatar_img = ImageOps.fit(avatar_img, (circle_radius*2, circle_radius*2), method=Image.LANCZOS, bleed=0.0, centering=(0.5, 0.5))
            avatar_img.putalpha(mask)
            
            # Paste the circular avatar on the template
            # Calculate top-left corner of where to paste the avatar
            top_left_x = circle_center[0] - circle_radius
            top_left_y = circle_center[1] - circle_radius
            template_img_pil.paste(avatar_img, (top_left_x, top_left_y), avatar_img)
            
            # Add the stars to the template
            draw = ImageDraw.Draw(template_img_pil)
            star = "★"
            stars_text = star * stars
            # Place stars text at an appropriate location (adjust as needed)
            #draw.text((circle_center[0] + circle_radius + 10, circle_center[1] - 20), stars_text, fill="white")
            
            # Save or send the image
            with BytesIO() as image_binary:
                template_img_pil.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='result.png'))
        else:
            await ctx.send("Green circle not found in the template.")
    else:
        await ctx.send("Please provide a star rating between 1 and 5.")



bot.run('')
#        template_img = Image.open("ShopBot/1233.png").convert("RGBA")
