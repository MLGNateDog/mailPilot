""" mailPilot.py
    Nathan Harris | April 3rd, 2021 """

import pygame, random
pygame.init()

screen = pygame.display.set_mode((800, 480))

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane.png")
        self.rect = self.image.get_rect()

        if not pygame.mixer:
            print("Problem with sound")
        else:
            pygame.mixer.init()
            self.sndYay = pygame.mixer.Sound("Yee.mp3")
            self.sndThunder = pygame.mixer.Sound("Lightning.mp3")
            self.sndEngine = pygame.mixer.Sound("Engine.mp3")
            self.sndEngine.play(-1)

    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 430)
        
class Island(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("island.png")
        self.rect = self.image.get_rect()
        self.reset()

        self.dy = 4

    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.top = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.rect.centery = random.randrange(-500, -300)

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cloud2.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(3, 5)
        self.dx = random.randrange(-1, 1)

class Ocean(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ocean2.gif")
        self.imgage = self.image.convert()
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()

    def update(self):
        self.rect.bottom += self.dy
        if self.rect.top >= 0:
            self.reset()
    def reset(self):
        self.rect.bottom = screen.get_height()


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)

    def update(self):
        self.text = "Lives: %d, Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()

def instructions(score):
    pygame.display.set_caption("Mail Pilot")
    plane = Plane()
    ocean = Ocean()

    allSprites = pygame.sprite.Group(ocean, plane)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Mail Pilot.   Last Score: %d" % score,
    "Instructions: You are a mail pilot,",
    "delivering mail to the islands.",
    "",
    "Fly over an island to drop the mail,",
    "but be careful not to hit the clouds",
    "the plane will fall apart, and you",
    "will lose the game if you hit 5 clouds.",
    "Good luck, have fun!",
    "",
    "Click to start, escape to quit"
    )

    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)

    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()

    plane.sndEngine.stop()
    pygame.mouse.set_visible(True)
    return donePlaying
        
def game():
    pygame.display.set_caption("Mail Pilot")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))


    plane = Plane()
    island = Island()
    cloud1 = Cloud()
    cloud2 = Cloud()
    cloud3 = Cloud()
    ocean = Ocean()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.Group(ocean, island, plane)
    cloudSprites = pygame.sprite.Group(cloud1, cloud2, cloud3)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(60)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True

        #check collisions

        #plane-island collision
        if plane.rect.colliderect(island.rect.inflate(-10, -10)):
            plane.sndYay.play()
            print("plane-island collision")
            island.reset()
            scoreboard.score += 100

        #plane-cloud collisions

        if plane.rect.colliderect(cloud1.rect.inflate(-15, -15)):
            plane.sndThunder.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
                print("Game Over!")
            cloud1.reset()
            print("plane-cloud collision")

        if plane.rect.colliderect(cloud2.rect.inflate(-15, -15)):
            plane.sndThunder.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
                print("Game Over!")
            cloud2.reset()
            print("plane-cloud collision")

        if plane.rect.colliderect(cloud3.rect.inflate(-15, -15)):
            plane.sndThunder.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
                print("Game Over!")
            cloud3.reset()
            print("plane-cloud collision")


        friendSprites.update()
        cloudSprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        cloudSprites.draw(screen)
        scoreSprite.draw(screen)

        pygame.display.flip()

    #stop engine
    plane.sndEngine.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True)
    return scoreboard.score

if __name__ == "__main__":
    main()
