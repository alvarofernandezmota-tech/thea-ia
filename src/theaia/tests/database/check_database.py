"""
Script para ver contenido PostgreSQL
"""
import asyncio
from sqlalchemy import text
from src.theaia.database.session import AsyncSessionLocal


async def ver_base_datos():
    """Muestra usuarios, conversaciones y mensajes."""
    async with AsyncSessionLocal() as session:
        print("\n" + "="*60)
        print("📊 BASE DE DATOS THEA IA - PostgreSQL")
        print("="*60)
        
        # === USUARIOS ===
        print("\n🧑 USUARIOS:")
        print("-" * 60)
        result = await session.execute(
            text("SELECT id, telegram_id, username, first_name, created_at FROM users")
        )
        users = result.fetchall()
        
        if users:
            for user in users:
                print(f"  ID: {user[0]}")
                print(f"  Telegram ID: {user[1]}")
                print(f"  Username: @{user[2]}")
                print(f"  Nombre: {user[3]}")
                print(f"  Creado: {user[4]}")
                print("-" * 60)
        else:
            print("  ⚠️ No hay usuarios registrados")
        
        # === CONVERSACIONES ===
        print("\n💬 CONVERSACIONES:")
        print("-" * 60)
        result = await session.execute(
            text("SELECT id, session_id, current_state, is_active, started_at FROM conversations")
        )
        convs = result.fetchall()
        
        if convs:
            for conv in convs:
                print(f"  ID: {conv[0]}")
                print(f"  Session ID: {conv[1]}")
                print(f"  Estado: {conv[2]}")
                print(f"  Activa: {'Sí' if conv[3] else 'No'}")
                print(f"  Iniciada: {conv[4]}")
                print("-" * 60)
        else:
            print("  ⚠️ No hay conversaciones activas")
        
        # === MENSAJES ===
        print("\n📝 MENSAJES (últimos 5):")
        print("-" * 60)
        result = await session.execute(
            text("""
                SELECT 
                    id, 
                    user_message, 
                    bot_response, 
                    intent_detected, 
                    confidence_score,
                    created_at
                FROM message_history 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
        )
        msgs = result.fetchall()
        
        if msgs:
            for i, msg in enumerate(msgs, 1):
                print(f"\n  Mensaje {i}:")
                print(f"    User: {msg[1]}")
                print(f"    Bot: {msg[2][:70]}...")
                print(f"    Intent: {msg[3]} (confidence: {msg[4]})")
                print(f"    Fecha: {msg[5]}")
                print("-" * 60)
        else:
            print("  ⚠️ No hay mensajes guardados")
        
        print("\n" + "="*60)
        print("✅ Consulta completada")
        print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(ver_base_datos())
