import pygame
import socket

import time

# Configuración del juego
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 70
#score1 = 0
#score2 = 0

# Inicializar Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 32)

def draw_text(text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    win.blit(surface, (x, y))

def draw_button(text, x, y, width, height):
    pygame.draw.rect(win, (50, 200, 50), (x, y, width, height))
    button_text = font.render(text, True, (255, 255, 255))
    text_width, text_height = button_text.get_size()
    win.blit(button_text, (x + (width - text_width) // 2, y + (height - text_height) // 2))


def input_loop(prompt):
    input_string = ""
    while True:
        win.fill((0, 0, 0))
        draw_text(prompt + input_string + "|", 10, 10)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_string
                elif event.key == pygame.K_BACKSPACE:
                    input_string = input_string[:-1]
                else:
                    input_string += event.unicode

def check_for_server_messages(sock):
    try:
        sock.settimeout(0.01)
        message = sock.recv(1024).decode().rstrip('\x00')
        return message
    except socket.timeout:
        return None

def main():
    host = "172.17.0.1"
    port = 8080
    state = "WAITING"
    
    #Boton de play
    play_button = {"x": WIDTH//2 - 70, "y": HEIGHT//2 - 25, "width": 140, "height": 50}
    
    #Variables de movimiento y velocidad de la bola
    ball_dx = 5
    ball_dy = 5
    BALL_SPEED = 1
    
    # Initial position of the ball
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    nickname = input_loop("Introduce tu apodo: ")
    if nickname is None:
        pygame.quit()
        return
    email = input_loop("Introduce tu dirección de correo electrónico: ")
    if email is None:
        pygame.quit()
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Conectado al servidor.")

    client_socket.sendall(f"{nickname},{email}".encode())
    game_message = client_socket.recv(1024).decode().rstrip('\x00')

    game_started = False
    paddle_y = HEIGHT // 2

    BALL_RADIUS = 10

    

    # Variables para la posición de la paleta del otro jugador
    other_paddle_y = HEIGHT // 2
    
    # Velocidad de movimiento de la paleta
    PADDLE_SPEED = 5

    # ...

    while True:
        win.fill((0, 0, 0))

        message = ""  # Inicializa la variable message al comienzo del bucle
        
        new_message = check_for_server_messages(client_socket)
        if new_message:
            if new_message == "juego iniciado":
                state = "PLAYING"
            else:
                game_message = new_message  # Actualizar el mensaje del juego

        if state == "WAITING":
            draw_text(game_message, 10, 10)
            if game_message == "2 jugadores conectados":
                draw_button("Play", play_button["x"], play_button["y"], play_button["width"], play_button["height"])

        elif state == "PLAYING":
            # Manejar entrada del jugador para mover la paleta
            keys = pygame.key.get_pressed()
            
            # Variables para la actualización posición de la bola
            ball_x += ball_dx * BALL_SPEED
            ball_y += ball_dy * BALL_SPEED
            
            #Colisión de bola con las paredes
            if ball_y <= BALL_RADIUS or ball_y >= HEIGHT - BALL_RADIUS:
                ball_dy = -ball_dy

            #Colisión de bola con las paletas
            paddle_rect = pygame.Rect(30, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
            other_paddle_rect = pygame.Rect(WIDTH-30-PADDLE_WIDTH, other_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
            ball_rect = pygame.Rect(ball_x, ball_y, BALL_RADIUS*2, BALL_RADIUS*2)

            # Comprobar colisiones
            if paddle_rect.colliderect(ball_rect) or other_paddle_rect.colliderect(ball_rect):
                ball_dx = -ball_dx
            
            # Detectar si la bola golpea los lados izquierdo o derecho de la ventana
            if ball_x <= BALL_RADIUS:
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = -ball_dx  # Cambia la dirección en x
                #draw_text(text1, 10, 10)

            if ball_x >= WIDTH - BALL_RADIUS:
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = -ball_dx  # Cambia la dirección en x
                #draw_text(text2, 10, 100)
                


            
            if keys[pygame.K_w] and paddle_y > 0:
                paddle_y -= PADDLE_SPEED
                print(f"Posición de la paleta después de mover hacia arriba: {paddle_y}")

                message = f"paddle_y:{paddle_y}\n"
                client_socket.sendall(message.encode())
                print(f"Mensaje enviado al servidor: {message}\n")

                #client_socket.sendall(f"paddle_y:{paddle_y}".encode())
            if keys[pygame.K_s] and paddle_y < HEIGHT - PADDLE_HEIGHT:
                paddle_y += PADDLE_SPEED
                print(f"Posición de la paleta después de mover hacia abajo: {paddle_y}\n")

                message = f"paddle_y:{paddle_y}"
                client_socket.sendall(message.encode())
                print(f"Mensaje enviado al servidor: {message}")

                #client_socket.sendall(f"paddle_y:{paddle_y}".encode())
            
            #Envio de posición al servidor
            ball_message = f"ball_position:{ball_x},{ball_y}"
            client_socket.sendall(ball_message.encode())
            
            #Mensaje del servidor de la posicion de la bola
            if "ball_position:" in message:
                ball_info = message.split(":")[1].split(',')
                ball_x, ball_y = int(ball_info[0]), int(ball_info[1])

            new_message = check_for_server_messages(client_socket)
            if new_message:
                messages = new_message.split('\n')
                for msg in messages:  # Cambié la variable del bucle para evitar confusiones
                    if "paddle_y:" in msg:
                        paddle_info = msg.split(":")
                        if len(paddle_info) > 1:
                            try:
                                other_paddle_y = HEIGHT - int(paddle_info[1])
                            except ValueError:
                                print(f"Valor no válido para la posición de la paleta: {paddle_info[1]}")

            
            # Dibujar las paletas
            pygame.draw.rect(win, (255, 255, 255), (30, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.rect(win, (255, 255, 255), (WIDTH - 30 - PADDLE_WIDTH, other_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
            
            # Dibujar la bola
            pygame.draw.circle(win, (255, 255, 255), (ball_x, ball_y), BALL_RADIUS)
            
            #Dibujar puntajes
            #text1 = font.render(str(score1), True, (255, 255, 255))
            #text2 = font.render(str(score2), True, (255, 255, 255))

            # ...

        else:
            draw_text(game_message, 10, 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if state == "WAITING" and game_message == "2 jugadores conectados":
                    if play_button["x"] <= mouse_x <= play_button["x"] + play_button["width"] and play_button["y"] <= mouse_y <= play_button["y"] + play_button["height"]:
                        state = "READY_TO_PLAY"
                        client_socket.sendall("ready".encode())

if __name__ == "__main__":
    main()
