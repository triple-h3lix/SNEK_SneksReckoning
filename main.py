import os
import sys

import pygame as pg

import colors
import constants
import sounds

pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "True"

""" Create window and render Screen surface """
clock = pg.time.Clock()
flags = (pg.HWSURFACE | pg.FULLSCREEN)
video = pg.display
video.set_caption('SNEK: THE RECKONING')
screen = video.set_mode(constants.display_size)

""" Loads font for all displayed text """
font = pg.font.Font("retro.ttf", 20)

""" Preloads images and parameters """
_image_library = {}


def img_loader(path):
    global _image_library
    img = _image_library.get(path)
    if img == None:
        canonicalized = path.replace('/', os.sep).replace('\\', os.sep)
        img = pg.image.load(canonicalized).convert()
        _image_library[path] = img
    img_rect = img.get_rect()
    img_size = img.get_size()
    return img, img_rect, img_size


img_background = pg.image.load(os.path.join('resources', 'img', 'background3.png')).convert()
level_size = img_background.get_size()
level_rect = img_background.get_rect()
img_title_screen = pg.image.load(os.path.join('resources', 'img', 'title.png')).convert()
img_bomb = pg.image.load(os.path.join('resources', 'img', 'bomb.png')).convert_alpha()
bomb_size = img_bomb.get_size()
img_apple = pg.image.load(os.path.join('resources', 'img', 'apple.png')).convert_alpha()
apple_size = img_apple.get_size()
img_head = pg.image.load(os.path.join('resources', 'img', 'snakehead.png')).convert_alpha()
img_body = pg.image.load(os.path.join('resources', 'img', 'snakebody.png')).convert()
img_heart = pg.image.load(os.path.join('resources', 'img', 'heart.png')).convert_alpha()
img_heart = pg.transform.scale(img_heart, (20, 20))
img_dog = pg.image.load(os.path.join('resources', 'img', 'bruh.png')).convert()
img_dog = pg.transform.scale(img_dog, (480, 440))
img_dog_neg = pg.image.load(os.path.join('resources', 'img', 'bruh_neg.png')).convert()
img_dog_neg = pg.transform.scale(img_dog_neg, (480, 440))
img_explosion = pg.image.load(os.path.join('resources', 'img', 'explosion.png')).convert_alpha()
img_explosion = pg.transform.scale2x(img_explosion)
explosion_size = img_explosion.get_size()

""" Default starting values """
direction = "right"
score = 0
apples_eaten = 0

""" Places an object origin point at center of screen """


def centered(obj_width, obj_height):
    x = (constants.display_width / 2) - (obj_width / 2)
    y = (constants.display_height / 2) - (obj_height / 2)

    center = (x, y)
    return center


""" These functions are used to assign the random coordinates """


def random_x(object_size):
    import random
    x = int(round(random.randrange(object_size[0], (constants.level_w - object_size[0])) / 10.0) * 10.0) + 60
    return x


def random_y(object_size):
    import random
    y = int(round(random.randrange(object_size[1], (constants.level_h - object_size[1])) / 10.0) * 10.0) + 40
    return y


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y, image=img_head):
        pg.sprite.Sprite.__init__(self)
        self.x = int(x)
        self.y = int(y)
        self.move_x = move_x
        self.move_y = move_y
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = "right"
        self.body = []
        self.health = 3
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def render(self, parts_list):
        if self.direction == "right":
            head = pg.transform.rotate(img_head, 270)
        if self.direction == "left":
            head = pg.transform.rotate(img_head, 90)
        if self.direction == "up":
            head = img_head
        if self.direction == "down":
            head = pg.transform.rotate(img_head, 180)

        screen.blit(head, (parts_list[-1][0], parts_list[-1][1]))

        for part in parts_list[:-1]:
            screen.blit(img_body, [part[0], part[1]])

        return self.rect

    def moveUp(self):
        self.direction = "up"
        self.move_x = 0
        self.move_y = -constants.block_size

    def moveDown(self):
        self.direction = "down"
        self.move_x = 0
        self.move_y = constants.block_size

    def moveLeft(self):
        self.direction = "left"
        self.move_x = -constants.block_size
        self.move_y = 0

    def moveRight(self):
        self.direction = "right"
        self.move_x = constants.block_size
        self.move_y = 0


class Apple(pg.sprite.Sprite):
    """
    A class for tasty apples
    """

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = int(x)
        self.y = int(y)
        self.pic = img_apple
        self.size = self.pic.get_size()
        self.rect = self.pic.get_rect()

    def render(self, screen):
        screen.blit(self.pic, (self.x, self.y))
        return self.rect


class Bomb(pg.sprite.Sprite):
    """
    A class for our bombs that damage the player
    """

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = int(x)
        self.y = int(y)
        self.pic = img_bomb
        self.size = self.pic.get_size()
        self.rect = self.pic.get_rect()
        self.collider = pg.Rect(self.rect)

    def render(self, screen):
        screen.blit(self.pic, (self.x, self.y))

    def is_hit(self, screen):
        screen.blit(img_explosion, (
            self.x - (explosion_size[0] / 2) + constants.block_size,
            self.y - (explosion_size[1] / 2) + constants.block_size))
        video.flip()
        pg.time.wait(20)


def message_to_screen(msg, color, x_offset, y_offset):
    """
    Display text in center of game screen
    :param msg: String you want displayed
    :param color: What color you want the text displayed as
    :param x_offset: Offset the location of text horizontally
    :param y_offset: Offset the location of text vertically
    """
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [((constants.display_width / 2) + x_offset) - (screen_text.get_width() / 2),
                              ((constants.display_height / 2) + y_offset) - (screen_text.get_height() / 2)])
    pg.time.wait(1)


def show_text(msg, color, x_coord, y_coord):
    """
    Display text at coordinates (for non-centered text)
    :param msg: String you want displayed
    :param color: What color you want text displayed as
    :param x_coord: Horizontal location
    :param y_coord: Vertical location
    """
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, (x_coord, y_coord))


def letter_by_letter(string):
    """
    Display a black screen with text typed letter by letter
    :param string: Text you want displayed
    :return:
    """
    text = ''
    for i in range(len(string)):
        screen.fill(colors.Black)
        text += string[i]
        text_surface = font.render(text, True, colors.White)
        text_rect = text_surface.get_rect()
        text_rect.center = (constants.display_width / 2, constants.display_height / 2)
        screen.blit(text_surface, [text_rect[0], text_rect[1], text_rect[2], text_rect[3]])
        sounds.text()
        pg.display.update()
        pg.time.wait(100)


def title():
    """
    This shows the title screen before the game starts
    """
    screen.blit(img_title_screen, (0, 0))
    video.flip()
    sounds.music_play('title_music.ogg')
    while True:
        ev = pg.event.poll()
        if ev.type == pg.KEYDOWN and ev.key == pg.K_RETURN:
            sounds.startgame()
            break
    screen.fill(colors.Black)
    letter_by_letter('I came to eat apples')
    pg.time.wait(200)
    letter_by_letter('and chew bubblegum...')
    pg.time.wait(1000)
    sounds.begin()


def flash_screen():
    """
    Just a little animation effect I created to make dying funny
    """
    sounds.music_stop()
    color = [colors.Red, colors.Yellow, colors.Blue, colors.Cyan, colors.Green, colors.Magenta, colors.White]

    for i in color * 4:
        screen.blit(img_dog_neg, (120, 20))
        pg.time.delay(30)
        video.flip()
        screen.fill(i)
        pg.time.delay(30)
        video.flip()
        screen.blit(img_dog, (120, 20))
        pg.time.delay(30)
        video.update()


def healthbar(num_of_hearts):
    """
    This function controls how much health you have as well as populates your health bar with heart icons
    :param num_of_hearts: The number of hearts you start with
    """
    lives = (
        (80, 10),
        (120, 10),
        (160, 10)
    )

    for i in range(num_of_hearts):
        screen.blit(img_heart, lives[i])

def gameloop(replay):
    """
    Everything that makes the game work
    :param replay: Only show title if NOT restarting
    """
    global direction
    global score
    global apples_eaten

    _Running = True
    _GameOver = False
    _ShowTitle = replay

    """ Initial starting points """
    # snake_x = constants.display_width / 2
    # snake_y = constants.display_height / 2

    """ Create instance of player character """
    player = Player(constants.display_width / 2, constants.display_height / 2, move_x=10, move_y=0)

    """ Create the list of bombs to populate the level """
    apple = Apple(random_x(apple_size), random_y(apple_size))

    bombs = []
    for i in range(5):
        bombs.append(Bomb(random_x(apple_size), random_y(apple_size)))

    def eat_apple():
        """
        Defines what occurs when the player collides with an apple object
        """
        global score
        global apples_eaten

        sounds.eat_apple()
        constants.snake_length += 1
        screen.fill(colors.White)
        pg.time.wait(30)
        video.update()
        pg.time.wait(60)
        constants.FPS += 0.5
        apples_eaten += 1

    while _Running:

        while _ShowTitle:
            title()
            pg.time.wait(1000)
            sounds.music_stop()
            """ Initializes/plays background music """
            sounds.music_play('road_to_snekistan.ogg')
            _ShowTitle = False

        while _GameOver:
            sounds.music_stop()
            player.x = 1
            player.y = 1

            screen.fill(colors.White)
            message_to_screen("GAME OVER", colors.Red, 0, -20)
            show_score = font.render("Your final score was " + str(score), True, colors.Black)
            screen.blit(show_score, [(constants.display_width / 2) - (show_score.get_width() / 2), 240])

            """ Add up and display the number of apples you ate after dying """
            if apples_eaten > 0:
                for ate in range(apples_eaten + 1):
                    screen.fill(colors.White)
                    message_to_screen("GAME OVER", colors.Red, 0, -20)
                    show_score = font.render("Your final score was " + str(score), True, colors.Black)
                    screen.blit(show_score, [(constants.display_width / 2) - (show_score.get_width() / 2), 240])
                    apple_large = pg.transform.scale2x(img_apple)
                    screen.blit(apple_large, [(constants.display_width / 2) - 70, 280])
                    eaten_count = font.render(" x " + str(ate), True, colors.Black)
                    screen.blit(eaten_count, [(constants.display_width / 2), 290])
                    sounds.bling()
                    pg.time.delay(50)
                    video.flip()
            else:
                pass

            video.flip()
            sounds.game_over()
            pg.time.delay(5000)
            screen.fill(colors.White)
            message_to_screen("Play again? Y or N", colors.Black, 0, -20)
            video.update()

            while True:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_y:
                            constants.snake_length = 3
                            direction = "right"
                            constants.FPS = 10
                            apples_eaten = 0
                            score = 0
                            sounds.music_play('the_reckoning.ogg')
                            gameloop(False)
                        if event.key == pg.K_n:
                            """ Save score to scores.txt and exit """
                            scores = open('scores.txt', 'w')
                            scores.write(str(score))
                            screen.fill(colors.Black)
                            video.flip()
                            scores.close()
                            quit()

        """ Movement controls """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                _Running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and player.direction != "right":
                    player.moveLeft()
                elif event.key == pg.K_RIGHT and player.direction != "left":
                    player.moveRight()
                elif event.key == pg.K_UP and player.direction != "down":
                    player.moveUp()
                elif event.key == pg.K_DOWN and player.direction != "up":
                    player.moveDown()
                elif event.key == pg.K_ESCAPE:
                    _Running = False

        """ Makes sure snake continues moving in current direction """
        player.x += player.move_x
        player.y += player.move_y

        """ Create background """
        screen.fill(colors.Black)
        screen.blit(img_background, (60, 40))

        """ Draw apples and bombs """
        apple.render(screen)

        for i in bombs:
            i.render(screen)

        """ Draw player head and body """
        snake_head = [player.x, player.y]
        player.body.append(snake_head)
        player.render(player.body)

        """ Keeps snake the same length while moving around level """
        if len(player.body) > constants.snake_length:
            del player.body[0]

        """ Draw Health Meter """
        healthbar(player.health)

        """ Draw score counter to screen """
        show_text("Score: " + str(score), colors.White, (constants.display_width / 2) - 50, 5)

        """ Game Over when player runs into self """
        for segment in player.body[:-1]:
            if segment == snake_head:
                sounds.xplode()
                flash_screen()
                _GameOver = True

        """ Game Over if player leaves area """
        if player.x >= constants.level_w + 60 or player.x <= 60 or player.y >= constants.level_h + 40 or player.y <= 40:
            _GameOver = True
            sounds.xplode()
            flash_screen()

        """ Game Over when health hits zero """
        if player.health == 0:
            sounds.xplode()
            flash_screen()
            _GameOver = True

        """ Handles collision detection between snake and apples/bombs """
        if apple.x <= player.x < apple.x + apple.size[0]:
            if apple.y <= player.y < apple.y + apple.size[1]:
                eat_apple()
                apple.x = random_x(apple.size)
                apple.y = random_y(apple.size)
                score += 10
                bombs.clear()
                for i in range(5):
                    bombs.append(Bomb(random_x(apple_size), random_y(apple_size)))

                if (apples_eaten % 10 == 0) and (player.health <= 2):
                    player.health += 1

        for target in bombs:
            if target.x <= player.x < target.x + target.size[0]:
                if target.y <= player.y < target.y + target.size[1]:
                    target.is_hit(screen)
                    sounds.bomb()
                    sounds.scream()
                    bombs.remove(target)
                    video.flip()
                    player.health -= 1

        video.update()
        clock.tick(constants.FPS)

    pg.quit()
    quit()
    sys.exit()


if __name__ == '__main__':
    gameloop(True)
