import pygame
import sys

# Initialising Pygame
pygame.init()

# Font for Displaying the High Score
font = pygame.font.Font("freesansbold.ttf", 16)

# Setting Up Colours for the High Score Window!
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 191, 255)


# Functions to append high scores to list & write high scores to the high score file
def write_high_score_file(file_name, your_name, points):
    # Function responsible for opening and writing new high scores to the high core file
    score_file = open(file_name, 'a')
    print(your_name + ",", points, file=score_file)
    score_file.close()


# Function to read high scores from the high score file for display
def read_high_score_file(file_name):
    # Opens and Reads from from the high_score file
    file = open(file_name, 'r')
    high_scores = file.readlines()
    file.close()
    # Variables to score and the high score holders name
    high_score = 0
    highscore_holder_name = ''
    for i in high_scores:
        name, score = i.strip().split(",")
        score = int(score)

        if score > high_score:
            high_score = score
            highscore_holder_name = name
    return highscore_holder_name, high_score


def highscore_holder_input(screen, highscore_holder_name):
    # These variables hold x and y values for the display size
    display_x = 480
    display_y = 100

    # Function for blinking text cursor
    def text_cursor(screen):
        for color in [blue, white]:
            pygame.draw.circle(display_box, color, (display_x // 2, int(display_y * 0.7)), 7, 0)
            screen.blit(display_box, (0, display_y // 2))
            pygame.display.flip()
            pygame.time.wait(300)

    def display_name(screen, name):
        pygame.draw.rect(display_box, white, (50, 60, display_x - 100, 20), 0)
        text_area = font.render(name, True, black)
        text_holder_box = text_area.get_rect(center=(display_x // 2, int(display_y * 0.7)))
        display_box.blit(text_area, text_holder_box)
        screen.blit(display_box, (0, display_y // 2))
        pygame.display.flip()

    display_box = pygame.surface.Surface((display_x, display_y))
    display_box.fill(blue)
    pygame.draw.rect(display_box, black, (0, 0, display_x, display_y), 1)
    txt_surf = font.render(highscore_holder_name, True, black)
    txt_rect = txt_surf.get_rect(center=(display_x // 2, int(display_y * 0.3)))
    display_box.blit(txt_surf, txt_rect)

    player_name = ""
    display_name(screen, player_name)

    # the input-loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pressed_key = event.key
                if pressed_key in [13, 271]:
                    return player_name
                elif pressed_key == 8:
                    player_name = player_name[:-1]
                elif pressed_key <= 300:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT and 122 >= pressed_key >= 97:
                        pressed_key -= 32
                    player_name += chr(pressed_key)

        if player_name == "":
            text_cursor(screen)
        display_name(screen, player_name)


# Function to append all high scores to the list and filter out the top ten
def display_top_ten(screen, file_name):
    # x and y axis display size for the high score list
    display_x = 480
    display_y = 400

    file = open(file_name, 'r')
    high_scores = file.readlines()
    # Empty list to store all high scores
    all_score = []
    # Loops through all high scores looking for the top 10
    for i in high_scores:
        separator = i.index(',')
        name = i[:separator]
        score = int(i[separator + 1:-1])
        all_score.append((score, name))
    all_score.sort(reverse=True)  # sort from largest to smallest
    top_ten = all_score[:10]  # top 10 values

    # Make High Score Display Area and filling in the text
    display_box = pygame.surface.Surface((display_x, display_y))
    display_box.fill(blue)
    pygame.draw.rect(display_box, white, (50, 12, display_x - 100, 35), 0)
    pygame.draw.rect(display_box, white, (50, display_y - 60, display_x - 100, 42), 0)
    pygame.draw.rect(display_box, black, (0, 0, display_x, display_y), 1)
    text_area = font.render("HIGH-SCORE", True, black)
    text_holder_box = text_area.get_rect(center=(display_x // 2, 30))
    display_box.blit(text_area, text_holder_box)
    text_area = font.render("Press ENTER to continue", True, black)
    text_holder_box = text_area.get_rect(center=(display_x // 2, 360))
    display_box.blit(text_area, text_holder_box)

    # writing the top 10 list data to the display holder box
    for i, j in enumerate(top_ten):
        text_area = font.render(j[1] + "  " + str(j[0]), True, black)
        text_holder_box = text_area.get_rect(center=(display_x // 2, 30 * i + 60))
        display_box.blit(text_area, text_holder_box)

    screen.blit(display_box, (0, 0))
    pygame.display.flip()

    while True:  # wait for user to acknowledge and return
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                return
        pygame.time.wait(20)


# Function controlling evaluation and storage if high scores in the high score file
def highscore(screen, score_file, player_score):
    high_name, high_score = read_high_score_file(score_file)

    # If player score is more than the current high score...
    if player_score > high_score:
        # Enter Name...
        player_name = highscore_holder_input(screen, "CONGRATULATIONS!\n You have Beaten the High Score!\n "
                                                     "\nEnter your Name: ")
    # If player score is more than the current high score...
    elif player_score == high_score:
        # Enter Name...
        player_name = highscore_holder_input(screen, "CONGRATULATIONS! You have equalled the High Score!\n "
                                                     "Enter your Name: ")
    # If player score is less than high score
    elif player_score < high_score:
        # Displays current high score...
        score_text = "Current HighScore: " + str(high_score) + '\n' + "Scored By: " + high_name + '\n' + "Enter your Name: "
        player_name = highscore_holder_input(screen, score_text)

    # Checks if player name entered is empty... If so...
    if player_name is None or len(player_name) == 0:
        # Do not write to file
        return
    # If name entered is valid... We write the Player's Name and New Player High Score to the list
    write_high_score_file(score_file, player_name, player_score)
    # Filters the top ten (from a potentially large list) in the score file for display
    display_top_ten(screen, score_file)
    return
