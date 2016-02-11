

class BaseApp():
    def __init__(self):
        self.wnd = None
        self.x = 0
        self.y = 0
        self.width = 1
        self.height = 1

        
    def set_wnd(self, wnd):
        self.wnd = wnd

        
    def set_x(self, x):
        self.x = x

        
    def set_y(self, y):
        self.y = y

        
    def set_width(self, width):
        self.width = width

        
    def set_height(self, height):
        self.height = height
