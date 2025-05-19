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

animacoes_enemy = {
    "idle": ["enemy_right1", "enemy_idle3"],
    "up": ["enemy_up1", "enemy_up2"],
    "down": ["enemy_down1", "enemy_down2"],
    "left": ["enemy_left1", "enemy_left2"],
    "right": ["enemy_right1", "enemy_right2"]
}

velocity = 5
enemies = []
enemy_number = 3
bullets = []

#Botão do menu
button_play = Rect((WIDTH//2 - 100, HEIGHT//2 - 50), (200, 50))
button_music = Rect((WIDTH//2 - 100, HEIGHT//2 + 10), (200, 50))
button_exit = Rect((WIDTH//2 - 100, HEIGHT//2 + 70), (200, 50))
music_control = True

#Sons
music_game = False


class Player:
    def __init__(self):
        self.direcao = "idle"
        self.frame_atual = 0
        self.frame_timer = 0
        self.sprite = Actor(animacoes_player[self.direcao][self.frame_atual], (WIDTH//2, HEIGHT//2))

    def update(self, dt):
        
        if keyboard.left:
            self.sprite.x -= velocity
            self.direcao = "left"
            
        elif keyboard.right:
            self.sprite.x += velocity
            self.direcao = "right"
            
        elif keyboard.up:
            self.sprite.y -= velocity
            self.direcao = "up"
            
        elif keyboard.down:
            self.sprite.y += velocity
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
            bullets.append(Projetil(self.sprite.x, self.sprite.y, dx, dy))
            
            if music_control:
                sounds.dead_enemy.play()
            

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
        self.sprite.x += velocity * 0.5 * dx / dist
        self.sprite.y += velocity * 0.5 * dy / dist

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
            self.frame = (self.frame + 1) % len(animacoes_enemy[self.direction])
            self.sprite.image = animacoes_enemy[self.direction][self.frame]

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


#Inicio do jogo
def iniciar_jogo():
    global estado, enemies, music_game, player, bullets
    estado = JOGO
    player = Player()
    enemies.clear()
    bullets.clear()
    for _ in range(3):
        spawn_enemy()

    if not music_game and music_control:
        sounds.musica.play(-1)
        music_game = True


def spawn_enemy():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    enemies.append(Inimigo(x, y))


def draw():
    screen.clear()
    if estado == MENU:
        screen.fill((30, 30, 30))
        screen.draw.text("Aventura Espacial", center=(WIDTH//2, 200), fontsize=60, color="white")
        
        screen.draw.filled_rect(button_play, (0, 150, 0))
        screen.draw.text("JOGAR", center=button_play.center, fontsize=40, color="white")
        
        screen.draw.filled_rect((button_music), (0, 0, 150))
        screen.draw.text("Musica e Sons", center=button_music.center, fontsize=40, color="white")
        
        screen.draw.filled_rect(button_exit, (150, 0, 0))
        screen.draw.text("SAIR", center=button_exit.center, fontsize=40, color="white")
        
        screen.draw.text("Use as setas para mover e espaço para atirar\nMira andando na direcao que quer atirar", center=(WIDTH//2, HEIGHT//2 + 160), fontsize=30, color="green")
        
        if music_control:
            sounds.menu_music.play(-1)
        else:
            sounds.menu_music.stop()
            

    elif estado == JOGO:
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()

    elif estado == MORTE:
        screen.fill((0, 0, 0))
        screen.draw.text("VOCÊ MORREU!", center=(WIDTH//2, HEIGHT//2 - 30), fontsize=60, color="red")
        screen.draw.text("click na tela pra voltar ao menu", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color="white")

def update(dt):
    global enemy_number, music_control
    if estado == JOGO:
        player.update(dt)
        for enemy in enemies:
            enemy.update(dt, player.get_actor().pos)
        for p in bullets:
            p.update()
        checar_colisoes()
        
        if len(enemies) == 0:
            enemy_number += 1

            for _ in range(enemy_number): 
                spawn_enemy()
                
        if estado == MORTE:
            enemies.clear()
            enemy_number = 3
                
        if player.get_actor().x < 0:
            player.get_actor().x = 0
        elif player.get_actor().x > WIDTH:
            player.get_actor().x = WIDTH
        if player.get_actor().y < 0:
            player.get_actor().y = 0
        elif player.get_actor().y > HEIGHT:
            player.get_actor().y = HEIGHT     
    
        
def checar_colisoes():
    global estado, enemies, enemy_number
    for obj in enemies:
        if player.get_actor().colliderect(obj.get_actor()):
            enemies.clear()
            estado = MORTE
            enemy_number = 3
            if music_control:
                sounds.eep.play()
            break
    for bullet in bullets[:]:
        for enemy in enemies:
            if bullet.get_actor().colliderect(enemy.get_actor()):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

def on_mouse_down(pos, button):
    global estado, music_game, music_control, enemies, enemy_number
    if estado == MENU and button_play.collidepoint(pos):
        sounds.menu_music.stop()
        iniciar_jogo()
        
    if estado == MENU and button_music.collidepoint(pos):
        if music_control:
            music_control = False
        else:
            music_control = True
            
    if estado == MENU and button_exit.collidepoint(pos):
        exit()      

    if estado == MORTE and button == mouse.LEFT:
        estado = MENU
        music_game = False
        enemies.clear()
        enemy_number = 3
        sounds.musica.stop()
        
    

def on_key_down():
    global estado
    if estado == JOGO and keyboard[keys.SPACE]:
        player.atirar()
    if estado == MORTE and False:
        estado = MENU
        
