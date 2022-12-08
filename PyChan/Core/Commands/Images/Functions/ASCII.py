import nextcord
from nextcord.ext import commands
from io import BytesIO
from tempfile import NamedTemporaryFile 
import requests
from PIL import Image
from math import sqrt


# String containing ASCII characters, ordered by their area
ascii_characters_list = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'`. "


def downsize(image):

    # Downscale image to a workable size for Discord (2000 characters total)
    width, height = image.size
    area = width * height

    area_max = 2000

    if area >= area_max:
        factor = int(sqrt(area/(area_max)))
        width = width/factor
        height = height/factor
        area = width * height

    # Adjustment for font's proportions
    height /= 2

    image = image.resize((round(width), round(height)))
    return image


def pixel_to_char(pixel):
    # Assaign each pixel a char from ascii_character_list based on it's brightness
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    pixel_brightness = r + g + b
    max_brightness = 255 * 3
    brightness_weight = len(ascii_characters_list) / max_brightness
    index = int(pixel_brightness * brightness_weight) - 1
    return ascii_characters_list[index]


def img_to_ascii(image):
    # Create string containing image in ASCII Art form 
    width, height = image.size
    ascii_img = []
    for i in range(0, height - 1):
        line = ''
        for j in range(0, width - 1):
            pixel = image.getpixel((j, i))
            line = line + pixel_to_char(pixel)
        ascii_img.append(line)
    return ascii_img


class ASCII(commands.Cog):
    """
    Class contains ASCII methods
    """

    def __init__(self, bot):
        """
        Constructor method
        """
        self.bot = bot
    
    @commands.command(
        pass_context=True, 
        name='ASCII', 
        category='Obraz',
        usage = "",
        help = """
               Konwertuje podany obraz na styl ASCII Art. Przyjmowane są tylko pliki .jpg i .png
               """
    )
    

    async def ASCII(self, ctx):
        if len(ctx.message.attachments) != 0:
            if ctx.message.attachments[0].filename.lower().endswith((".png", ".jpg")):
                await ctx.send("Proszę czekać, konwertowanie na ASCII")
                
                image_url = ctx.message.attachments[0].url
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                image = downsize(image)
                
                ascii_image = img_to_ascii(image)

                # Saving ASCII art to .txt file. Number of characters is technically unlimited, 
                # practical limit of 1025 characters per line for Windows Notepad

                # file = NamedTemporaryFile(mode="r+")
                # for line in ascii_image:
                #     print(line)
                #     file.write(line)

                # await ctx.send(file=nextcord.File(file.file, "ASCII_ART.txt", force_close=True))

                # Sending ASCII art in regular message in codeblock, number of characters is limited to 2000
                ascii_send = "```"
                for line in ascii_image:
                    ascii_send = ascii_send + line + '\n'
                ascii_send = ascii_send + "```"
                print(len(ascii_send))
                await ctx.send(ascii_send)
            else:
                await ctx.send("Błędny format pliku")
        else:
            await ctx.send("Brak załącznika")
