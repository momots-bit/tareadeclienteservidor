import socket
import threading

# FUNCIÓN PARA RECIBIR MENSAJES
def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(
                1024
            ).decode()
            if mensaje:
                print()
                print(
                    mensaje,
                    end=""
                )
                print(
                    "Tú: ",
                    end="",
                    flush=True
                )
        except:
            print(
                "\nConexión cerrada."
            )
            break

# CREAR SOCKET
cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# IP DEL SERVIDOR
ip_servidor = input(
    "Escribe la IP del servidor: "
)

# CONECTARSE
cliente.connect(
    (ip_servidor, 5000)
)

print(
    "Conectado al servidor."
)

# NOMBRE DE USUARIO
usuario = input(
    "Escribe tu nombre de usuario: "
)

# ENVIAR NOMBRE
cliente.send(
    (usuario + "\n").encode()
)

# CREAR HILO PARA RECIBIR
hilo_recibir = threading.Thread(
    target=recibir_mensajes
)
hilo_recibir.daemon = True
hilo_recibir.start()

# ENVIAR MENSAJES
while True:
    mensaje = input("Tú: ")

    cliente.send(
        (mensaje + "\n").encode()
    )