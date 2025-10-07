import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de conexión a tu base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'thea_ia',
    'user': 'postgres',
    'password': 'PutaVidx21',  # Cambia por tu contraseña de postgres
    'port': '5432'
}

def conectar_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la DB: {e}")
        return None

# Función para insertar usuario
def crear_usuario(nombre, email):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id;",
            (nombre, email)
        )
        usuario_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return usuario_id
    return None

# Función para agendar cita
def agendar_cita(usuario_id, fecha_inicio, servicio_id):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO citas (usuario_id, fecha_inicio, servicio_id, estado) 
               VALUES (%s, %s, %s, 'pendiente') RETURNING id;""",
            (usuario_id, fecha_inicio, servicio_id)
        )
        cita_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return cita_id
    return None

# Prueba básica
if __name__ == "__main__":
    # Probar conexión
    conn = conectar_db()
    if conn:
        print("✅ Conexión exitosa a thea_ia")
        conn.close()
    else:
        print("❌ Error de conexión")
