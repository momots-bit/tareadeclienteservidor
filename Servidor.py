# Importamos las librerías
import socket
import threading


# LISTA DE USUARIOS CONECTADOS

# Guardamos:
# nombre del usuario -> conexin
usuarios = {
    "Elena":conexion_elena,
    "Sara": conexion_sara
}


# FUNCIÓN PARA ATENDER A CADA CLIENTE

def atender_cliente(conexion, direccion):

    # Primero recibimos el nombre del usuario
    usuario = conexion.recv(1024).decode()

    # Guardamos al usuario y su conexión
    usuarios[usuario] = conexion

    print("Usuario conectado:", usuario)
    print("Dirección:", direccion)
    print("Usuarios conectados:", list(usuarios.keys()))


    # RECIBIR MENSAJES

    while True:

        mensaje = conexion.recv(1024).decode()

        # Si no recibimos nada, se desconectó
        if not mensaje:
            break


        # COMANDO /LISTA

        if mensaje == "/lista":

            lista = "Usuarios conectados:\n"

            for usuario_conectado in usuarios:
                lista += "- " + usuario_conectado + "\n"

            conexion.send(lista.encode())


        # MENSAJE A TODOS

        elif mensaje.startswith("@todos "):

            texto = mensaje[7:]

            mensaje_final = usuario + " a todos: " + texto

            # Recorremos todos los usuarios
            for usuario_conectado in usuarios:

                # No es necesario excluir al que envió
                conexion_destino = usuarios[usuario_conectado]

                conexion_destino.send(mensaje_final.encode())


        # MENSAJE A UN USUARIO ESPECÍFICO

        elif mensaje.startswith("@"):

            # Quitamos el @
            contenido = mensaje[1:]

            # Separamos usuario y mensaje
            partes = contenido.split(" ", 1)

            if len(partes) == 2:

                destinatario = partes[0]
                texto = partes[1]


                # Comprobamos si existe
                if destinatario in usuarios:

                    # Obtenemos la conexión del destinatario
                    conexion_destino = usuarios[destinatario]

                    # Creamos el mensaje
                    mensaje_final = usuario + ": " + texto

                    # Solamente se manda al destinatario
                    conexion_destino.send(mensaje_final.encode())

                    # Avisamos al remitente
                    conexion.send(
                        ("Mensaje enviado a " + destinatario).encode()
                    )

                else:

                    conexion.send(
                        "Ese usuario no está conectado.".encode()
                    )

            else:

                conexion.send(
                    "Uso: @usuario mensaje".encode()
                )


        
        # MENSAJE NORMAL

        else:

            print(usuario + ":", mensaje)

            conexion.send(
                "Usa @usuario mensaje para enviar a alguien.".encode()
            )


    
    # CLIENTE DESCONECTADO

    if usuario in usuarios:
        del usuarios[usuario]

    conexion.close()

    print("Usuario desconectado:", usuario)
    print("Usuarios conectados:", list(usuarios.keys()))


# CREACIÓN DEL SOCKET

servidor = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


# IP Y PUERTO

servidor.bind(("192.168.201.14", 5000))


# ESPERAR CONEXIONES

servidor.listen(2)

print("Servidor esperando conexiones...")


# ACEPTAR CLIENTES

while True:

    conexion, direccion = servidor.accept()

    hilo = threading.Thread(
        target=atender_cliente,
        args=(conexion, direccion)
    )

    hilo.start()
