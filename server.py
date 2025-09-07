import socket
import sqlite3
from datetime import datetime

# --- Creación de la base de datos y la tabla de mensajes ---
def inicializar_db():
    """Crea la base de datos y la tabla si no existen"""
    
    
# --- Crear tabla con id, contenido, fecha e IP. Si no hay errores, da el mensaje "Base de datos lista" ---
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("Base de datos lista.")
        
    # --- Si hay errores, da el mensaje "Error al inicializar la base de datos" ---
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        exit(1)

# --- Guarda un mensaje en la base de datos y devuelve la confirmación con la fecha de envío ---
def guardar_mensaje(contenido, ip_cliente):
    """Guarda un mensaje en la base de datos y devuelve la fecha de envío"""
    try:
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                       (contenido, fecha_envio, ip_cliente))
        conn.commit()
        conn.close()
        return fecha_envio
  # --- Si hay algún error, da el mensaje "Error al guardar el mensaje" ---
    except sqlite3.Error as e:
        print(f"Error al guardar el mensaje: {e}")
        return None

# --- Servidor ---
def inicializar_socket():
    """Configura el socket TCP/IP en localhost:5000"""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        server_socket.bind(("127.0.0.1", 5000))  # localhost:5000
        server_socket.listen(5)  # hasta 5 conexiones en espera
        print("Servidor escuchando en 127.0.0.1:5000")
        return server_socket
    except OSError as e:
        print(f"Error al iniciar el socket: {e}")
        exit(1)

def manejar_conexiones(server_socket):
    """Acepta conexiones y procesa mensajes de los clientes"""
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida desde {client_address}")

        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break  # si no hay datos, se corta la conexión

         # --- Guardar mensaje en la DB ---
            fecha_envio = guardar_mensaje(data, client_address[0])
            if fecha_envio:
                respuesta = f"Mensaje recibido: {fecha_envio}"
            else:
                respuesta = "Error al guardar el mensaje"

            # --- Enviar respuesta al cliente ---
            client_socket.send(respuesta.encode("utf-8"))

            # --- Si el cliente envía "éxito", se cierra esa conexión ---
            if data.lower() == "éxito":
                print("Cliente finalizó la sesión.")
                break

        client_socket.close()

if __name__ == "__main__":
    inicializar_db()
    server_socket = inicializar_socket()
    manejar_conexiones(server_socket)
