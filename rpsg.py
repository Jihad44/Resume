import pygame
from sys import exit
import random

GAME_WIDTH = 640
GAME_HEIGHT = 360

pygame.font.init()

# player hand
player_x = 0
player_y = GAME_HEIGHT/2
player_width = 34
player_height = 24

# npc hand
npc_x = GAME_WIDTH-251+23
npc_y = GAME_HEIGHT/2
npc_width = 34
npc_height = 24

# load image
background_image = pygame.image.load("background.png")
player_rock = pygame.image.load("player_rock.png")
player_rock_rect = player_rock.get_rect(topleft=(player_x, player_y))
player_paper = pygame.image.load("player_paper.png")
player_scissor = pygame.image.load("player_scissor.png")
rock = pygame.image.load("rock_button.png")
paper = pygame.image.load("paper_button.png")
scissor = pygame.image.load("scissor_button.png")
rock_rect = rock.get_rect(topleft=(190, 90))
paper_rect = paper.get_rect(topleft=(GAME_WIDTH-235, 90))
scissor_rect = scissor.get_rect(topleft=(298, 90))
select = pygame.image.load("select.png")
start_button = pygame.image.load("start.png")
start_rect = start_button.get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2))
npc_rock = pygame.transform.flip(player_rock, True, False)
npc_rock_rect = npc_rock.get_rect(topleft=(npc_x, npc_y))
npc_paper = pygame.transform.flip(player_paper, True, False)
npc_scissor = pygame.transform.flip(player_scissor, True, False)


# ingame define
player_health = 3
npc_health = 3
player_pick = 0
npc_pick = 0
start = False
timer = 0
up = False
loop = 0
decrease_health = 0
finish = False


def draw():
    global rock_rect, paper_rect, scissor_rect, player_health, npc_health
    window.blit(background_image, (0, 0))
    text_font = pygame.font.SysFont("Comic Sans MS", 20)
    if loop < 3 or player_pick == 1:
        window.blit(player_rock, player_rock_rect)
    if loop < 3 or npc_pick == 1:
        window.blit(npc_rock, npc_rock_rect)
    if loop == 3:
        if player_pick == 2:
            window.blit(player_paper, (player_x, player_y))
        if player_pick == 3:
            window.blit(player_scissor, (player_x, player_y))
        if npc_pick == 2:
            window.blit(npc_paper, (npc_x, npc_y))
        if npc_pick == 3:
            window.blit(npc_scissor, (npc_x, npc_y))
    if loop == 3:
        if player_pick == npc_pick:
            text_str = "you draw"
        elif ((player_pick == 1 and npc_pick == 3) or (player_pick == 2 and npc_pick == 1) or (player_pick == 3 and npc_pick == 2)):
            text_str = "you win"
        else:
            text_str = "you lose"
        text_render = text_font.render(text_str, True, "yellow")
        text_rect = text_render.get_rect(
            center=(GAME_WIDTH/2, GAME_HEIGHT/2))
        window.blit(text_render, text_rect)
    player_health_text = f"Your Health = {player_health}\nEnemy's Health = {npc_health}"
    player_health_render = text_font.render(
        player_health_text, True, "yellow")
    player_health_rect = player_health_render.get_rect(topleft=(3, 3))
    window.blit(player_health_render, player_health_rect)
    if not start:
        window.blit(rock, rock_rect)
        window.blit(paper, paper_rect)
        window.blit(scissor, scissor_rect)
        window.blit(start_button, start_rect)
    if player_pick == 1 and not start:
        window.blit(select, (175, 75))
    if player_pick == 2 and not start:
        window.blit(select, (GAME_WIDTH-250, 75))
    if player_pick == 3 and not start:
        window.blit(select, (283, 75))
    if finish:
        if player_health == 0:
            finish_render = text_font.render("you lose", True, "red")
        if npc_health == 0:
            finish_render = text_font.render("you win", True, "green")
        finish_rect = player_health_render.get_rect(
            topleft=(3, 55))
        window.blit(finish_render, finish_rect)


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissor")
clock = pygame.time.Clock()

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if rock_rect.collidepoint(event.pos):
                player_pick = 1
            if paper_rect.collidepoint(event.pos):
                player_pick = 2
            if scissor_rect.collidepoint(event.pos):
                player_pick = 3
            if start_rect.collidepoint(event.pos):
                if player_pick > 0:
                    start = True
                    up = True
                    npc_pick = random.randint(1, 3)
    if start:
        dt = clock.tick(60)
        timer += dt
        interval = 60
        if loop < 3:
            if timer >= interval:
                if up:
                    if player_rock_rect.y > player_y - 75:
                        player_rock_rect.y -= 5
                        npc_rock_rect.y -= 5
                        timer = 0
                    else:
                        up = False
                if not up:
                    if player_rock_rect.y < player_y:
                        player_rock_rect.y += 5
                        npc_rock_rect.y += 5
                        timer = 0
                    else:
                        up = True
                        loop += 1
        if loop == 3:
            if timer >= interval+2000:
                up = False
                start = False
                loop = 0
                if player_pick == npc_pick:
                    player_pick = 0
                    npc_pick = 0
                elif ((player_pick == 1 and npc_pick == 3) or (player_pick == 2 and npc_pick == 1) or (player_pick == 3 and npc_pick == 2)):
                    decrease_health = 1
                    player_pick = 0
                    npc_pick = 0
                else:
                    decrease_health = 2
                    player_pick = 0
                    npc_pick = 0
    if decrease_health == 1:
        npc_health -= 1
        decrease_health = 0
    if decrease_health == 2:
        player_health -= 1
        decrease_health = 0
    if player_health == 0 or npc_health == 0:
        finish = True
    draw()
