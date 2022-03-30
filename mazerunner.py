import pygame
import math
import gym
from gym import spaces
import numpy as np
import cv2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls """

    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, x, y):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def checkDir(self, walls):
        x1, y1 = self.rect.topleft
        x1b, y1b = self.rect.bottomright
        #right, up, left, down
        res = [SCREEN_WIDTH - x1b, y1, x1, SCREEN_HEIGHT - y1b]
        for wall in walls:
            x2, y2 = wall.rect.topleft
            x2b, y2b = wall.rect.bottomright
            if x2 >= x1b: #is to the right
                if y2 <= y1b and y2b >= y1: #is overlapping vertically
                    distR = abs(x1b - x2)
                    if distR < res[0]:
                        res[0] = distR
            elif x1 >= x2b: #is to the left
                if y2 <= y1b and y2b >= y1: #is overlapping vertically
                    distL = abs(x1 - x2b)
                    if distL < res[2]:
                        res[2] = distL
            else: #is above or below
                if y1 >= y2b: #is above
                    distU = abs(y1 - y2b)
                    if distU < res[1]:
                        res[1] = distU

                else:
                    distD = abs(y1b - y2)
                    if distD < res[3]:
                        res[3] = distD
        return res





    def move(self, walls):

        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Room(object):
    """ Base class for all rooms. """

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class Room1(Room):
    """This creates all the walls in room 1"""
    def __init__(self):
        super().__init__()
        # Make the walls. (x_pos, y_pos, width, height)

        # This is a list of walls. Each is in the form [x, y, width, height]
        walls = [[0, 0, 20, 350, WHITE],
                 [0, 350, 20, 250, WHITE],
                 [780, 0, 20, 250, WHITE],
                 [780, 350, 20, 250, WHITE],
                 [20, 0, 760, 20, WHITE],
                 [20, 580, 760, 20, WHITE],
                 [390, 50, 20, 500, BLUE]
                ]

        # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room2(Room):
    """This creates all the walls in room 2"""
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, RED],
                 [0, 350, 20, 250, RED],
                 [780, 0, 20, 250, RED],
                 [780, 350, 20, 250, RED],
                 [20, 0, 760, 20, RED],
                 [20, 580, 760, 20, RED],
                 [190, 50, 20, 500, GREEN],
                 [590, 50, 20, 500, GREEN]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room3(Room):
    """This creates all the walls in room 3"""
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, PURPLE],
                 [0, 350, 20, 250, PURPLE],
                 [780, 0, 20, 250, PURPLE],
                 [780, 350, 20, 250, PURPLE],
                 [20, 0, 760, 20, PURPLE],
                 [20, 580, 760, 20, PURPLE]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, RED)
                self.wall_list.add(wall)

        for x in range(150, 700, 100):
            wall = Wall(x, 200, 20, 200, WHITE)
            self.wall_list.add(wall)



class MazeEnv(gym.Env ):
    def __init__(self, time_limit = 10000, nice_render = False):
        super(MazeEnv, self).__init__()
# Define action and observation space
# They must be gym.spaces objects
# Example when using discrete actions:

        self.action_space = spaces.Discrete(3)
# Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=255, shape=(240, 80, 1), dtype=np.uint8)
        pygame.init()
        self.nice_render = nice_render
        self.maxTime = time_limit
        self.farthestInRoom = SCREEN_WIDTH * 3
        self.prev_reward = 0.0
        self.episode_reward = 0.0
        self.current_dir = 2
        self.history = []
        for i in range(0, 6):
            self.history.append(np.zeros((80, 80)))

# Create an 800x600 sized screen
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.info = {"episode_number" : 0}

# Set the title of the window
        pygame.display.set_caption('Maze Runner')
        self.time_limit = time_limit
        self.rooms = []

        room = Room1()
        self.rooms.append(room)

        room = Room2()
        self.rooms.append(room)

        room = Room3()
        self.rooms.append(room)

    def reward(self):
        return ((1+ self.current_room_no) * 1.0) +  -0.8 * math.sqrt((self.player.rect.x - SCREEN_WIDTH)**2 + (self.player.rect.y - SCREEN_HEIGHT/2)**2) / SCREEN_WIDTH

    def distToGoal(self):
        return math.sqrt((self.player.rect.x - SCREEN_WIDTH)**2 + (self.player.rect.y - SCREEN_HEIGHT/2)**2)


    def step(self, action):
        reward = 0.0
        dense_reward = 0.0
        done = False
        self.player.change_x = 0
        self.player.change_y = 0
        if action == 0:
            self.current_dir -= 1
        elif action == 2:
            self.current_dir += 1
        if self.current_dir == 8:
            self.current_dir = 0
        if self.current_dir < 0:
            self.current_dir = 7

        if self.current_dir == 0:
            self.player.change_y = -5
        elif self.current_dir == 1:
            self.player.change_y = -5
            self.player.change_x = 5
        elif self.current_dir == 2:
            self.player.change_x = 5
        elif self.current_dir == 3:
            self.player.change_y = 5
            self.player.change_x = 5
        elif self.current_dir == 4:
            self.player.change_y = 5
        elif self.current_dir == 5:
            self.player.change_y = 5
            self.player.change_x = -5
        elif self.current_dir == 6:
            self.player.change_x = -5
        elif self.current_dir == 7:
            self.player.change_y = -5
            self.player.change_x = -5

        self.player.move(self.current_room.wall_list)

        if self.player.rect.x < -15:
            self.time_limit -= 500
            print("Went back a room, -100 score")
            if self.current_room_no == 0:
                self.current_room_no = 2
                self.current_room = self.rooms[self.current_room_no]
                self.player.rect.x = 790
                reward -= 100

            elif self.current_room_no == 2:
                self.current_room_no = 1
                self.current_room = self.rooms[self.current_room_no]
                self.player.rect.x = 790
                reward -= 100
            else:
                self.current_room_no = 0
                self.current_room = self.rooms[self.current_room_no]
                self.player.rect.x = 790
                reward -= 100

        if self.player.rect.x > 801:
            self.time_limit += 500
            self.prev_reward = self.distToGoal() + 1
            print("Next room reached, +100 score")
            if self.current_room_no == 0:
                self.current_room_no = 1
                self.current_room = self.rooms[self.current_room_no]
                self.player.rect.x = 0
                reward += 100
            elif self.current_room_no == 1:
                self.current_room_no = 2
                self.current_room = self.rooms[self.current_room_no]
                self.player.rect.x = 0
                reward += 100
            else:
                self.current_room_no = 0
                self.current_room = self.rooms[self.current_room_no]
                self.player.rect.x = 50
                reward += 100
        self.time_limit -= 1
        if self.time_limit <= 0:
            done = True
        #dense_reward = self.reward()
        self.render()
        #observation = pygame.surfarray.array3d(pygame.display.get_surface())
        observation = self.pre_processing(pygame.surfarray.array3d(pygame.display.get_surface()))

        dense_reward = self.prev_reward - self.distToGoal()
        self.prev_reward = self.distToGoal()
        #reward += dense_reward
        if dense_reward == 0.0:
            reward -= 1
        self.episode_reward += reward
        return observation, reward, done, self.info


    def pre_processing(self, image):
        image = cv2.cvtColor(cv2.resize(image, (80, 80)), cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
        #image = image[ :, :, None].astype(np.float32)
        #_, image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
        image = image / 255
        del self.history[0]
        self.history.append(image)
        #print(type(image))
        #print(image.shape)
        image = np.concatenate((self.history[-5], self.history[-3], image), axis=0)
        #print(image.shape)
        image = np.expand_dims(image, axis=-1)
        #print(image.shape)
        return image

    def reset(self, time_limit=100):
# Call this function so the Pygame library can initialize itself

# Create the player paddle object
        self.player = Player(50, 50)
        self.movingsprites = pygame.sprite.Group()
        self.movingsprites.add(self.player)
        self.time_limit = self.maxTime
        self.episode_reward = 0.0


        self.current_room_no = 0
        self.current_room = self.rooms[self.current_room_no]

        self.clock = pygame.time.Clock()

        #observation = pygame.surfarray.array3d(pygame.display.get_surface())
        observation = self.pre_processing(pygame.surfarray.array3d(pygame.display.get_surface()))
        return observation  # reward, done, info can't be included

    def render(self, mode='human'):
        if self.nice_render:
            self.screen.fill(BLACK)

            self.movingsprites.draw(self.screen)
            self.current_room.wall_list.draw(self.screen)


            #print("Episode Total Reward:                 ", end="\r", flush=True)
            #print("Episode Total Reward: " + str(self.episode_reward), end="\r", flush=True)
            pygame.display.flip()
            self.clock.tick(580)

    def close (self):
        pygame.quit()

        print("Done :)")











