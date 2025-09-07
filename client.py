import socket

def cliente():
    """Cliente TCP que envía mensajes al servidor"""
    # --- Creación del socket ---
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # --- Conexión al servidor en localhost: 5000 ----
    client_socket.connect(("127.0.0.1", 5000))

    while True:
    # --- Se solicita un mensaje al usuario y se lo envía al servidor---
        mensaje = input("Escribí un mensaje ('salida' para salir): ")
        client_socket.send(mensaje.encode("utf-8"))

    # --- Se espera la respuesta del servidor ---
        respuesta = client_socket.recv(1024).decode("utf-8")
        print(f"Servidor: {respuesta}")
        
    # --- Si la respuesta es "salida", se cierra la conexión ---
        if mensaje.lower() == "salida":
            print("Cerrando conexión...")
            break
    # --- Cierre de la conexión ---           
    client_socket.close()

# --- Ejecuta la función principal del cliente para conectarse al servidor y enviar mensajes ---
    cliente()
