text
# 🔧 Troubleshooting — THEA IA

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:25 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 🔴 Problemas Comunes

### 1. FSM stuck en `processing`

**Síntomas:**
- Mensaje enviado pero sin respuesta
- Estado no avanza
- Logs: `FSM.processing timeout`

**Causa probable:**
- Agente falla sin error capturado
- Context corrupto

**Solución:**
Opción 1: Reset contexto (dev)
curl -X POST http://localhost:8000/admin/context/user_123/reset

Opción 2: Limpiar manualmente
python -c "
from src.theaia.core.context import ContextManager
cm = ContextManager()
cm.clear('user_123')
"

Opción 3: Check logs
docker logs thea-ia | grep "user_123"

text

---

### 2. Database connection timeout

**Síntomas:**
- Error: `psycopg2.OperationalError: could not connect to server`
- Queries lentas (>1s)
- Logs: `DB connection pool exhausted`

**Causa probable:**
- PostgreSQL no corre
- Connection pool lleno (leak)
- Red bloqueada (firewall)

**Solución:**
Verificar PostgreSQL
docker ps | grep postgres

o
psql postgresql://user:pass@localhost:5432/theaia -c "SELECT 1"

Si no corre, iniciar
docker-compose up -d postgres

Check connection pool
docker logs thea-ia | grep "pool"

Reset pool (si está corrupto)
Reiniciar app
kubectl rollout restart deployment/thea-ia

text

---

### 3. Intent detection no funciona

**Síntomas:**
- Intent siempre "unknown"
- Entity extraction falla
- Logs: `Model not found` o `spaCy error`

**Causa probable:**
- Modelo ML no descargado
- spaCy model corrupto
- Versión Python incompatible

**Solución:**
Descargar modelo spaCy
python -m spacy download es_core_news_sm

Verificar instalación
python -c "import spacy; nlp=spacy.load('es_core_news_sm'); print('OK')"

Entrenar modelo intent si es necesario
python scripts/train_intent_model.py --data data/training_data.json --output models/intent_model.pkl

Check versión Python
python --version # Debe ser 3.10+

text

---

### 4. Telegram bot no recibe mensajes

**Síntomas:**
- Bot no responde en Telegram
- Webhooks no llamados
- Logs vacíos

**Causa probable:**
- Token inválido
- Webhook URL incorrecta
- IP no whitelisted

**Solución:**
Verificar token
curl -s https://api.telegram.org/botTOKEN/getMe | jq

Verificar webhook
curl -s https://api.telegram.org/botTOKEN/getWebhookInfo | jq

Establecer webhook correcto
curl https://api.telegram.org/botTOKEN/setWebhook
-d url=https://your-domain.com/adapters/telegram/webhook
-d allowed_updates=message,callback_query

Test webhook local
ngrok http 8000 # Expone local a internet

text

---

### 5. JWT token expirado

**Síntomas:**
- Error 401 Unauthorized
- Logs: `JWT signature invalid` o `Token expired`

**Causa probable:**
- Token expirado (lifetimeToken < 1h)
- Secret JWT cambió
- Clock drift

**Solución:**
Verificar expiración token
python -c "
import jwt
token = 'your_token'
try:
jwt.decode(token, 'secret', algorithms=['HS256'])
print('Token válido')
except jwt.ExpiredSignatureError:
print('Token expirado')
except jwt.InvalidSignatureError:
print('Firma inválida')
"

Solicitar nuevo token
curl -X POST http://localhost:8000/auth/login
-d '{"email":"user@example.com","password":"..."}'

Sync time si hay clock drift
sudo ntpdate -s time.nist.gov # Linux

text

---

### 6. Tests fallan aleatoriamente

**Síntomas:**
- `pytest` pasa local, falla en CI
- Errores race conditions
- `Connection refused` aleatorio

**Causa probable:**
- Race condition en tests paralelos
- DB fixture no limpia
- Port en uso

**Solución:**
Ejecutar tests secuencialmente
pytest -n 0 # -n 0 = no parallelismo

Limpiar DB antes de tests
pytest --fixtures | grep -A 5 "db"

O manual:
python -c "
from src.theaia.tests.conftest import reset_db
reset_db()
"

Liberar port
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

text

---

### 7. Observabilidad (Prometheus/Grafana) no muestra métricas

**Síntomas:**
- Grafana: "No data"
- Prometheus: targets "DOWN"
- Logs: `metrics endpoint 404`

**Causa probable:**
- App no expone `/metrics`
- Prometheus no configado correctamente
- Firewall bloquea puerto 9090

**Solución:**
Verificar metrics endpoint
curl http://localhost:8000/metrics

Si 404, agregar a app
En src/theaia/api.py
from prometheus_client import make_wsgi_app
from prometheus_client import Counter, Histogram

Verificar Prometheus
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets.health'

Recargar config Prometheus
curl -X POST http://localhost:9090/-/reload

text

---

### 8. Docker build falla

**Síntomas:**
- Error: `ImportError` o `ModuleNotFoundError`
- Logs: `Dockerfile failed`

**Causa probable:**
- requirements.txt outdated
- Dependencia incompatible con Python 3.10
- Cache corrupta

**Solución:**
Rebuild sin cache
docker build --no-cache -t thea-ia:dev .

Actualizar requirements
pip install -U pip
pip freeze > requirements.txt

Verificar compatibilidad
python -m pip install -r requirements.txt --dry-run

text

---

### 9. Logs no visibles en Loki

**Síntomas:**
- Loki up pero sin logs
- Grafana: `No data` en Loki datasource

**Causa probable:**
- Promtail no scrapeando logs
- Labels incorrectas
- App no mandando logs

**Solución:**
Verificar Promtail
docker ps | grep promtail

Check config Promtail
cat /etc/promtail/config.yml

Mandar log de prueba
echo "test log" | logger

Query Loki
curl 'http://localhost:3100/loki/api/v1/query?query={job="thea-ia"}'

text

---

### 10. Performance degradada (latencia > 100ms)

**Síntomas:**
- FSM transiciones lentasrandom (`> 10ms`)
- Queries DB lentass (`> 100ms`)
- Requests Telegram timeout

**Causa probable:**
- DB queries sin índices
- Memory leak
- CPU saturada

**Solución:**
Check CPU/Memory
docker stats thea-ia

Analizar queries lentas
psql $DATABASE_URL -c "
SELECT query, calls, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC LIMIT 5;
"

Crear índices
psql $DATABASE_URL < scripts/create_indexes.sql

Profile app
python -m cProfile -s cumtime src/theaia/api.py

Usar APM (H11)
Agregar Jaeger tracing
from opentelemetry import trace

... configure Jaeger
text

---

## 📋 Checklist de Debug

- [ ] Revisar logs: `docker logs thea-ia`
- [ ] Verificar DB: `psql $DATABASE_URL -c "SELECT 1"`
- [ ] Ping app: `curl http://localhost:8000/health`
- [ ] Métricas: `curl http://localhost:8000/metrics`
- [ ] Traces: `jaeger-ui:16686`
- [ ] Resetear contexto si FSM stuck
- [ ] Limpiar cache Docker si build falla
- [ ] Restart pod si todo falla: `kubectl rollout restart deployment/thea-ia`

---

## 🆘 Escalación

Si problema persiste:
1. Guardar logs: `docker logs thea-ia > debug.log`
2. Export metrics: `curl http://localhost:9090/api/v1/query_range?query=...`
3. Create issue: https://github.com/thea-ia/thea-ia/issues
4. Mencionar: versión, reproducción, logs, metrics

---

## 📖 Documentación relacionada

- [Quickstart](./quickstart.md) — Setup inicial
- [Deployment](./deployment.md) — Producción
- [Architecture](../architecture/overview.md) — Entender diseño
- [Roadmap](../roadmap/master.md) — Plan completo

---

**Última actualización:** 2025-10-31 03:25 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)
