import socket

def cliente():
    """Cliente TCP que envía mensajes al servidor"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5000))

    while True:
        mensaje = input("Escribí un mensaje ('salida' para salir): ")
        client_socket.send(mensaje.encode("utf-8"))

        respuesta = client_socket.recv(1024).decode("utf-8")
        print(f"Servidor: {respuesta}")

        if mensaje.lower() == "salida":
            print("Cerrando conexión...")
            break

    client_socket.close()

if __name__ == "__main__":
    cliente()
