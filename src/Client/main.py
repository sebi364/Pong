import pygame
from math import dist, sqrt
from pygame.math import Vector2
import time
# Settings
screen_res = (1920, 1080)

border_width = 5
border_color = "White"

ball_color = "purple"
ball_radius = 40

background_color = "#232323"

# Variables
borders = []
ball = ""

# Classes
class Wall:
    def __init__(self,p1,p2,color,width):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.width = width
        self.length = dist(self.p1, self.p2)

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.p1, self.p2, self.width)
    
    def is_colliding(self, pT):
        # Chack distance to ball src=https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
        distance = abs(((self.p2[0]-self.p1[0])*(self.p1[1]-pT[1])) - ((self.p1[0]-pT[0])*(self.p2[1]-self.p1[1]))) / sqrt((self.p2[0]-self.p1[0])**2 + (self.p2[1]-self.p1[1])**2)
        
        if round(distance) <= ball_radius:
            #check on what side of the line the ball is src=https://math.stackexchange.com/questions/274712/calculate-on-which-side-of-a-straight-line-is-a-given-point-located
            side = (((pT[0]-self.p1[0])*(self.p2[1]-self.p1[1]))         -        ((pT[1]-self.p1[1])*(self.p2[0]-self.p1[0])))
            if side > 0:
                side = 1
            if side < 0:
                side = -1
            
            #calculate line normal src=
            distance = [self.p1[0] - self.p2[0], self.p1[1] - self.p2[1]]
            norm = sqrt(distance[0] ** 2 + distance[1] ** 2)
            wall_direction = Vector2(distance[0] / norm, distance[1] / norm).rotate(90*side)
            return(True,wall_direction)
        else:
            return(False,0)

class Ball:
    def __init__(self, pos, color, radius, vector):
        self.pos = pos
        self.color = color
        self.radius = radius
        self.vector = Vector2(1, 0)

    def draw(self, screen):
        self.pos += self.vector
        pygame.draw.circle(screen,self.color,self.pos,self.radius)

# Functions
## Parser for the game maps
def map_parser(map):
    global ball
    map_file = open(f"Maps/{map}.txt")
    map_content = map_file.read().split("\n")
    for i in map_content:
        i = i.split("=")
        if i[0] == "Name":
            pygame.display.set_caption(f"Pong! {i[1]}")

        if i[0] == "Wall":
            j = i[1].split(",")
            points = []

            for k in j:
                p1_x, p1_y = k.split(":")
                points.append((int(p1_x),int(p1_y)))
            x = Wall(points[0],points[1],border_color,border_width)
            borders.append(x)
        
        if i[0] == "Ball":
            j = i[1].split(",")
            p_x, p_y = j[0].split(":")
            pos = (int(p_x),int(p_y))
            ball = Ball(pos, ball_color, ball_radius, 1)

# Start Pygame
pygame.init()
screen = pygame.display.set_mode(screen_res)
pygame.display.set_caption("Pong!")
running = True

# Load Map
map_parser("square")

while running:
    screen.fill(background_color)
    for x in borders:
        x.draw(screen)
        collide, wall_vector = x.is_colliding(ball.pos)
        if collide == True:
            ball.vector = ball.vector + wall_vector
    ball.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False