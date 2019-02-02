import webcolors
class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    #borrowed from:
    #https://stackoverflow.com/questions/1859959/python-static-methods-how-to-call-a-method-from-another-method
    @staticmethod
    def __closest_color(requested_colour):
        min_colors = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]
    @staticmethod
    def get_color_name(requested_colour):
        try:
            closest_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = Color.__closest_color(requested_colour)
        return closest_name



    def __str__(self):
        return Color.get_color_name([self.r,self.g,self.b])