# 맨 처음 시작화면
import pygame as pg

pg.init()

Background = pg.image.load("background.jpg")
Background = pg.transform.scale(Background,(800,600))
Title = pg.image.load("Title.PNG")
Title = pg.transform.scale(Title,(680,150))

pg.mixer_music.load("backgroundmusic.mp3")
pg.mixer_music.play(-1,0.0)

screen = pg.display.set_mode((800, 600))
FONT = pg.font.SysFont('Comic Sans MS', 32)

IMAGE_NORMAL = pg.Surface((100, 32))
IMAGE_NORMAL.fill(pg.Color('brown'))
IMAGE_HOVER = pg.Surface((100, 32))
IMAGE_HOVER.fill(pg.Color('brown'))
IMAGE_DOWN = pg.Surface((100, 32))
IMAGE_DOWN.fill(pg.Color('black'))


def displayimage(Imagename,x,y):
    screen.blit(Imagename,(x,y))
class Button(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_DOWN):
        super().__init__()

        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))

        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)

        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)


        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal


class StartScreen:

    def __init__(self, screen):
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = screen

        self.all_sprites = pg.sprite.Group()
        self.number = 0

        self.start_button = Button(
            50, 350, 200, 65, self.start_game,
            FONT, 'Game Start', (255, 255, 255),
            IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)

        self.quit_button = Button(
            550, 350, 200, 65, self.quit_game,
            FONT, 'Quit', (255, 255, 255))

        self.how_to_play_button = Button(
            300, 350, 200, 65, self.how_to_play,
            FONT, 'How To Play', (255, 255, 255))
        self.back_button = Button(
            450,350,200,65,self.back,
            FONT,'Back',(255,255,255))

        self.all_sprites.add(self.start_button, self.quit_button,self.how_to_play_button)

    def quit_game(self):
        self.done = True

    def start_game(self):
        pass

    def how_to_play(self):
        screen.fill(30,30,30)
    def back(self):
        pass

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            for button in self.all_sprites:
                button.handle_event(event)

    def run_logic(self):
        self.all_sprites.update(self.dt)

    def draw(self):
        displayimage(Background,0,0)
        displayimage(Title,60,100)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == '__main__':
    StartScreen(screen).run()
    pg.quit()