import pygame
import random
import math
from pygame import mixer

pygame.init()

# width, height of the Window-Screen
screen = pygame.display.set_mode((800, 600))
# Load Background image
Background = pygame.image.load('starfield.png')

# Set Caption of Window
pygame.display.set_caption("Space-Shooting Game")

# Load icon image(Icon of the Window which will show in top left corner)
icon = pygame.image.load('spaceship.png')

# For Display the icon
pygame.display.set_icon(icon)

# background Music
mixer.music.load('background.wav')

# by doing -1 music will play in loop until we Exit the Game
mixer.music.play(-1)

# Spaceship
shooterImg = pygame.image.load('spaceship64.png')

# Starting position of the Space ship
# X Coordinate of Space ship (from Left)
shooterX = 360
# Y Coordinate of Space ship (from Top)
shooterY = 480+32
#512

# For storing new position of the space ship(after Moving)
ChangeSX = shooterX
ChangeSY = shooterY
# Speed of Space Ship (6 px)
speedS = 6

# Enemies
EnemyImg = pygame.image.load('enemy.ico')

# For Storing Y Co-ordinate of enemy
EnemyY = []
# For Storing X Co-ordinate of enemy
EnemyX = []
# For Storing Changing Speed of enemy
ChangeEx = []
ChangeEy = []
# Number of Enemy
num_of_Enemy = 20

# For Generate(Randomly) the X and Y coordinate of Enemy and Changing Speed in X(Left/Right) and Y axis(Down)
for i in range(num_of_Enemy):
    EnemyY.append(random.randint(50, 150))
    EnemyX.append(random.randint(0, 735))
    ChangeEx.append(4)
    ChangeEy.append(40)

# Load the Bullet Image
BulletImg = pygame.image.load('bullet.png')
# For Storing the instance of the bullet Object
bullets = []


# For storing the state of the Bullets and Add and remove multiple Bullets
class Bullet:
    bulletX = 0
    # Here BulletY is Always Because our Space Ship is at  512 px (480 + 32)
    bulletY = 480
    bulletX_change = 0
    # Changing Speed of Bullet in Y Axis (10 px)
    bulletY_change = 10

    # bx is Starting Position of Bullet
    def __init__(self, bx):
        self.bulletX = bx

    def fire_bullet(self, Index):
        # if Our Bullet is 10px far from Top then it will Disappeared (Pop from the bullets List)
        if self.bulletY - 10 <= 0:
            bullets.pop(Index)
            return
        self.bulletY -= self.bulletY_change
        screen.blit(BulletImg, (self.bulletX + 27, self.bulletY))
        pass
    pass


# For Storing The Score Value
score_val = 0
# For Creating instance of Boldfinger 32 px font
font = pygame.font.Font('Boldfinger.ttf', 32)

textX = 10
textY = 10

# For Creating instance of  Boldfinger 64 px font
over_font = pygame.font.Font('Boldfinger.ttf', 64)


# For Render and Printing the Score Value on top left Corner of the Screen
def show_score():
    # Render the Font
    score = font.render("Score : " + str(score_val), True, (255, 235, 225))
    # Printing on the Window at Location (10, 10) px from Top of the Screen
    screen.blit(score, (textX, textY))


def game_over_text():
    # Render the Font
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    # Printing on the Window at Location (250, 250) px from Top of the Screen
    screen.blit(over_text, (200, 250))


# Drawing Shooter
def shooter(x, y):
    screen.blit(shooterImg, (x, y))
    pass


# Checking Collision Between Enemy and the Bullet
def isCollision(enemyX, enemyY):
    for j, b in enumerate(bullets):
        # Calculate Distance Between Bullet and enemy
        distance = math.sqrt(((enemyX - b.bulletX) ** 2) + ((enemyY - b.bulletY) ** 2))
        # if distance is Less than or Equal to 29 px then Our enemy will Kill(Disappear) and Respawn Between 50
        # and 150px and Bullet Will Pop from bullets list
        if distance <= 29:
            bullets.pop(j)
            return True
        else:
            return False


# Drawing Enemy
def enemy(x, y):
    screen.blit(EnemyImg, (x, y))
    pass


# For Moving Enemy
def moveEnemy():
    for i in range(num_of_Enemy):
        # For Checking Game Over Condition
        if EnemyY[i] > 480:
            # this is for disappearing all enemy
            for j in range(num_of_Enemy):
                EnemyY[j] = 2000
            game_over_text()
            break
        # if Our Enemy is Moving Towards Right(Ex > 0)
        if ChangeEx[i] > 0:
            # Checking Boundary Condition
            if ChangeEx[i] + EnemyX[i] + 48 <= 800:
                EnemyX[i] += ChangeEx[i]
            else:
                # if Enemy hit Right Border Then ...
                ChangeEx[i] *= -1
                EnemyX[i] += ChangeEx[i]
                EnemyY[i] += ChangeEy[i]
        else:
            # if Our Enemy is Moving Towards Left
            # Checking Boundary Condition
            if EnemyX[i] - ChangeEx[i] >= 0:
                EnemyX[i] += ChangeEx[i]
            else:
                # if Enemy hit left Border Then ...
                ChangeEx[i] *= -1
                EnemyX[i] += ChangeEx[i]
                EnemyY[i] += ChangeEy[i]


running = True

while running:

    for event in pygame.event.get():
        # if User Click on the quit button
        if event.type == pygame.QUIT:
            running = False

        # Key Down event
        if event.type == pygame.KEYDOWN:
            # if Space key is press than
            if event.key == pygame.K_SPACE:
                # Creating instance of Bullet and Store it in the bullets list
                bullets.append(Bullet(ChangeSX))
                # mixer.sound because we have to play this sound many times and
                # Pygame only supports one Music at a time but we can have several Sound objects playing at once
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()

    # List of All key Pressed
    key = pygame.key.get_pressed()

    # if User Press right arrow button and if Our Space Ship not touch at the right Corner
    if key[pygame.K_RIGHT] and ChangeSX + 64 + speedS <= 800:
        ChangeSX += speedS
        pass

    # if User Press left arrow button and if Our Space Ship not touch at the left Corner
    if key[pygame.K_LEFT] and ChangeSX - speedS >= 0:
        ChangeSX -= speedS
        pass

    # Display the BackGround image From (0 px, 0 px)
    screen.blit(Background, (0, 0))

    # Fire Our all Bullet(Progress the position of the all bullets)
    for index, bullet in enumerate(bullets):
        bullet.fire_bullet(index)

    #  Checking all bullet Collision with All enemy
    for i in range(num_of_Enemy):
        collision = isCollision(EnemyX[i], EnemyY[i])
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            score_val += 1
            # print(score)
            EnemyY[i] = random.randint(50, 150)
            EnemyX[i] = random.randint(0, 735)
        # display all enemy
        enemy(EnemyX[i], EnemyY[i])

    # Display the Space Ship
    shooter(ChangeSX, ChangeSY)
    # Move All enemy
    moveEnemy()
    # Show(Display) Score
    show_score()
    # Update the Screen and Show in the Screen
    pygame.display.update()
    pass
