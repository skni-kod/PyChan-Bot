import nextcord
from nextcord.ext import commands
from io import BytesIO
from io import StringIO
import requests
from PIL import Image
from PIL import ImageOps
import numpy as np


# String containing ASCII characters, ordered by their area
ascii_characters_list = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^'`. "
ascii_characters_list_2 = "ÆÑÊŒØMÉËÈÃÂWQBÅæ#NÁþEÄÀHKRŽœXgÐêqÛŠÕÔA€ßpmãâG¶øðé8ÚÜ$ëdÙýèÓÞÖåÿÒb¥FDñáZPäšÇàhû§ÝkŸ®S9žUTe6µOyxÎ¾f4õ5ôú&aü™2ùçw©Y£0VÍL±3ÏÌóC@nöòs¢u‰½¼‡zJƒ%¤Itocîrjv1lí=ïì<>i7†[¿?×}*{+()\/»«•¬|!¡÷¦¯—^ª„”“~³º²–°­¹‹›;:’‘‚’˜ˆ¸…·¨´` "

max_width = {
    "orig": 8000000,
    "medium": 256,
    "small": 128,
    "invert": 128,
}


def downsize(image, quality, mode, invert):

    # Downscale image to the desired size
    width, height = image.size

    if width > quality:
        factor = width/quality
        width = int(width/factor)
        height = int(height/factor)

    # Changing into black and white for braille style
    if mode == "braille":
        image = image.resize((round(width), round(height)))
        image = image.convert("L")
        if invert:
            image = ImageOps.invert(image)

    # Adjustment for font's proportions
    else:
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


def img_to_ascii_braille(image):
    image_array = dithering_floyd_steinberg(image)
    row, col = image_array.shape
    result = ''
    line = ''

    for y in range(0, row - 4, 4):
        for x in range(0, col - 2, 2):
            """
            |1|4|
            |2|5|
            |3|6|
            |7|8|

            https://en.wikipedia.org/wiki/Braille_Patterns

            """

            str_tmp = str(image_array[y, x])                # 1
            str_tmp += str(image_array[y + 1, x])           # 2
            str_tmp += str(image_array[y + 2, x])           # 3
            str_tmp += str(image_array[y, x + 1])           # 4
            str_tmp += str(image_array[y + 1, x + 1])       # 5
            str_tmp += str(image_array[y + 2, x + 1])       # 6
            str_tmp += str(image_array[y + 3, x])           # 7
            str_tmp += str(image_array[y + 3, x + 1])       # 8

            str_tmp = str_tmp[::-1]
            binary_number = int(str_tmp, 2)
            hex_str = format(binary_number, 'x').upper()
            if len(hex_str) == 1:
                hex_str = '0' + hex_str
            hex_str = '28' + hex_str
            line = line + chr(int(hex_str, 16))
        result = result + line + '\n'
        line = ''

    return result


def dithering_floyd_steinberg(image):

    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering

    width, height = image.size
    image_array = np.asarray(image)
    error_array = np.zeros([height + 1, width + 1])
    result = np.zeros([height, width], dtype=int)
    error = 0
    threshold = 128
    max_value = 255

    for y in range(0, height-1):
        for x in range(0, width-1):

            if image_array[y, x] + error_array[y + 1, x + 1] < threshold:
                result[y, x] = 1        # black
                error = image_array[y, x] + error_array[y + 1, x + 1]
            else:
                result[y, x] = 0        # white
                error = image_array[y, x] + \
                    error_array[y + 1, x + 1] - max_value

            error_array[y + 1, x + 2] = error_array[y +
                                                    1, x + 2] + 7 / 16 * error
            error_array[y + 2, x] = error_array[y + 2, x] + 3 / 16 * error
            error_array[y + 2, x + 1] = error_array[y +
                                                    2, x + 1] + 5 / 16 * error
            error_array[y + 2, x + 2] = error_array[y +
                                                    2, x + 2] + 1 / 16 * error

    return result


class ASCII(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="ascii",
        category="Media",
    )
    async def ascii(self, ctx: commands.Context):
        '''Komendy związane z grafiką ASCII'''
        pass

    @ascii.command(
        pass_context=True,
        name='standard',
        usage='<grafika w formacie .jpg i .png w załączniku> <jakość>',
        help="""
               Konwertuje podany obraz na styl ASCII Art wykorzystując podstawowe znaki.
               Przyjmowane są tylko pliki .jpg lub .png

               Jakości to:
               **orig**     - oryginaly rozmiar grafiki
               **medium**   - szerokość 256 znaków
               **small**    - szerokość 128 znaków
               **liczba**   - dowolna szerokość znaków (wymagana liczba całkowita, wartość większa od oryginalnej da taki sam efekt jak **orig**)

               Parametr jakości jest opcjonalny, w przypadku niewpisania go wykorzystana zostanie wartość **small**
               """
    )
    async def standard(self, ctx, quality="small"):
        if len(ctx.message.attachments) != 0:
            if ctx.message.attachments[0].filename.lower().endswith((".png", ".jpg")):
                await ctx.send("Proszę czekać, konwertowanie na ASCII")

                if quality.isdigit():
                    await ctx.send("Szerokość " + quality)
                elif quality in max_width:
                    quality = max_width.get(quality)
                else:
                    await ctx.send("Błedny argument jakości, wykorzystanie domyślnej wartości small")
                    quality = max_width.get('small')

                image_url = ctx.message.attachments[0].url
                name_len = len(ctx.message.attachments[0].filename)
                name = ctx.message.attachments[0].filename[:name_len -
                                                           4] + "_ascii.txt"

                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))

                image = downsize(image, int(quality), 'standard', False)

                ascii_image = img_to_ascii(image)
                # Saving ASCII art to .txt file. Number of characters is technically unlimited,
                # practical limit of 1024 characters per line for Windows Notepad
                buffer = StringIO(ascii_image)
                file = nextcord.File(buffer, filename=name, force_close=True)
                await ctx.send(file=file)

            else:
                await ctx.send("Błędny format pliku")
        else:
            await ctx.send("Brak załącznika")

    @ascii.command(
        pass_context=True,
        name='braille',
        usage='<grafika w formacie .jpg i .png w załączniku> <jakość> <invert>',
        help="""
                Konwertuje podany obraz na styl ASCII Art wykorzystując znaki systemu Braille.
                Przyjmowane są tylko pliki .jpg lub .png

                Jakości to:
                **orig**     - oryginalna szerokość grafiki
                **medium**   - szerokość 256 znaków
                **small**    - szerokość 128 znaków
                **liczba**   - dowolna szerokość w znakach (wymagana liczba całkowita, wartość większa od oryginalnej da taki sam efekt jak **orig**)

                Wykorzystanie opcjonalnego parametru **invert** skutkuje odwróceniem kolorów gotowego pliku.
                W przypadku niektórych grafik może pomóc to w uzyskaniu czytelniejszego wyniku
                
                Parametr jakości jest opcjonalny, w przypadku niewpisania go wykorzystana zostanie wartość **small**
                """
    )
    async def braille(self, ctx, quality="small", invert="False"):
        if len(ctx.message.attachments) != 0:
            if ctx.message.attachments[0].filename.lower().endswith((".png", ".jpg")):
                await ctx.send("Proszę czekać, konwertowanie na ASCII")

                if invert == 'invert' or quality == 'invert':
                    invert = True
                else:
                    invert = False

                if quality.isdigit():
                    await ctx.send("Szerokość " + quality)
                elif quality in max_width:
                    quality = max_width.get(quality)
                else:
                    await ctx.send("Błedny argument jakości, wykorzystanie domyślnej wartości small")
                    quality = max_width.get('small')

                image_url = ctx.message.attachments[0].url
                name_len = len(ctx.message.attachments[0].filename)
                name = ctx.message.attachments[0].filename[:name_len -
                                                           4] + "_ascii.txt"

                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))

                image = downsize(image, int(quality), 'braille', invert)

                ascii_image = img_to_ascii_braille(image)
                buffer = StringIO(ascii_image)
                file = nextcord.File(buffer, filename=name, force_close=True)
                await ctx.send(file=file)

            else:
                await ctx.send("Błędny format pliku")
        else:
            await ctx.send("Brak załącznika")
