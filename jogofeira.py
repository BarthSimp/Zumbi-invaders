import pygame
import random
import math
import time

# Inicializando o Pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Dimensões da tela
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Tiro Top-Down")

# Carregar e redimensionar imagens
player_img = pygame.image.load("topdown.png")
enemy_img = pygame.image.load("zumbi.png")
bullet_img = pygame.image.load("pixil-frame-0.png")
background_img = pygame.image.load("fundo.png")  # Adicionando imagem do fundo

player_img = pygame.transform.scale(player_img, (60, 60))  # Ajuste o tamanho do jogador
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # Ajuste o tamanho do inimigo
bullet_img = pygame.transform.scale(bullet_img, (8, 16))  # Ajuste o tamanho do projétil
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Ajusta a imagem do fundo

player_size = player_img.get_rect().size
enemy_size = enemy_img.get_rect().size
bullet_size = bullet_img.get_rect().size

# Jogador
player_pos = [WIDTH // 2, HEIGHT - player_size[1] - 10]
player_speed = 15
player_health = 100

# Inimigos
enemy_speed = 2
enemy_list = []

# Projéteis
bullet_speed = 15
bullet_list = []
last_shot_time = 0
shoot_delay = 0.0
current_bullets = 20

# Hordas
horde_count = 1
max_horde = 5
zombie_count = [7, 13, random.randint(15, 20), random.randint(18, 25), random.randint(20, 30)]
ammo_count = [20, 26, random.randint(30, 40), random.randint(35, 45), random.randint(40, 50)]
kills_to_next_horde = [3, 6, 9, 12, 15]  # Quantidade de zumbis que devem ser mortos por horda

# Contagem de zumbis eliminados
zombies_killed = 0

# Estados do jogo
game_active = False
game_over = False
game_won = False

# Função para criar inimigos aleatoriamente
def create_enemy():
    while len(enemy_list) < zombie_count[horde_count - 1]:  # Certifica-se de que a quantidade correta de zumbis seja criada
        x_pos = random.randint(0, WIDTH - enemy_size[0])
        y_pos = 0
        enemy_list.append([x_pos, y_pos])  # Adiciona o inimigo à lista

# Função para desenhar o jogador
def draw_player():
    screen.blit(player_img, (player_pos[0], player_pos[1]))

# Função para desenhar inimigos
def draw_enemies():
    for enemy_pos in enemy_list:
        screen.blit(enemy_img, (enemy_pos[0], enemy_pos[1]))

# Função para desenhar projéteis
def draw_bullets():
    for bullet_pos in bullet_list:
        screen.blit(bullet_img, (bullet_pos[0], bullet_pos[1]))

# Função para desenhar a barra de vida
def draw_health_bar():
    pygame.draw.rect(screen, RED, [10, 10, 200, 20])
    pygame.draw.rect(screen, GREEN, [10, 10, player_health * 2, 20])

# Função para desenhar o contador de hordas
def draw_horde_counter():
    font = pygame.font.Font(None, 36)
    draw_text(f'Horda: {horde_count}/{max_horde}', font, WHITE, screen, WIDTH // 2, 40)

# Função para desenhar munições
def draw_ammo_counter():
    font = pygame.font.Font(None, 36)
    draw_text(f'Munições: {current_bullets}', font, WHITE, screen, WIDTH // 2, 70)

# Função para desenhar a contagem de zumbis mortos
def draw_zombies_killed():
    font = pygame.font.Font(None, 36)
    draw_text(f'Zumbis Eliminados: {zombies_killed}/{kills_to_next_horde[horde_count - 1]}', font, WHITE, screen, WIDTH // 2, 100)

# Função para desenhar mensagem
def draw_message(message):
    font = pygame.font.Font(None, 74)
    draw_text(message, font, WHITE, screen, WIDTH // 2, HEIGHT // 2)

# Função para mover os inimigos
def move_enemies():
    for enemy_pos in enemy_list:
        enemy_pos[1] += enemy_speed

# Função para mover os projéteis
def move_bullets():
    for bullet_pos in bullet_list:
        bullet_pos[1] -= bullet_speed

# Função para verificar colisões
def detect_collision(obj1_pos, obj2_pos, obj1_size, obj2_size):
    dx = obj1_pos[0] - obj2_pos[0]
    dy = obj1_pos[1] - obj2_pos[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance < (obj1_size[0] / 2 + obj2_size[0] / 2):
        return True
    return False

# Função para exibir texto na tela
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Tela inicial
def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    draw_text("Jogo de Tiro Top-Down", font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
    draw_text("Pressione qualquer tecla para iniciar", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    wait_for_input()

# Tela de game over
def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    draw_text("Game Over", font, RED, screen, WIDTH // 2, HEIGHT // 3)
    draw_text("Pressione qualquer tecla para reiniciar", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    wait_for_input()

# Tela de vitória da horda
def victory_screen():
    screen.fill(BLACK)
    draw_message(f"Horda {horde_count -1} Vencida!")
    pygame.display.update()
    wait_for_input()

# Tela de vitória final
def game_won_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    draw_text("Você Venceu Todas as Hordas!", font, GREEN, screen, WIDTH // 2, HEIGHT // 3)
    draw_text("Pressione qualquer tecla para sair", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    wait_for_input()

# Função para aguardar entrada do jogador
def wait_for_input():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Função para reiniciar o jogo
def reset_game():
    global player_pos, enemy_list, bullet_list, game_active, game_over, current_bullets, player_health, zombies_killed
    player_pos = [WIDTH // 2, HEIGHT - player_size[1] - 10]
    enemy_list = []
    bullet_list = []
    current_bullets = ammo_count[horde_count - 1]  # Atualiza munições para a horda atual
    player_health = 100
    zombies_killed = 0  # Reset da contagem de zumbis eliminados
    game_active = True
    create_enemy()  # Certifica-se de que os zumbis sejam criados ao reiniciar a horda


# Loop principal
running = True
clock = pygame.time.Clock()

# Tela inicial antes de iniciar o jogo
start_screen()

while running:
    screen.blit(background_img, (0, 0))  # Desenha o fundo na tela
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_bullets > 0:  # Verifica se há munição
                if time.time() - last_shot_time > shoot_delay:
                    bullet_pos = [player_pos[0] + player_size[0] // 2 - bullet_size[0] // 2, player_pos[1]]
                    bullet_list.append(bullet_pos)
                    current_bullets -= 1  # Diminui munição
                    last_shot_time = time.time()

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size[0]:
        player_pos[0] += player_speed
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size[1]:
        player_pos[1] += player_speed

    # Criar inimigos no início da horda, se necessário
    if len(enemy_list) == 0:
        create_enemy()

    # Mover inimigos e projéteis
    move_enemies()
    move_bullets()

    # Desenhar jogador, inimigos, projéteis, barra de vida e contador de hordas
    draw_player()
    draw_enemies()
    draw_bullets()
    draw_health_bar()
    draw_horde_counter()
    draw_ammo_counter()
    draw_zombies_killed()

    # Verificar colisões
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos, player_size, enemy_size):
            player_health -= 10
            if player_health <= 0:
                game_over = True
        for bullet_pos in bullet_list:
            if detect_collision(bullet_pos, enemy_pos, bullet_size, enemy_size):
                bullet_list.remove(bullet_pos)
                enemy_list.remove(enemy_pos)
                zombies_killed += 1  # Incrementa zumbis mortos
                if zombies_killed >= kills_to_next_horde[horde_count - 1]:  # Verifica se matou zumbis suficientes
                    horde_count += 1
                    if horde_count > max_horde:
                        game_won = True
                    else:
                        victory_screen()  # Exibe tela de vitória da horda
                        reset_game()

    if game_over:
        game_over_screen()
        reset_game()

    if game_won:
        game_won_screen()
        running = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()
