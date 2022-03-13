import pygame

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
