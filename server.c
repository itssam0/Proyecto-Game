#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

void register_user(FILE *logFile, char *nickname, char *email) {
    fprintf(logFile, "Nuevo usuario registrado - Nickname: %s, Email: %s\n", nickname, email);
    fflush(logFile);
}

void log_message(FILE *logFile, char *message) {
    fprintf(logFile, "%s\n", message);
    fflush(logFile);
}

int num_clients = 0;
int client_sockets[2];
pthread_mutex_t num_clients_mutex = PTHREAD_MUTEX_INITIALIZER;
int num_ready = 0;

typedef struct {
    FILE *logFile;
} GlobalData; 

GlobalData globalData;

void *handle_client(void *arg) {

    
    int client_socket = *((int *)arg);
    char buffer[1024];
    char nickname[256];
    char email[256];

    // Recibir datos del cliente
    ssize_t len = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
    buffer[len] = '\0'; // Asegurando que el string termine correctamente

    // Dividir nickname y email
    char *token = strtok(buffer, ",");
    strcpy(nickname, token);
    token = strtok(NULL, ",");
    strcpy(email, token);

    // Registrar datos del cliente
    register_user(globalData.logFile, nickname, email);

    pthread_mutex_lock(&num_clients_mutex);
    num_clients++;

    if (num_clients == 2) {
        char ready_message[] = "2 jugadores conectados";
        send(client_sockets[0], ready_message, strlen(ready_message), 0);
        send(client_sockets[1], ready_message, strlen(ready_message), 0);
        log_message(globalData.logFile, ready_message);
    } else {
        char waiting_message[] = "Esperando a que el segundo jugador se conecte...";
        send(client_socket, waiting_message, strlen(waiting_message), 0);
        log_message(globalData.logFile, waiting_message);
    }

    pthread_mutex_unlock(&num_clients_mutex);

    while (1) {
        len = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
        if (len <= 0) {
            break; // El cliente probablemente se desconectó
        }

        buffer[len] = '\0';
        log_message(globalData.logFile, buffer); // Registrar el mensaje recibido

        /*
        if (strstr(buffer, "ball_position:") != NULL) {
            if (client_socket == client_sockets[0]) { // Si es el primer jugador
                send(client_sockets[1], buffer, strlen(buffer), 0);
                log_message(globalData.logFile, buffer); // Registrar el mensaje que se va a enviar
                printf("Posición de la bola reenviada al segundo jugador: %s\n", buffer);
            } else {
                // Para el segundo jugador, invertimos la posición en el eje x
                char new_buffer[1024];
                int ball_x, ball_y;
                sscanf(buffer, "ball_position:%d,%d", &ball_x, &ball_y);
                
                // Invertimos la posición x
                int inverted_x = 800 - ball_x;
                
                sprintf(new_buffer, "ball_position:%d,%d", inverted_x, ball_y);
                send(client_sockets[0], new_buffer, strlen(new_buffer), 0);
                log_message(globalData.logFile, new_buffer);
                printf("Posición de la bola invertida y reenviada al primer jugador: %s\n", new_buffer);
            }
        }*/

        if (strstr(buffer, "paddle_y:") != NULL) {
            if (client_socket == client_sockets[0]) { // Si es el primer jugador
                send(client_sockets[1], buffer, strlen(buffer), 0);
                log_message(globalData.logFile, buffer); // Registrar el mensaje que se va a enviar
                printf("Mensaje reenviado al segundo jugador: %s\n", buffer);
            } else {
                send(client_sockets[0], buffer, strlen(buffer), 0);
                log_message(globalData.logFile, buffer); // Registrar el mensaje que se va a enviar
                printf("Mensaje reenviado al primer jugador: %s\n", buffer);
            }
        }

        if (strcmp(buffer, "ready") == 0) {
            pthread_mutex_lock(&num_clients_mutex);
            num_ready++;
            pthread_mutex_unlock(&num_clients_mutex);

            if (num_ready == 2) {
                char game_start_message[] = "juego iniciado";
                send(client_sockets[0], game_start_message, strlen(game_start_message), 0);
                send(client_sockets[1], game_start_message, strlen(game_start_message), 0);
                log_message(globalData.logFile, game_start_message);
            }
        }
    }

    close(client_socket);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s <PORT> <LogFile>\n", argv[0]);
        exit(1);
    }

    int port = atoi(argv[1]);
    char *logFileName = argv[2];

    globalData.logFile = fopen(logFileName, "w"); // a = Abre el archivo de log en modo "append" w = "write"
    if (globalData.logFile == NULL) {
        perror("Error al abrir el archivo de log");
        log_message(globalData.logFile, "Error al abrir el archivo de log");
        exit(1);
    }

    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("Error al crear el socket del servidor");
        log_message(globalData.logFile, "Error al crear el socket del servidor");
        fprintf(globalData.logFile, "Error al crear el socket del servidor");
        exit(1);
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Error al hacer bind");
        log_message(globalData.logFile, "Error al hacer bind");
        exit(1);
    }

    if (listen(server_socket, 5) == -1) {
        perror("Error al escuchar");
        log_message(globalData.logFile, "Error al escuchar");
        exit(1);
    }

    printf("Servidor esperando conexiones en el puerto %d...\n", port);
    fprintf(globalData.logFile, "Servidor esperando conexiones en el puerto %d...\n", port);

    pthread_t threads[2];
    struct sockaddr_in client_addr; // Variable para la dirección del cliente
    socklen_t client_len = sizeof(client_addr); // Variable para la longitud de la dirección del cliente

    // Esperar a que se conecten al menos dos clientes
    while (num_clients < 2) {
        int new_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_len);
        if (new_socket == -1) {
            perror("Error al aceptar la conexión del cliente");
            log_message(globalData.logFile, "Error al aceptar la conexión del cliente");
            continue;
        }

        pthread_mutex_lock(&num_clients_mutex);
        if (num_clients >= 2) { // ya hay 2 clientes conectados
            close(new_socket);
            pthread_mutex_unlock(&num_clients_mutex);
            continue;
        }
        client_sockets[num_clients] = new_socket;
        printf("Cliente %d conectado\n", num_clients + 1);

        if (pthread_create(&threads[num_clients], NULL, handle_client, &client_sockets[num_clients]) != 0) {
            perror("Error al crear el hilo del cliente");
            log_message(globalData.logFile, "Error al aceptar la conexión del cliente");
            close(client_sockets[num_clients]);
        }
        pthread_mutex_unlock(&num_clients_mutex);
    }

    for (int i = 0; i < 2; ++i) {
        pthread_join(threads[i], NULL);
    }

    close(server_socket);
    fclose(globalData.logFile);
    return 0;
}