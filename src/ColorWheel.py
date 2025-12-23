import matplotlib.colors as mc
import colorsys
import matplotlib.pyplot as plt        
import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap

class _colorwheeldotdict(dict):
    """dot.notation access to dictionary attributes"""
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    colors_used = []
    
    def __getattr__(self, key):
        if key not in self.keys():
            raise ValueError(f"No such color or method \"{key}\"")
        else:
            if key not in self.colors_used: self.colors_used.append(key)
            return self[f"{key}"]
    
class ColorWheel(_colorwheeldotdict):
    """
    ColorWheel object to store common colors used by the CashabackLab
    Can Access colors as a dictionary key or as a class attribute
    """
    def __init__(self):
        """
        Only define colors with Hex codes here.
        For any attributes that are not hex code colors, create a function with the @property decorator
        For Examples see color_list and legacy_list
        """
        self.dark_grey       = "#727273"
        self.light_grey      = "#B2B1B3"
        self.plum_blue       = '#881BE0'
        self.orange_creamsicle = '#FFA66B'
        self.dark_red = "#C70808"
        self.dark_blue = "#23537F"
        self.light_blue = "#0BB8FD"
        self.light_orange = "#FD8B0B"
        self.pink = "#E35D72"
        self.dark_grey = "#727273"
        self.grey = "#919192"
        self.light_grey = "#B2B1B3"
        self.purple = "#984FDE"
        self.green = '#33cc33'
        self.hc_dark_blue = "#4f7598" 
        self.black  = "#000000"
        self.white  = "#FFFFFF"
        self.orange = '#E89D07'
        self.faded_orange = '#FFC859'
        self.burnt_orange = '#F76700'
        self.blue = '#4169E1'
        self.plum = '#881BE0'
        self.sunburst_orange = "#F76700"
        self.burnt_orange = "#CC5500"
        self.yellow = "#FFD966"
        
        self.teal = '#4d9387'
        self.autumn = '#dd521b'
        self.spearmint = "#45B08C"
        self.mint      = "#AAF0D1"
        self.dark_blue2  = "#016b93"

        self.dark_brown  = "#854600"
        self.brown        = "#9e5300"
        self.light_brown = "#c86a00"

        self.bubblegum = "#FFC1CC"
        self.red = "#f63333"
        self.chartreuse = "#7fff00"
        self.light_green = "#00ff00"
        
        self.vibrant_red = "#FA0000"
        self.jean_blue   = "#2D74B4"
        self.matcha = "#C3D4A5"

        self.lavender = "#c195eb" 
        self.dark_periwinkle = '#8375FF'
        self.periwinkle = "#CCCCFF"
        self.scarlet = "#FF2400"
        self.sunflower = "#FFDA03"
        self.wine = "#B31E6F"
        self.peach = "#EE5A5A"

        self.powder_blue = "#A6CDFD"
        #New Colors to add#################################
        
    @property
    def num_colors(self):
        return len(self.color_list)
    
    @property
    def color_list(self):
        return [x for x in self.keys() if x not in self.legacy_list]
    
    @property
    def color_list_hex(self):
        return [self[x] for x in self.keys() if x not in self.legacy_list]
        
    @property
    def random_color(self):
        return np.random.choice(list(self.values()), size = 1, replace = False)
        
    @property
    def none(self):
        return "none"
    
    @property
    def bold(self):
        return "bold"
    
    def get_random_color(self, n = 1):
        return np.random.choice(list(self.values()), size = n, replace = False)
    
    
    def in_wheel(self, inp):
        """
        Returns True if input is in the color wheel.
        """
        if inp in self.keys() or inp in self.values():
            return True
        
        return False
    
    def hex_to_rgb(self, hex_code, normalize = False):
        """
        Input: Hex String
        Output: integer RGB values
        """
        hex_code = hex_code.lstrip("#")
        RGB_vals = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        
        if normalize: 
            RGB_vals = (RGB_vals[0] / 255, RGB_vals[1] / 255, RGB_vals[2] / 255)
        
        return RGB_vals
    
    def rgb_to_hex(self, rgb):
        """
        Input: rgb tuple, ex: (.2, .8, .2) or (40, 185, 40)
        Output: Hex Representation of color
        """
        bool_test = [type(x) == int for x in rgb]
        rgb = [max(x, 0) for x in rgb]
        
        if False in bool_test:
            int_rgb = (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)
            int_rgb = [int(x) for x in int_rgb]
        else:
            int_rgb = [int(x) for x in rgb]
            
        
        return '#%02x%02x%02x' % tuple(int_rgb)
    
    def recolor_icons(self,img_path, color = "#000000"):
        new_color = color #change this to desired color
        img = Image.open(img_path)
        img = img.convert("RGBA")
        datas = img.getdata()
        new_color = self.hex_to_rgb(new_color)

        newData = []

        for i, item in enumerate(datas):
            if item[3] < 0.1:
                newData.append((255, 255, 255, 0))
            else:
                newData.append((new_color[0], new_color[1], new_color[2], 255))

        img.putdata(newData)
        return img
    
    def lighten_color(self, color, amount = 1, return_rgb = False):
        """
        Lightens the given color by multiplying (1-luminosity) by the given amount.
        Input can be matplotlib color string, hex string, or RGB tuple.
        
        amount must be between 0 and 2
        amount = 1 returns the same color
        amount > 1 returns darker shade
        amount < 1 returns lighter shade
        
        Default return is Hex Code, set return_rgb = True for rgb tuple
        
        Examples:
        >> lighten_color('g', amount = 0.3)
        >> lighten_color('#F034A3', amount = 0.6)
        >> lighten_color((.3,.55,.1), amount = 0.5)
        """

        c = colorsys.rgb_to_hls(*mc.to_rgb(color))
        rgb = colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
        
        if return_rgb:
            return rgb
        else:
            return self.rgb_to_hex(rgb)
        
    def blend_colors(self, color1, color2, ratio = .5):
        """
        Blends to given colors. Input must be hex code
        Returns blended color in hex code
        """
        colorRGBA1 = self.hex_to_rgb(color1)
        colorRGBA2 = self.hex_to_rgb(color2)
        
        amount = int(255 * ratio)
        
        red   = (colorRGBA1[0] * (255 - amount) + colorRGBA2[0] * amount) / 255
        green = (colorRGBA1[1] * (255 - amount) + colorRGBA2[1] * amount) / 255
        blue  = (colorRGBA1[2] * (255 - amount) + colorRGBA2[2] * amount) / 255
        
        return self.rgb_to_hex((int(red), int(green), int(blue)))

    def demo_colors(self, selection = "all", background = "white", no_legacy = True, fontname = "Dejavu Sans"):
        """
        Shows a plot demo for the available colors.
        set selection to 
            "all" for every color
            "selected", "selection", "used" for all colors accessed by the wheel
            list of color names or hex codes (can not mix both) for a specific selection of colors
        Change background to look at colors with different backgrounds
        set no_legacy = True to see legacy color names
        set fontname to see different fonts
        Returns axis object
        """
        if self._isnotebook:
            return self._demo_colors_notebook(background = background, selection = selection, no_legacy = no_legacy, fontname = fontname)
        else:
            return self._demo_colors_spyder(background = background, selection = selection, no_legacy = no_legacy, fontname = fontname)

    def find_contrast_color(self, og_color, n = 1, hue_weight = 1, sat_weight = 1, lum_weight = 1, avoid = [], demo = False):
        """
        Find the top n contrasting colors in the color wheel.
        Parameters:
            n: number of colors to return
            XX_weight: adjust weighting of hue (hue_weight), luminance (lum_weight), or saturation (sat_weight). 
            avoid: list of ColorWheel colors to avoid using
            demo: display contrasting colors and their names
        Returns:
            list of top n contrasting colors
        """
        curr_hls = colorsys.rgb_to_hls(*mc.to_rgb(og_color))

        contrast_array = []
        for color in self.keys():
            if color in self.legacy_list or color in ["white", "black", "dark_grey", "light_grey", "grey"] or self[color] in avoid:
                continue
            else:
                new_hls = colorsys.rgb_to_hls(*mc.to_rgb(self[color]))

                hue_diff = (abs(curr_hls[0] - new_hls[0]))*(hue_weight)
                lum_diff = (abs(curr_hls[1] - new_hls[1]))*(lum_weight)
                sat_diff = (abs(curr_hls[2] - new_hls[2]))*(sat_weight)

                contrast_ratio = (hue_diff + lum_diff + sat_diff)**.5

                contrast_array.append( [self[color], contrast_ratio] )

        contrast_array.sort(key = lambda x: -x[1])
        return_array = [contrast_array[i][0] for i in range(n)]
        
        if demo:
            x = return_array
            plt.figure(dpi = 300, figsize = (4,3))
            for i in range(len(x)):
                plt.bar(1, i+1, color = x[-(i+1)], zorder = -i, width = 1)
                plt.text(1, i+.5, self._get_name(x[-(i+1)]), ha = "center", va = "center", color = "white")
                plt.axhline(i+1, color = self.black)
            plt.bar(0, i+1, color = og_color, width = 1)
            plt.ylim(0, i+1)
            plt.xlim(-.5, 1.5)
            plt.xticks([])
            plt.yticks([])
            plt.title(f"Contrasting {self._get_name(og_color)}")
        return return_array
    
    def luminance_gradient(self, color, n = 5, allow_darker = False, demo = False):
        """
        Returns luminant gradient of given color.
        n: number of colors to generate
        allow_darker: allows gradient to go darker than the given color
        """
        if color in self.color_list:
            hex_color = self[color]
        elif type(color) == str and color[0] == "#":
            hex_color = color
        else:
            raise ValueError(f"Invalid Color Input: {color}. Input must be hex code or a color name in the color wheel.")
            
        if allow_darker:
            luminance_list = [self.lighten_color(hex_color, amount = (x+1)/int(n/2+1)) for x in range(n) ]
        else:
            luminance_list = [self.lighten_color(hex_color, amount = (x+1)/int(n+1)) for x in range(n) ]
        if demo:
            x = luminance_list
            plt.figure(dpi = 300, figsize = (3,3))
            for i in range(len(x)):
                plt.bar(1, i+1, color = x[i], zorder = -i, width = 1)
                plt.text(1, i+.5, f"{i}", ha = "center", va = "center", color = "black")
                plt.axhline(i+1, color = self.black)
            plt.ylim(0, i+1)
            plt.xlim(.5, 1.5)
            plt.xticks([])
            plt.yticks([])
            plt.title(f"Luminance Gradient for {self._get_name(hex_color)}")
            
        return luminance_list
    
    
    def _get_hsv(self, hexrgb):
        hexrgb = hexrgb[1]
        hexrgb = hexrgb.lstrip("#")   
        r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in range(0,5,2))
        return colorsys.rgb_to_hsv(r, g, b)
    