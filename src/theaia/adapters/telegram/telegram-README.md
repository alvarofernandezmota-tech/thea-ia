# TelegramAdapter — THEA IA

**Versión:** v1.0.0  
**Estado:** ✅ Funcional  
**Fecha:** 12 Nov 2025

## 🎯 Descripción

Adapter Telegram Bot para THEA IA con persistencia PostgreSQL completa.

## ✨ Características

- ✅ Bot Telegram funcional con python-telegram-bot 20.7
- ✅ Persistencia automática de usuarios en PostgreSQL
- ✅ Persistencia de conversaciones (FSM state + context JSONB)
- ✅ Auditoría completa de mensajes (intent, entities, confidence)
- ✅ Comandos básicos: /start, /help, /reset
- ✅ Error handling con rollback automático
- ✅ Async/await completo

## 🚀 Configuración

### Variables Requeridas (.env)

```bash
# Bot Token de @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Modo (desarrollo: polling, producción: webhooks)
TELEGRAM_POLLING=true

# Webhooks (solo producción)
TELEGRAM_WEBHOOK_URL=https://api.theaia.com/webhook/telegram
TELEGRAM_WEBHOOK_SECRET=your_secret_here
