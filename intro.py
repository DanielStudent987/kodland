WIDTH = 800
HEIGHT = 600

estado = "menu"

btn_play = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 25), (200, 50))
btn_creditos = Rect((WIDTH // 2 - 100, (HEIGHT+130) // 2 - 25), (200, 50))
btn_menu = Rect((WIDTH // 6 - 50, HEIGHT // 6 - 15), (100, 30))

alien = Actor('alien')
alien.pos = 100, 56

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
    
    alien.draw()

def create_Actor():
    player = Actor("alien")
    

def on_mouse_down(pos):
    global estado
    if estado == "menu" and btn_play.collidepoint(pos):
        estado = "jogo"
        
    if estado == "jogo" and btn_menu.collidepoint(pos):
        estado = "menu"