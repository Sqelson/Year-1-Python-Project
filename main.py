# Main Python Project File.
# A space invaders type side scroller.

# Import Modules.
import sys
import pygame
import random
import pygame.surface

# Initialise pygame.
pygame.init()

# Initialise constant variables.
clock = pygame.time.Clock()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Colours are all here.
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
yellow = 255, 255, 0
green = 0, 255, 0
blue = 0, 0, 255
orange = 255, 165, 0
pink = 255, 192, 203
purple = 128, 0, 128


# The player class.
class Player:
    # The initialising method.
    def __init__(self, colour, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.direction = None
        self.speed = 5

    # The move method with left and right attributes, the self.direction can be accessed as it is in the same class.
    # Note this also bounces the player back the other way when reaching the sides of the screen.
    def move(self):
        if self.direction == 'Left':
            self.rect.x = self.rect.x - self.speed
            if self.rect.x < 0:
                self.direction = 'Right'
        if self.direction == 'Right':
            self.rect.x = self.rect.x + self.speed
            if self.rect.x > 590:
                self.direction = 'Left'

    # The collision method.
    def collide(self, other_rect):
        # This will return true if self collides with the other_rect.
        return self.rect.colliderect(other_rect)

    # The draw method, which draws the square onto the screen, with its assigned colour and rect (dimensions).
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


# The enemy class.
class Enemy:
    # The initialising method.
    def __init__(self, colour, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.direction = None
        self.speed = 3

    # The move method that allows enemy's to go down the screen, which is all that's required (with more time this
    # could be improved)
    def move(self):
        if self.direction == 'Down':
            self.rect.y = self.rect.y + self.speed

    # The collision method.
    def collide(self, other_rect):
        # This will return true if self collides with the other_rect.
        return self.rect.colliderect(other_rect)

    # The draw method, which draws the square onto the screen, with its assigned colour and rect (dimensions).
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


# The projectile class.
class Projectile:
    # The initialising method.
    def __init__(self, colour, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.speed = 10
        self.direction = None

    # The move method that allows projectiles to go up or down the screen, which is all that's required (with more
    # time this could be improved).
    def move(self):
        if self.direction == 'Up':
            self.rect.y = self.rect.y - self.speed
        if self.direction == 'Down':
            self.rect.y = self.rect.y + self.speed

    # The collision method.
    def collide(self, other_rect):
        # This will return true if self collides with the other_rect.
        return self.rect.colliderect(other_rect)

    # The draw method, which draws the square onto the screen, with its assigned colour and rect (dimensions).
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


# Set up the various lists to be used in the program.
player_projectiles = []
enemy_projectiles = []
enemies = []
player = []


# The main program loop.
def main():
    # Create the player and append it to the player list.
    p1 = Player(blue, 295, 400, 50, 50)
    player.append(p1)
    # Set the score initially to 0, and set the font to comic sans for labels.
    score = 0
    # Set the font style and font size for in-game.
    main_font = pygame.font.SysFont("comicsans", 35)
    # While done is false, the game loop continues.
    done = False

    while not done:
        # If the program detects a quit action, it sets done to true, ending the while loop and ending the program.
        for event in pygame.event.get():
            # This is here to detect key presses.
            if event.type == pygame.KEYDOWN:
                if event.key == 97:  # The A Key, to go left.
                    p1.direction = 'Left'
                elif event.key == 100:  # The D Key, to go right.
                    p1.direction = 'Right'
                elif event.key == 32:  # The Space Bar, to fire a projectile up.
                    # The spawn point of the projectile is defined as the middle of the player object.
                    projectile_spawn = p1.rect.x + p1.rect.width / 2 - 2.5
                    # It is then given its properties, and appended to the player_projectiles list.
                    pp = Projectile(orange, projectile_spawn, p1.rect.y, 5, 15)
                    pp.direction = 'Up'
                    pp.speed = 10
                    player_projectiles.append(pp)

        # The function to clear the screen. It is place near the top of main() so it wipes everything first.
        def clear_screen():
            enemies.remove(e)
            player.remove(p1)
            for _ in enemies:
                enemies.clear()
            for _ in player:
                player.clear()
            for _ in player_projectiles:
                player_projectiles.clear()
            for _ in enemy_projectiles:
                enemy_projectiles.clear()

        # The high score function writes to the highscore text file if the most recent score is higher than the
        # current on in the text file.
        def high_score():
            # Opens the highscore file in read mode, reads all the lines in as a list and get the first line of the
            # file.
            f = open('highscore.txt', 'r')
            file = f.readlines()
            last = int(file[0])

            # Then if the current score is greater than the previous highest score, the file is re-opened in write mode.
            # From there the new best score is written in and the file is saved and closed.
            if last < int(score):
                f.close()
                file = open('highscore.txt', 'w')
                file.write(str(score))
                file.close()

        # Collision checking for player projectiles hitting the enemy.
        for pp in player_projectiles:
            for e in enemies:
                # If the player projectile collides with an enemy...
                if pp.collide(e.rect):
                    # ...Remove both the enemy and player projectile and add to the score.
                    enemies.remove(e)
                    player_projectiles.remove(pp)
                    score += 10

        # Collision checking for enemy projectiles hitting the player.
        for ep in enemy_projectiles:
            for p1 in player:
                # If the enemy projectile collides with the player...
                if ep.collide(p1.rect):
                    # ...clear the screen and set done to True, so the game loop is ended and return to main menu.
                    high_score()
                    clear_screen()
                    done = True

        # Collision checking for enemies colliding with the player..
        for p1 in player:
            for e in enemies:
                # If an enemy itself collides with the player...
                if e.collide(p1.rect):
                    # ...clear the screen and set done to True, so the game loop is ended and return to main menu.
                    high_score()
                    clear_screen()
                    done = True

        # Player projectiles that go out of the windows bounds are removed.
        for pp in player_projectiles:
            if pp.rect.y < 0:
                player_projectiles.remove(pp)

        # Enemies that go out of the windows bounds are removed.
        for e in enemies:
            if e.rect.y > 480:
                enemies.remove(e)

        # Enemy projectiles that go out of the windows bounds are removed.
        for ep in enemy_projectiles:
            if ep.rect.y > 480:
                enemy_projectiles.remove(ep)

        # Update the game objects in motion.
        p1.move()  # Move the player.

        # Ensure the projectiles move.
        for pp in player_projectiles:
            pp.move()

        for ep in enemy_projectiles:
            ep.move()

        # Ensure the enemies move.
        for e in enemies:
            e.move()

        # Spawn in the enemies and make them move.
        if random.randint(1, 100) == 1:
            s = random.randint(0, screen_width - 40)
            e = Enemy(green, s, -40, 40, 40)
            e.direction = 'Down'
            enemies.append(e)

        # The screen is filled with a black background.
        screen.fill(black)

        # Setup the lives label as equal to the current score and add it to the screen in the top left.
        lives_label = main_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(lives_label, (0, 0))

        # Draw the projectiles and player and enemy objects on the screen.
        for pp in player_projectiles:
            pp.draw(screen)
        for ep in enemy_projectiles:
            ep.draw(screen)
        for e in enemies:
            e.draw(screen)
        for p1 in player:
            p1.draw(screen)

        # Draw all the aliens and give them a chance to shoot!
        for enemy in enemies:
            enemy.draw(screen)
            # Aliens shoot randomly.
            # 0.1 percent change per frame that an alien shoots.
            if random.randint(1, 1000) < 10:
                projectile_spawn = enemy.rect.x + enemy.rect.width / 2 - 2.5
                ep = Projectile(red, projectile_spawn, enemy.rect.y, 5, 15, )
                ep.direction = 'Down'
                ep.speed = 10
                enemy_projectiles.append(ep)

        # This ensures the entire screen is updated.
        pygame.display.flip()

        # Sets the FPS to 60.
        clock.tick(60)


def main_menu():
    # Set the font style and font size for the main menu.
    menu_font = pygame.font.SysFont("comicsans", 35)
    done = False
    while not done:
        # Fill the screen with black.
        screen.fill(black)

        # Set up the different labels to appear.
        title_label = menu_font.render("Welcome to my Space Invaders Type Game!", True, (255, 255, 255))
        play_label = menu_font.render("Press the E key to Play.", True, (255, 255, 255))
        leaderboard_label = menu_font.render("Press the H key to view the leaderboard.", True, (255, 255, 255))
        exit_label = menu_font.render("Press the ESC key to exit.", True, (255, 255, 255))

        # Use said labels and apply them to the pygame screen, they are all centred.
        screen.blit(title_label, (screen_width / 2 - title_label.get_width() / 2, 0))
        screen.blit(play_label, (screen_width / 2 - play_label.get_width() / 2, 151.66))
        screen.blit(leaderboard_label, (screen_width / 2 - leaderboard_label.get_width() / 2, 303.33))
        screen.blit(exit_label, (screen_width / 2 - exit_label.get_width() / 2, 455))

        # Update the display.
        pygame.display.flip()

        # Check what keys are pressed on the main menu and do an action accordingly.
        menu_keys = pygame.key.get_pressed()
        for _ in pygame.event.get():
            # Pressing E starts the game.
            if menu_keys[pygame.K_e]:
                main()
            # Pressing H brings up the leaderboard.
            if menu_keys[pygame.K_h]:
                high_score()
            # Pressing ESC quits the game.
            if menu_keys[pygame.K_ESCAPE]:
                sys.exit()


def high_score():
    # Set the font style and font size for the leaderboard.
    leaderboard_font = pygame.font.SysFont("comicsans", 35)
    high_score_font = pygame.font.SysFont("comicsans", 105)

    # This function simply gets the current high score to be displayed in the screen.
    def get_score():
        f = open('highscore.txt', 'r')
        file = f.readlines()
        last = int(file[0])
        return last

    while True:

        # Fill the screen with black.
        screen.fill(black)

        # Set up the different labels to appear.
        title_label = leaderboard_font.render("Leaderboard.", True, (255, 255, 255))
        score_label = high_score_font.render("High Score is: " + str(get_score()), True, (255, 255, 255))
        exit_label = leaderboard_font.render("Press the B key to go back.", True, (255, 255, 255))

        # Use said labels and apply them to the pygame screen, they are all centred.
        screen.blit(title_label, (screen_width / 2 - title_label.get_width() / 2, 0))
        screen.blit(score_label, (screen_width / 2 - score_label.get_width() / 2, 200))
        screen.blit(exit_label, (screen_width / 2 - exit_label.get_width() / 2, 455))

        # Update the display.
        pygame.display.flip()

        # Check what keys are pressed on the main menu and do an action accordingly.
        ldb_keys = pygame.key.get_pressed()
        for _ in pygame.event.get():
            # Pressing B goes back to the main menu.
            if ldb_keys[pygame.K_b]:
                main_menu()


# Ensure the main menu is run at the end of the code, meaning the only way to exit is pressing ESC in the main menu.
main_menu()
