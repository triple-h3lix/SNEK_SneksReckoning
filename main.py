import os
import pygame as pg
import colors
import constants
import sounds

""" Load PyGame library and assign pg.display to the value video to simplify things """
pg.init()
video = pg.display

""" Sets up basics for rendering window """
clock = pg.time.Clock()
screen = video.set_mode(constants.display_size, pg.HWSURFACE)
video.set_caption('SNEK: THE RECKONING')
os.environ['SDL_VIDEO_CENTERED'] = "True"

""" Loads font for all displayed text """
font = pg.font.SysFont(None, 30)

""" Preloads images and parameters """
background = pg.image.load('background3.png')
background = background.convert()
level_size = background.get_size()
level_rect = background.get_rect()
bomb = pg.image.load('bomb.png').convert_alpha()
bomb_size = bomb.get_size()
apple = pg.image.load('apple.png').convert_alpha()
apple_size = apple.get_size()
img_head = pg.image.load('snakehead.png').convert_alpha()
snakebod = pg.image.load('snakebody.png').convert()

""" Default starting values """
direction = "right"
score = 0

""" These functions are used to assign the random coordinates """


def random_x(object_size):
    import random
    x = int(round(random.randrange(object_size[0], (constants.level_w - object_size[0])) / 10.0) * 10.0) + 60
    return x


def random_y(object_size):
    import random
    y = int(round(random.randrange(object_size[1], (constants.level_h - object_size[1])) / 10.0) * 10.0) + 40
    return y


def random_loc(object_size):
    import random
    x = round(random.randrange(object_size[0], (constants.level_w - object_size[0])) / 10.0) * 10.0
    y = round(random.randrange(object_size[1], (constants.level_h - object_size[1])) / 10.0) * 10.0

    location = (x, y)
    return location


def snake(parts_list):
    """
    This function draws the head of the snake, turns it in the appropriate direction, and builds the parts following it
    """
    if direction == "right":
        head = pg.transform.rotate(img_head, 270)

    if direction == "left":
        head = pg.transform.rotate(img_head, 90)

    if direction == "up":
        head = img_head

    if direction == "down":
        head = pg.transform.rotate(img_head, 180)

    screen.blit(head, (parts_list[-1][0], parts_list[-1][1]))

    for part in parts_list[:-1]:
        screen.blit(snakebod, [part[0], part[1]])


class Bomb:
    """
    A class for our bombs that damage the player
    """

    def __init__(self, x, y, pic=bomb, size=bomb_size):
        self.x = int(x)
        self.y = int(y)
        self.pic = pic
        self.size = size
        self.rect = self.pic.get_rect(center=(self.x / 2, self.y / 2))

    def render(self, screen):
        screen.blit(self.pic, (self.x, self.y))


def message_to_screen(msg, color):
    """
    Display text in center of game screen
    :param msg: String you want displayed
    :param color: What color you want the text displayed as
    """
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [(constants.display_width / 2) - (screen_text.get_width() / 2),
                              (constants.display_height / 2) - (screen_text.get_height() / 2)])
    pg.time.wait(1)


def title():
    """
    This shows the title screen before the game starts
    """
    title_screen = pg.image.load('title.png')
    title_screen.convert()
    screen.blit(title_screen, (0, 0))
    video.flip()


def flash_screen():
    """
    Just a little animation effect I created to make dying funny
    """
    dog = pg.image.load('bruh.png')
    dog = pg.transform.scale(dog, (480, 440))
    dog.convert()
    dog_neg = pg.image.load('bruh_neg.png')
    dog_neg = pg.transform.scale(dog_neg, (480, 440))
    dog.convert()

    sounds.music_stop()
    color = [colors.Red, colors.Yellow, colors.Blue, colors.Cyan, colors.Green, colors.Magenta, colors.White]

    for i in color * 4:
        screen.blit(dog_neg, (120, 20))
        pg.time.delay(30)
        video.flip()
        screen.fill(i)
        pg.time.delay(30)
        video.flip()
        screen.blit(dog, (120, 20))
        pg.time.delay(30)
        video.update()


def gameloop(replay):
    """
    Everything that makes the game work
    :param replay: Only show title if NOT restarting
    """
    global direction
    global score

    _Running = True
    _GameOver = False
    _ShowTitle = replay

    """ Initial starting points """
    snake_x = constants.display_width / 2
    snake_y = constants.display_height / 2
    apple_x = random_x(apple_size) / 2
    apple_y = random_x(apple_size) / 2
    bomb_x = random_x(bomb_size)
    bomb_y = random_y(bomb_size)

    """ Begin player movement """
    move_x = constants.block_size
    move_y = 0

    """ Opens file to store score data """
    scores = open('scores.txt', 'w')

    """ Initializes/plays background music """
    sounds.load_music()
    sounds.music_play()

    """ Player starts with full health (3 hearts) """
    hearts = 3

    """ Assigns the player a body """
    snake_list = []

    """ Create the list of bombs to populate the level """
    bombs = [Bomb(random_x(bomb_size), random_y(bomb_size)), Bomb(random_x(bomb_size), random_y(bomb_size)),
             Bomb(random_x(bomb_size), random_y(bomb_size)), Bomb(random_x(bomb_size), random_y(bomb_size)),
             Bomb(random_x(bomb_size), random_y(bomb_size))]

    def health(hearts):
        """
        This function controls how much health you have as well as populates your health bar with heart icons
        :param hearts: The number of hearts you start with
        """
        heart = pg.image.load('heart.png')
        heart = heart.convert_alpha()
        heart = pg.transform.scale(heart, (20, 20))

        lives = (
            (80, 10),
            (120, 10),
            (160, 10)
        )

        for i in range(hearts):
            screen.blit(heart, lives[i])

    def hit_bomb(loc):
        global bomb_x, bomb_y
        """
        Defines what occurs whenever the game detects collision between player and bomb object
        :param: 'loc' is the location of the bomb you hit, to determine where the explosion is shown
        """

        boom = pg.image.load('explosion.png')
        boom = boom.convert_alpha()
        explosion_size = boom.get_size()
        boom = pg.transform.scale(boom, ((explosion_size[0] * 3), (explosion_size[1] * 3)))
        screen.blit(boom, (loc.x - 40, loc.y - 40))
        video.flip()
        pg.time.wait(20)

    def eat_apple():
        """
        Defines what occurs when the player collides with an apple object
        """
        global score

        sounds.eat_apple()
        constants.snake_length += 1
        screen.fill(colors.White)
        pg.time.wait(30)
        video.update()
        pg.time.wait(60)
        constants.FPS += 0.5

    while _Running:

        while _ShowTitle:
            title()
            pg.time.wait(1500)
            sounds.begin()
            _ShowTitle = False

        while _GameOver:
            sounds.music_stop()
            snake_x = 1
            snake_y = 1
            screen.fill(colors.White)
            message_to_screen("GAME OVER", colors.Red)
            show_score = font.render("Your final score was " + str(score), True, colors.Black)
            screen.blit(show_score, [(constants.display_width / 2) - (show_score.get_width() / 2), 260])
            video.flip()
            sounds.game_over()
            pg.time.delay(5000)
            screen.fill(colors.White)
            message_to_screen("Play again? Y or N", colors.Black)
            video.update()

            while True:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_y:
                            gameloop(False)
                        if event.key == pg.K_n:
                            scores.write(str(score))
                            screen.fill(colors.Black)
                            video.flip()
                            quit()

        """ Movement controls """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                _Running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and direction != "right":
                    direction = "left"
                    move_x = -constants.block_size
                    move_y = 0
                elif event.key == pg.K_RIGHT and direction != "left":
                    direction = "right"
                    move_x = constants.block_size
                    move_y = 0
                elif event.key == pg.K_UP and direction != "down":
                    direction = "up"
                    move_y = -constants.block_size
                    move_x = 0
                elif event.key == pg.K_DOWN and direction != "up":
                    direction = "down"
                    move_y = constants.block_size
                    move_x = 0
                elif event.key == pg.K_ESCAPE:
                    _Running = False

        """ Makes sure snake continues moving in current direction """
        snake_x += move_x
        snake_y += move_y

        """ Create background """
        screen.fill(colors.Black)
        screen.blit(background, (60, 40))

        """ Spawn random objects (apple and bombs) """
        screen.blit(apple, (apple_x, apple_y))
        # screen.blit(bomb, (bomb_x, bomb_y))

        for i in bombs:
            i.render(screen)

        """ Spawn player head and body """
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        snake(snake_list)

        """ Keeps snake the same length while moving around level """
        if len(snake_list) > constants.snake_length:
            del snake_list[0]

        """ Draw Health Meter """
        health(hearts)

        """ Draw score counter to screen """
        score_board = font.render("Score: " + str(score), True, colors.White)
        screen.blit(score_board, [(constants.display_width / 2) - (score_board.get_width() / 2), 10])

        """ Game Over when player runs into self """
        for segment in snake_list[:-1]:
            if segment == snake_head:
                sounds.xplode()
                flash_screen()
                _GameOver = True

        """ Game Over if player leaves area """

        if snake_x >= constants.level_w + 60 or snake_x <= 60 or snake_y >= constants.level_h + 40 or snake_y <= 40:
            _GameOver = True
            sounds.xplode()
            flash_screen()

        """ Game Over when health hits zero """
        if hearts == 0:
            sounds.xplode()
            flash_screen()
            _GameOver = True

        """ Handles collision detection between snake and apples/bombs """
        if all([snake_x >= apple_x, snake_x < apple_x + apple_size[0], snake_y >= apple_y,
                snake_y < apple_y + apple_size[1]]):
            eat_apple()
            apple_x = random_x(apple_size)
            apple_y = random_y(apple_size)
            bombs.clear()
            bombs = [Bomb(random_x(bomb_size), random_y(bomb_size)), Bomb(random_x(bomb_size), random_y(bomb_size)),
                     Bomb(random_x(bomb_size), random_y(bomb_size)), Bomb(random_x(bomb_size), random_y(bomb_size)),
                     Bomb(random_x(bomb_size), random_y(bomb_size))]
            score += 10

        for target in bombs:
            if snake_x >= target.x and snake_x <= target.x + 10:
                if snake_y >= target.y and snake_y <= target.y + 10:
                    hit_bomb(target)
                    sounds.bomb()
                    video.flip()
                    bombs.remove(target)
                    hearts -= 1

        video.update()
        clock.tick(constants.FPS)

    scores.close()
    pg.quit()
    quit()


if __name__ == '__main__':
    gameloop(True)
