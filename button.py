from datetime import datetime
import pygame
import sys

pygame.init()
fps = 60

fpsClock = pygame.time.Clock()

width, height = 700, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont("Arial", 40)

objects = []

class Button:
    def __init__(self, x: int, y: int, button_width: int, button_height: int, buttonText: str = "Button",
                 onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333"
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors["normal"])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors["pressed"])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


class Clicker:
    def __init__(self):
        self.clicks = 0
        self.CPS = 0
        self.processing_clicks = True
        self.started_datetime = datetime.now().timestamp()
        self.stopped_datetime = None

    def update_clicks(self):
        self.clicks += 1

    def update_cps(self):
        running_time = datetime.now().timestamp() - self.started_datetime
        self.CPS = round(self.clicks / running_time, 2)

    def get_running_time(self) -> datetime.timestamp:
        if self.processing_clicks:
            return datetime.now().timestamp() - self.started_datetime
        else:
            return self.stopped_datetime - self.started_datetime

    def get_clicks(self):
        return self.clicks

    def get_cps(self):
        return self.CPS

    def check_if_on(self):
        return self.processing_clicks

    def turn_off(self):
        self.processing_clicks = False
        self.stopped_datetime = datetime.now().timestamp()

    def turn_on(self):
        self.clicks = 0
        self.CPS = 0
        self.processing_clicks = True
        self.started_datetime = datetime.now().timestamp()
        self.stopped_datetime = None


clicker = Clicker()
Button(30, 30, 400, 100, "PRESS ME!", clicker.update_clicks)
Button(450, 30, 200, 50, "Stop", clicker.turn_off)
Button(450, 90, 200, 50, "Start Again", clicker.turn_on)

while True:
    screen.fill((32, 56, 178))

    font = pygame.font.SysFont("Arial", 36)
    cpssurface = font.render(f"CPS: {clicker.get_cps()}", True, (206, 22, 22))
    screen.blit(cpssurface, (200 - cpssurface.get_width(), 200 - cpssurface.get_height()))
    clickssurface = font.render(f"Clicks: {clicker.get_clicks()}", True, (206, 22, 22))
    screen.blit(clickssurface, (200 - clickssurface.get_width(), 400 - clickssurface.get_height()))
    timersurface = font.render(f"Timer: {round(clicker.get_running_time(), 1)}", True, (206, 22, 22))
    screen.blit(timersurface, (200 - timersurface.get_width(), 300 - timersurface.get_height()))

    if clicker.check_if_on():
        clicker.update_cps()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for object_ in objects:
        object_.process()

    pygame.display.flip()
    fpsClock.tick(fps)
