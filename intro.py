import random

WIDTH = 800
HEIGHT = 700

# Estados do jogo
MENU = "menu"
JOGO = "jogo"
MORTE = "morte"
estado = MENU

# Player e inimigo
player = Actor("alien", (WIDTH//2, HEIGHT//2))
inimigos = []
velocidade = 3

# Botão do menu
botao_jogar = Rect((WIDTH//2 - 100, HEIGHT//2 - 40), (200, 50))

# Sons
musica_menu = "menu_music"
musica_jogo = "game_music"

# Função para resetar o jogo
def iniciar_jogo():
    global estado, player, inimigos
    estado = JOGO
    player.pos = (WIDTH//2, HEIGHT//2)
    inimigos.clear()
    for _ in range(3):
        spawn_inimigo()
    

# Cria inimigos em posições aleatórias
def spawn_inimigo():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    inimigo = Actor("inimigo", (x, y))
    inimigos.append(inimigo)

def draw():
    screen.clear()

    if estado == MENU:
        screen.fill((30, 30, 30))
        screen.draw.text("ROGUELIKE SLIME", center=(WIDTH//2, 100), fontsize=60, color="white")
        screen.draw.filled_rect(botao_jogar, (0, 150, 0))
        screen.draw.text("JOGAR", center=botao_jogar.center, fontsize=40, color="white")
        

    elif estado == JOGO:
        player.draw()
        for inimigo in inimigos:
            inimigo.draw()

    elif estado == MORTE:
        screen.fill((0, 0, 0))
        screen.draw.text("VOCÊ MORREU!", center=(WIDTH//2, HEIGHT//2 - 30), fontsize=60, color="red")
        screen.draw.text("Pressione qualquer tecla para voltar ao menu", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color="white")

def update():
    if estado == JOGO:
        mover_player()
        mover_inimigos()
        checar_colisoes()

def mover_player():
    if keyboard.left:
        player.x -= velocidade
    if keyboard.right:
        player.x += velocidade
    if keyboard.up:
        player.y -= velocidade
    if keyboard.down:
        player.y += velocidade

def mover_inimigos():
    for inimigo in inimigos:
        dx = player.x - inimigo.x
        dy = player.y - inimigo.y
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        inimigo.x += velocidade * 0.5 * dx / dist
        inimigo.y += velocidade * 0.5 * dy / dist

def checar_colisoes():
    global estado
    for inimigo in inimigos:
        if player.colliderect(inimigo):
            estado = MORTE
            sounds.eep.play()
                
            break

def on_mouse_down(pos, button):
    global estado
    if estado == MENU and botao_jogar.collidepoint(pos):
        iniciar_jogo()
        
    if player.collidepoint(pos):
        sounds.eep.play()
        
    if estado == MORTE and button == mouse.LEFT:
        estado = MENU
       
        
        
def on_key_down():
    global estado
    if estado == MORTE and False:
        estado = MENU
        """
        if sounds.is_playing(musica_jogo):
            sounds.stop(musica_jogo)
        sounds.play(musica_menu)

        """
# Começa com música de menu
#sounds.play(musica_menu)