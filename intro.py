WIDTH = 800
HEIGHT = 700

estado = "menu"

#botoes do menu
btn_play = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 25), (200, 50))
btn_creditos = Rect((WIDTH // 2 - 100, (HEIGHT+130) // 2 - 25), (200, 50))
btn_menu = Rect((WIDTH // 10 - 50, HEIGHT // 10 - 60), (100, 30))

#player
player = Actor('alien')
#player.pos = 100, 56

status = False

def draw():
    screen.clear()
    
    if estado == "menu":
        menu()
    elif estado == "jogo":
        jogo()

def menu():
    screen.draw.text("Roguelike", center=(WIDTH // 2, HEIGHT // 3), fontsize=60, color="white")
    
    #btn_play
    screen.draw.filled_rect(btn_play, "darkgreen")
    screen.draw.text("Jogar", center=btn_play.center, fontsize=40, color="white")
    
    #btn_creditos
    screen.draw.filled_rect(btn_creditos, "darkgreen")
    screen.draw.text("Créditos", center=btn_creditos.center, fontsize=40, color="white")

def jogo():
    screen.draw.text("teste", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="yellow")
    
    screen.draw.filled_rect(btn_menu, "darkgreen")
    screen.draw.text("Menu", center=btn_menu.center, fontsize=20, color="white")
    
    global status
    if status:
        start()
        status = True
    
    player.draw()

def create_Actor():
    #player = Actor("alien")
    player.pos = 100, 90
    
    
    
def update():
    global estado
    if estado == "jogo":
        player_move()
        if player.x < 10:
            player.x = 10
        if player.x > WIDTH-10:
            player.x = WIDTH-10
        if player.y < 100:
            player.y = 100
        if player.y > HEIGHT-20:
            player.y = HEIGHT-20
    
#moves
def player_move():
    if keyboard.left:
        player.x -= 3
    if keyboard.right:
        player.x += 3
    if keyboard.up:
        player.y -= 3
    if keyboard.down:
        player.y += 3

def on_mouse_down(pos):
    global estado
    if estado == "menu" and btn_play.collidepoint(pos):
        estado = "jogo"
        
    global status    
    if estado == "jogo" and btn_menu.collidepoint(pos):
        estado = "menu"
        status = False
        create_Actor()
        
def start():
    global estado
    if estado == "jogo":
        create_Actor()
    
    