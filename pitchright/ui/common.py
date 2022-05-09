import pygame


# https://stackoverflow.com/a/46390412
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.inactive = pygame.Color('lightskyblue3')
        self.active = pygame.Color('dodgerblue2')
        self.font = pygame.font.Font("res/OpenSans-Regular.ttf", 24)

        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.inactive
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active if self.active else self.inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.redraw_text()

    def redraw_text(self):
        self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image, rot_rect


def draw_text(font, screen, text, x, y, color):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x - (textobj.get_width().real / 2), y - (textobj.get_height().real / 2))
    screen.blit(textobj, textrect)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_button(surface, font, text, x, y, mx, my, xoff=0, color=(54, 54, 54, 100), color_highlight=(75, 75, 75, 255)):
    textobj = font.render(text, True, (255, 255, 255))
    textrect = textobj.get_rect().copy()

    textrect.x = x - (textobj.get_width().real / 2)
    textrect.y = y - (textobj.get_height().real / 2)

    background = pygame.Rect(textrect.x - 25, textrect.y - 25, textrect.width + 50, textrect.height + 50)
    button_color = color
    if background.collidepoint(mx - xoff, my):
        button_color = color_highlight
    pygame.draw.rect(surface, button_color, background)

    surface.blit(textobj, textrect)

    return background
