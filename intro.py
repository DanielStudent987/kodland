import random

WIDTH = 800
HEIGHT = 700

MENU = "menu"
JOGO = "jogo"
MORTE = "morte"
estado = MENU

animacoes_player = {
    "idle": ["alien_idle1", "alien_idle2"],
    "up": ["walk_up1", "walk_up2"],
    "down": ["walk_down1", "walk_down2"],
    "left": ["walk_e1", "walk_e2", "walk_e3"],
    "right": ["walk_d1", "walk_d2", "walk_d3"]
}

player_direcao = "idle"
frame_atual = 0
frame_timer = 0
frame_intervalo = 0.15

animacoes_inimigo = {
    "idle": ["enemy_right1", "enemy_idle3"],
    "up": ["enemy_up1", "enemy_up2"],
    "down": ["enemy_down1", "enemy_down2"],
    "left": ["enemy_left1", "enemy_left2"],
    "right": ["enemy_right1", "enemy_right2"]
}


#Player e inimigo
player = Actor(animacoes_player[player_direcao][frame_atual], (WIDTH//2, HEIGHT//2))
inimigos = []
velocidade = 3

#Botão do menu
botao_jogar = Rect((WIDTH//2 - 100, HEIGHT//2 - 40), (200, 50))

#Sons
musica_jogo = False

#Função para resetar o jogo
def iniciar_jogo():
    global estado, player, inimigos, musica_jogo
    estado = JOGO
    player.pos = (WIDTH//2, HEIGHT//2)
    inimigos.clear()
    for _ in range(3):
        spawn_inimigo()
    
    if not musica_jogo:
        sounds.musica.play(-1)
        musica_jogo = True
        

def spawn_inimigo():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    inimigo = Actor("inimigo", (x, y))
    inimigo.frame = 0
    inimigo.timer = 0
    inimigo.direction = "idle"
    inimigos.append(inimigo)

def draw():
    screen.clear()

    if estado == MENU:
        screen.fill((30, 30, 30))
        screen.draw.text("ROGUELIKE", center=(WIDTH//2, 100), fontsize=60, color="white")
        screen.draw.filled_rect(botao_jogar, (0, 150, 0))
        screen.draw.text("JOGAR", center=botao_jogar.center, fontsize=40, color="white")
        

    elif estado == JOGO:
        player.draw()
        for inimigo in inimigos:
            inimigo.draw()

    elif estado == MORTE:
        screen.fill((0, 0, 0))
        screen.draw.text("VOCÊ MORREU!", center=(WIDTH//2, HEIGHT//2 - 30), fontsize=60, color="red")
        screen.draw.text("click na tela pra voltar ao menu", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color="white")

def update(dt):
    if estado == JOGO:
        mover_player(dt)
        mover_inimigos(dt)
        checar_colisoes()

def mover_player(dt):
    global frame_atual, frame_timer, player_direcao
    moveu = False
    
    if keyboard.left:
        player.x -= velocidade
        player_direcao = "left"
        moveu = True
    elif keyboard.right:
        player.x += velocidade
        player_direcao = "right"
        moveu = True
    elif keyboard.up:
        player.y -= velocidade
        player_direcao = "up"
        moveu = True
    elif keyboard.down:
        player.y += velocidade
        player_direcao = "down"
        moveu = True
    else:
        player_direcao = "idle"
        
    frame_timer += dt
    if frame_timer >= frame_intervalo:
        frame_timer = 0
        frame_atual = (frame_atual + 1) % len(animacoes_player[player_direcao])
        player.image = animacoes_player[player_direcao][frame_atual]

def mover_inimigos(dt):
    global frame_intervalo
    mover = False
    
    for inimigo in inimigos:
        dx = player.x - inimigo.x
        dy = player.y - inimigo.y
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        inimigo.x += velocidade * 0.5 * dx / dist
        inimigo.y += velocidade * 0.5 * dy / dist
        
        if dx < 0 and abs(dx) > abs(dy):
            inimigo.direction = "left"
        elif dx > 0 and abs(dx) > abs(dy):
            inimigo.direction = "right"
        elif dy < 0 and abs(dy) > abs(dx):
            inimigo.direction = "up"
        elif dy > 0 and abs(dy) > abs(dx):
            inimigo.direction = "down"
        else:
            inimigo.direction = "idle"

        #print(f"Inimigo indo para: {enemy_direction}")
            
        inimigo.timer += dt
        if inimigo.timer >= frame_intervalo:
            inimigo.timer = 0
            inimigo.frame = (inimigo.frame + 1) % len(animacoes_inimigo[inimigo.direction])
            inimigo.image = animacoes_inimigo[inimigo.direction][inimigo.frame]
            
    

def checar_colisoes():
    global estado
    for obj in inimigos:
        if player.colliderect(obj):
            estado = MORTE
            sounds.eep.play()
            break
        
        #if obj.colliderect():

def on_mouse_down(pos, button):
    global estado, musica_jogo
    if estado == MENU and botao_jogar.collidepoint(pos):
        iniciar_jogo()
        
    if player.collidepoint(pos):
        sounds.eep.play()
        
    if estado == MORTE and button == mouse.LEFT:
        estado = MENU
        musica_jogo = False
        sounds.musica.stop()
       
        
def on_key_down():
    global estado
    if estado == MORTE and False:
        estado = MENU
        

