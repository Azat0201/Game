import pygame


class Button:
    width = None
    height = None
    gap = None
    button_color = None
    activated_color = None

    def __init__(self, x, y, function, text=None, activator=False, additional_text=None, parameters=None, width=None,
                 height=None, gap=None, button_color=None, activated_color=None):
        if text is None:
            text = ''
        if parameters is None:
            parameters = ()
        for par in ('width', 'height', 'gap', 'button_color', 'activated_color'):
            if eval(par) is None:
                value = self.__class__.__dict__[par]
            else:
                value = eval(par)
            self.__dict__['_' + par] = value
        self._activated = False
        self._rect = pygame.Rect(x - self._width // 2, y - self._height // 2, self._width - self._gap // 2, self._height - self._gap // 2)
        self._frame = pygame.Rect(x - self._width // 2, y - self._height // 2, self._width, self._height)
        self._function = function
        self._text = text
        self._additional_text = additional_text
        self._parameters = (self,) if parameters == 'self' else parameters
        self._activator = activator

    def use_function(self):
        self._function(*self._parameters)

    @property
    def color(self):
        activated = self._activated
        self._activated = False
        return self._activated_color if self._activator or activated else self.button_color

    @property
    def rect(self):
        return self._rect

    @property
    def frame(self):
        return self._frame

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, other_text):
        self._text = other_text

    @property
    def additional_text(self):
        return self._additional_text

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, other_parameters):
        self._parameters = other_parameters

    def change_active(self):
        self._activated = not self._activated
