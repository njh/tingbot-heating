import tingbot

class touch_button(object):
    instances = []

    def __init__(self, label, xy, size=None, align='center', color='blue'):
        self.label = label
        self.xy = xy
        self.state = 'up'
        self.color = tingbot.graphics._color(color)

        if size is None:
            self.size = (75, 40)
        else:
            self.size = size

        # Register touch handler
        self.touch = tingbot.touch(xy, size, align)
        self.touch(self.my_touch)

        self.__class__.instances.append(self)

    def __call__(self, f):
        self.callback = f
        return f

    def my_touch(self, action):
        if action=='down':
            self.state = 'down'
        elif action=='up':
            self.state = 'up'
            self.callback()

    # FIXME: do this better?
    def _darken(self, t, amount=0.8):
        lst = list(t)
        lst[0] *= amount
        lst[1] *= amount
        lst[2] *= amount
        return tuple(lst)

    def _luminance(self, color):
        return (float(color[0])/255.0)*0.2126 + \
               (float(color[1])/255.0)*0.7152 + \
               (float(color[2])/255.0)*0.0722

    def render(self):
        if self.state == 'up':
            back_color = self.color
        elif self.state == 'down':
            back_color = self._darken(self.color)

        if self._luminance(back_color) < 0.5:
            font_color = 'white'
        else:
            font_color = 'black'

        tingbot.screen.rectangle(self.xy, self.size, color=back_color)
        tingbot.screen.text(self.label, xy=self.xy, color=font_color, max_width=self.size[0], max_lines=1, font_size=13)

    @classmethod
    def renderAll(self):
        for instance in self.instances:
            instance.render()
