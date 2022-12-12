import nextcord
from nextcord.ext import commands
from io import BytesIO
from io import StringIO
import requests
from PIL import Image


# String containing ASCII characters, ordered by their area
ascii_characters_list = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'`. "

max_width = {
    "orig": 8000000,
    "medium": 254,
    "small": 128,
}


def downsize(image, quality):

    # Downscale image to the desired size
    width, height = image.size

    if width > max_width.get(quality):
        factor = width/max_width.get(quality)
        width = int(width/factor)
        height = int(height/factor)

    # Adjustment for font's proportions
    height /= 2

    image = image.resize((round(width), round(height)))
    return image


def pixel_to_char(pixel):
    # Assaign each pixel to a char from ascii_character_list based on it's brightness
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    pixel_brightness = r + g + b
    max_brightness = 255 * 3
    brightness_weight = len(ascii_characters_list) / max_brightness
    index = int(pixel_brightness * brightness_weight) - 1
    return ascii_characters_list[index]


def img_to_ascii(image):
    # Create string containing image in ASCII Art style 
    width, height = image.size
    ascii_img = ""
    for i in range(0, height - 1):
        line = ''
        for j in range(0, width - 1):
            pixel = image.getpixel((j, i))
            line = line + pixel_to_char(pixel)
        ascii_img = ascii_img + line + '\n'
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
        usage = '<grafika w formacie .jpg i .png w załączniku> <jakość>',
        help = """
               Konwertuje podany obraz na styl ASCII Art. Przyjmowane są tylko pliki .jpg i .png
               Jakości to:
               orig - Oryginaly rozmiar grafiki (może zostać zmniejszony do 8 mb)
               medium - szerokość 256 znaków
               small - szerokość 128 znaków
               """
    )
    

    async def ASCII(self, ctx, quality="small"):
        if len(ctx.message.attachments) != 0:
            if ctx.message.attachments[0].filename.lower().endswith((".png", ".jpg")):
                await ctx.send("Proszę czekać, konwertowanie na ASCII")
                
                if quality not in max_width:
                    await ctx.send("Błedny argument jakości, wykorzystanie domyślnej wartości small")
                    quality = 'small'
                image_url = ctx.message.attachments[0].url
                name_len = len(ctx.message.attachments[0].filename)
                name = ctx.message.attachments[0].filename[:name_len - 4] + "_ascii.txt"
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                image = downsize(image,quality)
                
                ascii_image = img_to_ascii(image)

                # Saving ASCII art to .txt file. Number of characters is technically unlimited, 
                # practical limit of 1025 characters per line for Windows Notepad

                buffer = StringIO(ascii_image)
                file = nextcord.File(buffer, filename=name, force_close=True)

                await ctx.send(file=file)

            else:
                await ctx.send("Błędny format pliku")
        else:
            await ctx.send("Brak załącznika")