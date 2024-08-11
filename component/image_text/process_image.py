from PIL import Image, ImageDraw, ImageFont
import os

class ProcessImage:

    __bg_image = "src\\img\\bg.png"
    __text = None
    __text_color = 'black'
    __font = ImageFont.load_default()
    __align = 'center'
    output_folder = None

    def __init__(self, text, path):
        self.__text = text
        try:
            font = ImageFont.truetype('src\\font\\Arimo-Bold.ttf', 50)
            self.__font = font
        except IOError:
            font = ImageFont.load_default()
            self.__font = font
        
        self.output_folder = path
    

    def _calculate_text(self):
        image = Image.open(self.__bg_image)
        max_width = image.width - 150
        max_height = image.height - 20

        draw = ImageDraw.Draw(image)
        wrapped_text = self._adjust_font_size(self.__text, self.__font, max_width, max_height, draw)
        
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=self.__font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        text_x = (image.width - text_width) / 2
        text_y = (image.height - text_height) / 2

        

        draw.text((text_x, text_y), wrapped_text, font=self.__font, fill=self.__text_color, align=self.__align)

        return image
    
    def _wrap_text(self, text, font, max_width, draw):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textlength(line + words[0], font=font) < max_width:
                line = f'{line} {words.pop(0)}'.strip()
            lines.append(line)
        return "\n".join(lines)
    
    def _adjust_font_size(self, text, font, max_width, max_height, draw):

        font_size = 60

        while True:
            wrapped_text = self._wrap_text(text, font, max_width, draw)
            text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            if text_height <= max_height and text_width < max_width:
                break
            else:
                font_size -= 2
                font = ImageFont.truetype("arial.ttf", font_size) if font_size > 10 else font
                if font_size <= 10:  # Avoid making the font too small
                    break
        
        return wrapped_text
    
    def save_image(self):
        image = self._calculate_text()
        os.makedirs(os.path.dirname(self.output_folder), exist_ok=True)
        image.save(self.output_folder)
        
