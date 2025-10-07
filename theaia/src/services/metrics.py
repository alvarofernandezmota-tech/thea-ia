from prometheus_client import Counter, Histogram, start_http_server

# Métricas
REQUEST_COUNT = Counter(
    'thea_requests_total',
    'Total de solicitudes procesadas'
)
REQUEST_LATENCY = Histogram(
    'thea_request_latency_seconds',
    'Latencia de procesamiento de solicitudes'
)

def record_request(func):
    """Decorador para contar y medir latencia de cada llamada."""
    def wrapper(*args, **kwargs):
        REQUEST_COUNT.inc()
        with REQUEST_LATENCY.time():
            return func(*args, **kwargs)
    return wrapper

def start_metrics_server(port: int = 8000):
    """Inicia el servidor HTTP de métricas en el puerto dado."""
    start_http_server(port)
