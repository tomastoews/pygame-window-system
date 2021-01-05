#!/usr/bin/python3

import pygame
import pygame.locals

pygame.init()
pygame.font.init()

screen_width, screen_height = 1400, 800
INITIAL_WINDOW_WIDTH = 500
INITIAL_WINDOW_HEIGHT = 300
origin_mouse_pos = None

fps = 60
pygame.mouse.set_visible(True)
pygame.display.init()
screen = pygame.display.set_mode(
    size=(screen_width, screen_height),
    #flags=pygame.FULLSCREEN
)

title_font = pygame.font.SysFont('Sans Regular', 20)
font1 = pygame.font.SysFont('Sans Regular', 24)

windows = list()
focused_window_index = None

class Window(pygame.Rect):
    def __init__(self, x, y, title):
        super().__init__(self)
        self.is_resizing = False
        self.is_dragging = False
        self.is_fullscreen = False
        self.border = 10
        self.title_bar_height = 40
        self.title_bar_button_height = 20
        self.title = title
        self.x = x
        self.y = y
        self.width = INITIAL_WINDOW_WIDTH+(self.border*3)
        self.height = INITIAL_WINDOW_HEIGHT+(self.border*2)
        self.title_text = title_font.render(self.title, False, (255,255,255))
        self.title_bar = pygame.Rect(0,0,0,0)
        self.container = pygame.Rect(0,0,0,0)
        self.fullscreen_button = pygame.Rect(0,0,0,0)
        self.resize_button = pygame.Rect(0,0,0,0)
        self.lines = []
        self.elements = []
        self.update()

    def get_rectangle_lines(self, rectangle):
        return [
            # Rectangle top
            ((rectangle.x, rectangle.y), (rectangle.x+rectangle.width, rectangle.y)),
            # Rectangle bottom
            ((rectangle.x, rectangle.y+rectangle.height), (rectangle.x+rectangle.width, rectangle.y+rectangle.height)),
            # Rectangle left
            ((rectangle.x, rectangle.y), (rectangle.x, rectangle.y+rectangle.height)),
            # Rectangle right
            ((rectangle.x+rectangle.width, rectangle.y), (rectangle.x+rectangle.width, rectangle.y+rectangle.height))
        ]

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_fullscreen:
            self.toggle_fullscreen()
        if mouse_pos[0] <= 40 and mouse_pos[1] <= 40:
            self.snap_top_left_corner()
            return None
        elif mouse_pos[0] >= screen_width-40 and mouse_pos[1] <= 40:
            self.snap_top_right_corner()
            return None
        elif mouse_pos[0] <= 40 and mouse_pos[1] >= screen_height-40:
            self.snap_botton_left_corner()
            return None
        elif mouse_pos[0] >= screen_width-40 and mouse_pos[1] >= screen_height-40:
            self.snap_botton_right_corner()
            return None
        elif mouse_pos[0] > 40 and mouse_pos[0] < screen_width-40 and mouse_pos[1] <= 40:
            self.snap_top()
            return None
        elif mouse_pos[0] > 40 and mouse_pos[0] < screen_width-40 and mouse_pos[1] >= screen_height-40:
            self.snap_bottom()
            return None
        elif mouse_pos[0] <= 40 and mouse_pos[1] > 40 and mouse_pos[1] < screen_height-40:
            self.snap_left()
            return None
        elif mouse_pos[0] >= screen_width-40 and mouse_pos[1] > 40 and mouse_pos[1] < screen_height-40:
            self.snap_right()
            return None
        # x_distance = (self.x - mouse_pos[0]) * -1
        # y_distance = (self.y - mouse_pos[1]) * -1
        x = mouse_pos[0] - (self.width/2)
        y = mouse_pos[1] - (self.border+self.title_bar.height/2)
        # print(f"Mouse: {mouse_pos[0]}, Window: {x}, Distance: {x_distance}")
        # print(f"Distance: {x_distance}")
        self.boxed_x = 0
        self.boxed_y = 0
        self.boxed_width = 0
        self.boxed_height = 0
        self.x = x
        self.y = y
        self.title_bar.x = x
        self.title_bar.y = y
        self.container.x = x
        self.container.y = self.title_bar.height
        self.update()

    def resize(self):
        # TODO: Fix minimum resize dimensions issue
        if self.is_fullscreen:
            self.is_fullscreen = False
        mouse_pos = pygame.mouse.get_pos()
        if self.width >= 200:
            self.width = mouse_pos[0] - self.x
        if self.height >= 200:
            self.height = mouse_pos[1] - self.y
        self.update()

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.boxed_x = self.x
            self.boxed_y = self.y
            self.boxed_width = self.width
            self.boxed_height = self.height
            self.is_fullscreen = True
        else:
            self.x = self.boxed_x
            self.y = self.boxed_y
            self.width = self.boxed_width
            self.height = self.boxed_height
            self.is_fullscreen = False
        self.update()

    def snap_top(self):
        self.x = 0
        self.y = 0
        self.width = screen_width - 1
        self.height = screen_height/2 - 1
        self.update()

    def snap_bottom(self):
        self.x = 0
        self.y = screen_height/2 - 1
        self.width = screen_width - 1
        self.height = screen_height/2 - 1
        self.update()

    def snap_right(self):
        self.x = screen_width/2 - 1
        self.y = 0
        self.width = screen_width/2 - 1
        self.height = screen_height - 1
        self.update()

    def snap_left(self):
        self.x = 0
        self.y = 0
        self.width = screen_width/2 - 1
        self.height = screen_height - 1
        self.update()

    def snap_top_left_corner(self):
        self.x = 0
        self.y = 0
        self.width = screen_width/2 - 1
        self.height = screen_height/2 - 1
        self.update()

    def snap_top_right_corner(self):
        self.x = screen_width/2 - 1
        self.y = 0
        self.width = screen_width/2 - 1
        self.height = screen_height/2 - 1
        self.update()

    def snap_botton_left_corner(self):
        self.x = 0
        self.y = screen_height/2 - 1
        self.width = screen_width/2 - 1
        self.height = screen_height/2 - 1
        self.update()

    def snap_botton_right_corner(self):
        self.x = screen_width/2 - 1
        self.y = screen_height/2 - 1
        self.width = screen_width/2 - 1
        self.height =  screen_height/2 - 1
        self.update()

    def update(self):
        if self.is_fullscreen:
            self.x = 0
            self.y = 0
            self.width = screen_width - 1
            self.height = screen_height - 1

        self.title_bar.x = self.x+self.border
        self.title_bar.y = self.y+self.border
        self.title_bar.width = self.width-(+self.border*2)
        self.title_bar.height = self.title_bar_height

        self.container.x = self.x+self.border
        self.container.y = self.y+self.title_bar.height+(self.border*2)
        self.container.width = self.width-(+self.border*2)
        self.container.height = self.height-(self.border*3)-self.title_bar.height

        self.fullscreen_button.x = self.title_bar.x+self.title_bar.width - self.title_bar_button_height - self.title_bar_height/4
        self.fullscreen_button.y = self.title_bar.y + self.title_bar_button_height - self.title_bar_height/4
        self.fullscreen_button.width = self.title_bar_button_height
        self.fullscreen_button.height = self.title_bar_button_height

        self.resize_button.x = (self.x+self.width)-self.border
        self.resize_button.y = (self.y+self.height)-self.border
        self.resize_button.width = self.border
        self.resize_button.height = self.border

        self.lines.clear()
        for line in self.get_rectangle_lines(self):
            self.lines.append(line)

        for line in self.get_rectangle_lines(self.title_bar):
            self.lines.append(line)

        for line in self.get_rectangle_lines(self.container):
            self.lines.append(line)

    def draw(self):
        global screen
        pygame.draw.rect(screen, (255,255,255), self, 1)
        pygame.draw.rect(screen, (255,255,255), self.title_bar, 1)
        pygame.draw.rect(screen, (255,255,255), self.container, 1)
        pygame.draw.rect(screen, (255,255,255), self.resize_button, 1)

        screen.fill((0,0,0), rect=self)
        screen.fill((0,0,0), rect=self.title_bar)
        screen.fill((0,0,0), rect=self.container)
        screen.fill((255,255,255), rect=self.resize_button)

        for line in self.lines:
            pygame.draw.line(screen, (255,255,255), line[0], line[1], 1)
        pygame.draw.rect(screen, (255,255,255), self.fullscreen_button, 1)

        for i in range(len(self.elements)):
            screen.blit(self.elements[i], (
                self.container.x+10,
                self.container.y+10+i*self.elements[i].get_height()
            ))
        screen.blit(self.title_text, (
            (self.title_bar.x+self.title_bar.width/2)-(self.title_text.get_width()/2),
            (self.title_bar.y+self.title_bar.height/2)-(self.title_text.get_height()/2)
        ))

def focus_window(index):
    global windows, focused_window_index
    window = windows[index]
    windows.pop(index)
    windows.append(window)
    focused_window_index = len(windows)-1

def switch_window_focus():
    global windows, focused_window_index
    if not focused_window_index == None:
        if focused_window_index < len(windows)-1:
            focus_window(focused_window_index + 1)
        elif focused_window_index == len(windows)-1:
            focus_window(0)

def events():
    global windows, focused_window_index, origin_mouse_pos
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit(0)
            #elif event.key == pygame.K_F12:
            #    pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_TAB:
                switch_window_focus()
            elif event.key == pygame.K_UP:
                if not focused_window_index == None:
                    windows[focused_window_index].snap_top()
            elif event.key == pygame.K_DOWN:
                if not focused_window_index == None:
                    windows[focused_window_index].snap_bottom()
            elif event.key == pygame.K_RIGHT:
                if not focused_window_index == None:
                    windows[focused_window_index].snap_right()
            elif event.key == pygame.K_LEFT:
                if not focused_window_index == None:
                    windows[focused_window_index].snap_left()
        if event.type == pygame.MOUSEMOTION:
            if not focused_window_index == None:
                if windows[focused_window_index].is_dragging:
                    windows[focused_window_index].move()
                elif windows[focused_window_index].is_resizing:
                    windows[focused_window_index].resize()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            windows = windows[::-1]
            for i in range(len(windows)):
                if windows[i].collidepoint(mouse_pos):
                    focus_window(i)
                    if windows[i].fullscreen_button.collidepoint(mouse_pos):
                        windows[i].toggle_fullscreen()
                        break
                    elif windows[i].title_bar.collidepoint(mouse_pos):
                        windows[i].is_dragging = True
                        origin_mouse_pos = mouse_pos
                        break
                    elif windows[i].resize_button.collidepoint(mouse_pos):
                        windows[i].is_resizing = True
                        origin_mouse_pos = mouse_pos
                        break
        if event.type == pygame.MOUSEBUTTONUP:
            if not focused_window_index == None:
                windows[focused_window_index].is_dragging = False
                windows[focused_window_index].is_resizing = False

def draw():
    global windows
    for window in windows:
        window.draw()

windows.append(Window(x=100, y=100, title="Window 1"))
windows.append(Window(x=screen_width-(100+INITIAL_WINDOW_WIDTH), y=100, title="Window 2"))

windows[0].elements.append(font1.render("Information and Help:", False, (255,255,255)))
windows[0].elements.append(font1.render("", False, (255,255,255)))
windows[0].elements.append(font1.render("This is a simple window system for PyGame.", False, (255,255,255)))
windows[0].elements.append(font1.render("Move a window by clicking and dragging the title bar.", False, (255,255,255)))
windows[0].elements.append(font1.render("Use the button in the title bar to maximize a window.", False, (255,255,255)))
windows[0].elements.append(font1.render("Click and drag the white rectange in the lower right corner to", False, (255,255,255)))
windows[0].elements.append(font1.render("resize a window.", False, (255,255,255)))
windows[0].elements.append(font1.render("Press the arrow keys to snap it to the top, bottom, left or right.", False, (255,255,255)))
windows[0].elements.append(font1.render("Move a window into any corner to snap it there.", False, (255,255,255)))
windows[0].elements.append(font1.render("Press TAB to switch the focus between windows.", False, (255,255,255)))
windows[0].elements.append(font1.render("", False, (255,255,255)))
# windows[0].elements.append(font1.render("Press F12 to toggle fullscreen.", False, (255,255,255)))
windows[0].elements.append(font1.render("Press ESC to exit the program.", False, (255,255,255)))

while True:
    screen.fill((0,0,0))
    events()
    draw()
    pygame.display.update()
