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

animacoes_inimigo = {
    "idle": ["enemy_right1", "enemy_idle3"],
    "up": ["enemy_up1", "enemy_up2"],
    "down": ["enemy_down1", "enemy_down2"],
    "left": ["enemy_left1", "enemy_left2"],
    "right": ["enemy_right1", "enemy_right2"]
}

velocidade = 3
inimigos = []
projeteis = []

# Botão do menu
botao_jogar = Rect((WIDTH//2 - 100, HEIGHT//2 - 40), (200, 50))

# Sons
musica_jogo = False

class Player:
    def __init__(self):
        self.direcao = "idle"
        self.frame_atual = 0
        self.frame_timer = 0
        self.sprite = Actor(animacoes_player[self.direcao][self.frame_atual], (WIDTH//2, HEIGHT//2))

    def update(self, dt):
        
        if keyboard.left:
            self.sprite.x -= velocidade
            self.direcao = "left"
            
        elif keyboard.right:
            self.sprite.x += velocidade
            self.direcao = "right"
            
        elif keyboard.up:
            self.sprite.y -= velocidade
            self.direcao = "up"
            
        elif keyboard.down:
            self.sprite.y += velocidade
            self.direcao = "down"
            
        else:
            self.direcao = "idle"

        self.frame_timer += dt
        if self.frame_timer >= 0.15:
            self.frame_timer = 0
            self.frame_atual = (self.frame_atual + 1) % len(animacoes_player[self.direcao])
            self.sprite.image = animacoes_player[self.direcao][self.frame_atual]

    def draw(self):
        self.sprite.draw()

    def get_actor(self):
        return self.sprite
    
    def atirar(self):
        dx, dy = 0, 0
        if self.direcao == "up": dy = -1
        elif self.direcao == "down": dy = 1
        elif self.direcao == "left": dx = -1
        elif self.direcao == "right": dx = 1

        if dx != 0 or dy != 0:
            projeteis.append(Projetil(self.sprite.x, self.sprite.y, dx, dy))

class Inimigo:
    def __init__(self, x, y):
        self.sprite = Actor("inimigo", (x, y))
        self.frame = 0
        self.timer = 0
        self.direction = "idle"

    def update(self, dt, player_pos):
        dx = player_pos[0] - self.sprite.x
        dy = player_pos[1] - self.sprite.y
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        self.sprite.x += velocidade * 0.5 * dx / dist
        self.sprite.y += velocidade * 0.5 * dy / dist

        if dx < 0 and abs(dx) > abs(dy):
            self.direction = "left"
        elif dx > 0 and abs(dx) > abs(dy):
            self.direction = "right"
        elif dy < 0 and abs(dy) > abs(dx):
            self.direction = "up"
        elif dy > 0 and abs(dy) > abs(dx):
            self.direction = "down"
        else:
            self.direction = "idle"

        self.timer += dt
        if self.timer >= 0.15:
            self.timer = 0
            self.frame = (self.frame + 1) % len(animacoes_inimigo[self.direction])
            self.sprite.image = animacoes_inimigo[self.direction][self.frame]

    def draw(self):
        self.sprite.draw()

    def get_actor(self):
        return self.sprite
    
class Projetil:
    def __init__(self, x, y, dx, dy):
        self.sprite = Actor("bullet", (x, y))
        self.dx = dx * 10
        self.dy = dy * 10

    def update(self):
        self.sprite.x += self.dx
        self.sprite.y += self.dy

    def draw(self):
        self.sprite.draw()

    def get_actor(self):
        return self.sprite

player = Player()

def iniciar_jogo():
    global estado, inimigos, musica_jogo, player, projeteis
    estado = JOGO
    player = Player()
    inimigos.clear()
    projeteis.clear()
    for _ in range(3):
        spawn_inimigo()

    if not musica_jogo:
        sounds.musica.play(-1)
        musica_jogo = True

def spawn_inimigo():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    inimigos.append(Inimigo(x, y))

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
        for p in projeteis:
            p.draw()

    elif estado == MORTE:
        screen.fill((0, 0, 0))
        screen.draw.text("VOCÊ MORREU!", center=(WIDTH//2, HEIGHT//2 - 30), fontsize=60, color="red")
        screen.draw.text("click na tela pra voltar ao menu", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color="white")

def update(dt):
    if estado == JOGO:
        player.update(dt)
        for inimigo in inimigos:
            inimigo.update(dt, player.get_actor().pos)
        for p in projeteis:
            p.update()
        checar_colisoes()

def checar_colisoes():
    global estado
    for obj in inimigos:
        if player.get_actor().colliderect(obj.get_actor()):
            estado = MORTE
            sounds.eep.play()
            break

def on_mouse_down(pos, button):
    global estado, musica_jogo
    if estado == MENU and botao_jogar.collidepoint(pos):
        iniciar_jogo()

    if estado == MORTE and button == mouse.LEFT:
        estado = MENU
        musica_jogo = False
        sounds.musica.stop()

def on_key_down():
    global estado
    if estado == JOGO and keyboard[keys.SPACE]:
        player.atirar()
    if estado == MORTE and False:
        estado = MENU
