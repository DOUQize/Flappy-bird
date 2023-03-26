import arcade
from random import randint


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
score = 0
TITLE = "Flappy bird"
TUBE_SPEED = 3
TUBE_GAP = 280
MAX_FALL_SPEED = 6
FALL_SPEED = 0.5
MAX_ANGLE = 36
ANGLE_SPEED = 2
JUMP_SPEED = 10
dist = None


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.BABY_BLUE)
        self.scene = None
        self.ground_list = None
        self.cloud_list = None

    def setup(self):
        self.scene = arcade.Scene()

        self.city = arcade.Sprite("city.png", 0.57)
        self.city.center_x = 200
        self.city.center_y = 120
        self.scene.add_sprite("City", self.city)
        self.city1 = arcade.Sprite("city.png", 0.57)
        self.city1.center_x = 599
        self.city1.center_y = 120
        self.scene.add_sprite("City1", self.city1)

        self.cloud_list = arcade.SpriteList()
        self.cloud_list_posx = [0, 225, 510, 765]
        for i in range(4):
            cloud = Cloud()
            cloud.center_x = self.cloud_list_posx[i]
            cloud.center_y = randint(350, 550)
            self.cloud_list.append(cloud)
        self.scene.add_sprite_list("Clouds", False, self.cloud_list)

        self.tube = Tube()
        self.scene.add_sprite("Tube", self.tube)
        self.tube_flip = Tube_flip()
        self.scene.add_sprite("Tube_flip", self.tube_flip)
        self.tube1 = Tube()
        self.scene.add_sprite("Tube1", self.tube1)
        self.tube_flip1 = Tube_flip()
        self.scene.add_sprite("Tube_flip1", self.tube_flip1)
        self.tube1.position = [1000, -80]
        self.tube_flip1.position = [1000, 480]

        self.ground_list = arcade.SpriteList()
        for x in range(0, SCREEN_WIDTH+132, 66):
            ground = Dirt()
            ground.center_x = x
            ground.center_y = 32
            self.ground_list.append(ground)
        self.scene.add_sprite_list("Ground", False, self.ground_list)

        self.bird = Bird()
        self.scene.add_sprite("Bird", self.bird)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        arcade.draw_text(f"Score: {score}", 100, SCREEN_HEIGHT-100, [0, 0, 0], 20)

    def update(self, delta_time: float):
        self.scene.update()
        if self.bird.change_y < MAX_FALL_SPEED:
            self.bird.change_y += FALL_SPEED
        if self.bird.angle > -MAX_ANGLE:
            self.bird.angle -= ANGLE_SPEED

        if arcade.check_for_collision(self.bird, self.tube):
            dead()
        if arcade.check_for_collision(self.bird, self.tube1):
            dead()
        if arcade.check_for_collision(self.bird, self.tube_flip):
            dead()
        if arcade.check_for_collision(self.bird, self.tube_flip1):
            dead()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.bird.change_y = -JUMP_SPEED
            self.bird.angle = 60


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__("bird.png", 1)
        self.change_y = 5
        self.center_x = 200
        self.center_y = 300
        self.angle = 0

    def update(self):
        self.center_y -= self.change_y
        if self.center_y < 76:
            self.center_y = 76
            self.angle = 0
        if self.center_y > SCREEN_HEIGHT - 12:
            self.center_y = SCREEN_HEIGHT - 12
            self.angle = 0


class Tube(arcade.Sprite):
    def __init__(self):
        super().__init__("tube.png", 1)
        self.change_x = TUBE_SPEED
        self.center_x = 600
        self.center_y = 20

    def update(self):
        self.center_x -= self.change_x
        if self.center_x <= -25:
            self.center_x = SCREEN_WIDTH+25
            global dist
            dist = randint(200, 400)
            self.center_y = dist - TUBE_GAP
        if 202 > self.center_x > 198:
            global score
            score += 1


class Tube_flip(arcade.Sprite):
    def __init__(self):
        super().__init__("tube.png", 1, flipped_vertically=True)
        self.change_x = TUBE_SPEED
        self.center_x = 600
        self.center_y = 580

    def update(self):
        self.center_x -= self.change_x
        if self.center_x <= -25:
            self.center_x = SCREEN_WIDTH+25
            self.center_y = dist + TUBE_GAP

class Dirt(arcade.Sprite):
    def __init__(self):
        super().__init__("dirt.png", 1)
        self.center_y = 32
        self.center_x = 0

    def update(self):
        self.center_x -= TUBE_SPEED
        if self.center_x < -66:
            self.center_x = SCREEN_WIDTH+66

class Cloud(arcade.Sprite):
    def __init__(self):
        super().__init__("pngegg.png", 0.2)

    def update(self):
        self.center_x -= 1
        if self.center_x < - 110:
            self.center_x = SCREEN_WIDTH + 110
            self.center_y = randint(350, 550)

def dead():
    print("You died")
    print(f"score: {score}")
    arcade.close_window()

window = Game()
window.setup()
arcade.run()