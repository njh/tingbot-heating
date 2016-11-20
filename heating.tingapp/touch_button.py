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
    def _darken(self, t):
        lst = list(t)
        lst[0] *= 0.8
        lst[1] *= 0.8
        lst[2] *= 0.8
        return tuple(lst)
    
    def render(self):
        if self.state == 'up':
            back_color = self.color
        elif self.state == 'down':
            back_color = self._darken(self.color)

        tingbot.screen.rectangle(self.xy, self.size, color=back_color)
        tingbot.screen.text(self.label, xy=self.xy, color='white', max_width=self.size[0], max_lines=1, font_size=12)

    @classmethod
    def renderAll(self):
        for instance in self.instances:
            instance.render()
