import logging
from wsgiref.simple_server import make_server
from spyne.server.wsgi import WsgiApplication
from .soap_service import application

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        wsgi_app = WsgiApplication(application)
        server = make_server("127.0.0.1", 8001, wsgi_app)
        logger.info("SOAP service running on http://127.0.0.1:8001")
        server.serve_forever()
    except Exception as e:
        logger.error(f"SOAP Service failed to start: {e}")
