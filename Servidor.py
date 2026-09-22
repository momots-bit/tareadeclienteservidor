# Importamos las librerías
import socket
import threading

# LISTA DE USUARIOS CONECTADOS

# Guardamos:
# nombre del usuario -> conexión
usuarios = {}


# FUNCIÓN PARA ENVIAR MENSAJES DESDE EL SERVIDOR

def enviar_desde_servidor():
    while True:
        mensaje = input("Servidor: ")
        # MENSAJE A TODOS
        if mensaje.startswith("@todos "):
            texto = mensaje[7:]
            mensaje_final = ("Servidor a todos: "+ texto+ "\n")
            for usuario_conectado in list(usuarios):
                conexion_destino = usuarios[ usuario_conectado ]
                try:
                    conexion_destino.send( mensaje_final.encode())
                except:
                    pass


        # MENSAJE A UN USUARIO ESPECÍFICO
        elif mensaje.startswith("@"):
            contenido = mensaje[1:]
            partes = contenido.split(" ", 1)
            if len(partes) == 2:
                destinatario = partes[0]
                texto = partes[1]
                # Comprobar si está conectado
                if destinatario in usuarios:
                    conexion_destino = usuarios[destinatario ]
                    mensaje_final = ("Servidor: "+ texto+ "\n" )
                    try:
                        conexion_destino.send( mensaje_final.encode())
                        print("Mensaje enviado a "+ destinatario)
                    except:
                        print("No se pudo enviar el mensaje." )
                else:
                    print( "Ese usuario no está conectado." )
            else:
                print("Uso: @usuario mensaje")

        # COMANDO NO RECONOCIDO
        else:

            print(
                "Usa @usuario mensaje "
                "o @todos mensaje"
            )


# FUNCIÓN PARA ATENDER A CADA CLIENTE

def atender_cliente(conexion, direccion):

    # RECIBIR NOMBRE DEL USUARIO
    usuario = conexion.recv(1024).decode().strip()
    # Si no llegó nombre, cerramos
    if not usuario:
        conexion.close()
        return

    # GUARDAR USUARIO
    usuarios[usuario] = conexion

    print()
    print("Usuario conectado:", usuario)
    print("Dirección:", direccion)
    print(
        "Usuarios conectados:",
        list(usuarios.keys())
    )

    # RECIBIR MENSAJES
    while True:
        try:
            mensaje = conexion.recv(
                1024
            ).decode().strip()
        except:         
            break
        # Si no recibimos nada,
        # el cliente se desconectó
        if not mensaje:
            break

        # COMANDO /LISTA
        if mensaje == "/lista":
            lista = ("Usuarios conectados:\n" )
            for usuario_conectado in usuarios:
                lista += (
                    "- "
                    + usuario_conectado
                    + "\n"
                )
            conexion.send(lista.encode() )

        # MENSAJE A TODOS
        elif mensaje.startswith("@todos "):

            texto = mensaje[7:]

            mensaje_final = (usuario + " a todos: "+ texto + "\n" )

            for usuario_conectado in list(usuarios):
                conexion_destino = usuarios[usuario_conectado]
                try:
                    conexion_destino.send( mensaje_final.encode())
                except:
                    pass

        # MENSAJE A UN USUARIO ESPECÍFICO
        elif mensaje.startswith("@"):
            contenido = mensaje[1:]
            partes = contenido.split( " ",1)

            if len(partes) == 2:
                destinatario = partes[0]
                texto = partes[1]

                # Comprobar si existe
                if destinatario in usuarios:
                    conexion_destino = usuarios[destinatario]
                    mensaje_final = (usuario + ": "+ texto + "\n" )
                    try:
                        # Mandar solamente al destinatario
                        conexion_destino.send( mensaje_final.encode())
                        # Avisar al que envió
                        conexion.send(("Mensaje enviado a " + destinatario + "\n" ).encode() )

                    except:
                        print("Error al enviar mensaje." )

                else:
                    conexion.send(
                        ("Ese usuario no " 
                         "está conectado.\n"
                        ).encode()
                    )

            else:
                conexion.send( ( "Uso: @usuario mensaje\n" ).encode())
               
        # MENSAJE NORMAL
        else:
            print( usuario+ ": "+ mensaje)

            conexion.send(
                ( "Usa @usuario mensaje "
                    "para enviar a alguien.\n"
                ).encode()
            )

    # CLIENTE DESCONECTADO
    if usuario in usuarios:

        del usuarios[usuario]

    conexion.close()

    print()
    print("Usuario desconectado:", usuario)

    print("Usuarios conectados:",list(usuarios.keys()) )

# CREAR SOCKET DEL SERVIDOR
servidor = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# IP Y PUERTO
servidor.bind(
    ("192.168.200.103", 5000)
)

# ESPERAR CONEXIONES
servidor.listen(2)
print(
    "Servidor esperando conexiones..."
)

# HILO PARA QUE EL SERVIDOR PUEDA ENVIAR
hilo_servidor = threading.Thread(
    target=enviar_desde_servidor
)

hilo_servidor.daemon = True
hilo_servidor.start()


# ACEPTAR CLIENTES
while True:

    conexion, direccion = servidor.accept()

    hilo = threading.Thread(
        target=atender_cliente,
        args=(conexion, direccion)
    )

    hilo.daemon = True

    hilo.start()
