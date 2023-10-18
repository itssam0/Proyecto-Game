# Proyecto-Game Pong
#### Samuel Acosta Aristizábal, Julio Cesar Posada Torres, Alejandro Cardona Jaramillo 

## 1. Introducción: 
En este repositorio proporciona una visión detallada de nuestro proyecto, el cual consiste en una adaptación del juego Pong estructurado en un modelo servidor-cliente. Aquí se presenta una descripción técnica y el proceso sistemático que se siguió desde la fase de conceptualización hasta su implementación final. La intención es ofrecer una comprensión clara y exhaustiva del desarrollo y las decisiones tomadas durante su construcción.

## 2. Desarrollo:
### Descripción del proyecto:
El presente proyecto propone una versión del juego Pong, enfocándose no solo en replicar su dinámica original, sino también en integrarla en el contexto de las redes y los entornos multijugador aplicando los conocimientos adqueridos en la materia de Telematica. La clave de esta transformación radica en la incorporación de una arquitectura servidor-cliente, complementada con técnicas de programación de sockets a través de la API Sockets Berkeley.

Debemos mencionar que la programación de sockets es esencial para la eficiencia de esta implementación. Garantiza que  encontremos una comunicación ágil entre el servidor y los clientes. Gracias a la utilización de sockets, se facilita el intercambio de información del juego en un contexto de tiempo real, generando una dinámica de juego.

Además la arquitectura del proyecto está fundamentada en un servidor central que actúa como núcleo coordinador, encargado de administrar el estado actual del juego,  sincronizar acciones y facilitar la interacción entre distintos clientes, actuando de manera coherente con las multiples penticiones que gestiona el servidor. Dichos clientes son responsables de procesar las entradas del usuario y presentar la visualización del juego. Esta configuración asegura una respuesta ágil y consistente durante el juego, posibilitando la participación multijugador a través de los dispositivos.

A continuación, se desglosarán y examinarán a fondo las especificidades y componentes de este proyecto.

### Flujo del programa: 


### Implementación de protocolo pong:
Creamos nuestro propio protocolo para la comunicación entre el servidor y el cliente, es neceario aclarar que el protocolo lo encontrarás en Python y en C dado que el código del cliente está hecho en Python y el del servidor en C


#### Escucha y envio de datos:
Una vez que un cliente se conecta al servidor, el servidor recibe los datos iniciales del cliente que contienen el apodo y el correo electrónico, separados por una coma. Esta información se registra en un archivo de log.

#### Verificación del Número de Clientes Conectados:
Verifica el número de clientes conectados. Si solo hay un cliente conectado, envía un mensaje Esperando a que el segundo jugador se conecte... al cliente y registra este evento en el archivo de log. Si ya hay dos clientes conectados, envía un mensaje 2 jugadores conectados a ambos clientes y registra este evento en el archivo de log.

#### Recepción y Reenvío de la Posición de la Paleta:
El servidor escucha constantemente a ambos clientes para recibir mensajes sobre la posición de la paleta. Cuando recibe un mensaje que contiene la posición de la paleta (paddle_y:) de un cliente, reenvía este mensaje al otro cliente para mantener sincronizado el estado de las paletas en el juego. Este evento también se registra en el archivo de log.

#### Manejo del Inicio del Juego:
Los clientes pueden enviar un mensaje ready para indicar que están listos para comenzar el juego. Cuando ambos clientes están listos, el servidor envía un mensaje juego iniciado a ambos clientes para indicar que el juego ha comenzado y registra este evento en el archivo de log.

#### Terminación del Cliente:
Si retorna un valor menor o igual a cero, indica que el cliente probablemente se desconectó. En este caso, se cierra el socket del cliente y se termina el hilo correspondiente.

#### Logging:
Todos los eventos importantes, como los mensajes recibidos de los clientes y los mensajes enviados a los clientes, se registran en un archivo de log mediante la función log_message.

### Ejecución del proyecto:
*Antes de leer las indicaciones debes saber que nuestro juego solo se ejecuta en computadoras que tengan Linux o a través de una maquina virtual.*

Nuestro servidor se encuentra en AWS, y opera en un puerto con una IP publica que varía cada vez que se reinicia la instancia. Para jugar, descarga el directorio del cliente y el archivo .py de constantes. Modifica la IP según te indicaremos. Luego, al ejecutar el archivo .py en tu terminal, verás la interfaz del juego.

Lo primero es introducir un alias o nombre de usuario y pulsar enter. Si no hay otro jugador en línea, verás el aviso "Esperando a que el segundo jugador se conecte...". Cuando ambos estén conectados, se mostrará "2 jugadores conectados" y un botón de 'play'. Ambos deben hacer clic en este botón para empezar. Al hacerlo, verán en pantalla las paletas y la bola. Cada jugador verá su paleta a la izquierda y la de su adversario a la derecha. 


## Conclusiones: 
- Optar por desarrollar un protocolo personalizado, en lugar de adoptar uno preexistente, fue uno de los desafíos más significativos. Al hacerlo, adaptamos la comunicación a las demandas específicas de nuestro juego.
- Al desarrollar nuestro protocolo en la capa de aplicación, tratamos de asegurar una comunicación más ajustada y efectiva para las necesidades del juego Pong, en lugar de depender de protocolos genéricos que pueden no ser del todo adecuado
- Logramos evidenciar los patrones clásicos de arquitectura de red. Esta estratificación no solo facilita la identificación y solución de problemas al separar las responsabilidades, sino que también proporciona flexibilidad, permitiendo la adaptación o modificación de una capa sin alterar significativamente las otras.
- En el marco de la implementación de nuestro juego, la determinación del protocolo adecuado resultó ser crucial. La elección de TCP, a pesar de las alternativas, se fundamentó en su capacidad para asegurar una comunicación precisa y consistente, elementos vitales en el juego de Pong. La naturaleza de conexión continua de TCP, en contraposición a la transmisión potencialmente intermitente de UDP, se alineó con nuestra visión de brindar una experiencia de juego homogénea a todos los participantes.

Al cerrar este trabajo, reiteramos nuestra dedicación y compromiso hacia el aprendizaje y los conocimientos obtenidos. Las lecciones aprendidas y las competencias adquiridas nos posicionan con una base sólida para futuros desafíos y proyectos. Agradecemos a todos los que estuvieron involucrados y brindaron su apoyo en esta travesía, como lo fueron los profesores de la materia, asi como los compañeros de carrera que fueron un gran soporte para cluminar con el trabajo. 

## Referencias: 
- https://beej.us/guide/bgc/
- https://beej.us/guide/bgnet/
- https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
- https://www.youtube.com/watch?v=zieYbvANT-4
- https://www.youtube.com/watch?v=U28svzb1WUs
- https://www.pygame.org/wiki/GettingStarted
- https://www.youtube.com/watch?v=fNerEo6Lstw
- https://www.youtube.com/watch?v=Pg_4Jz8ZIH4
- https://www.youtube.com/watch?v=3QiPPX-KeSc
