import logging
from sqlalchemy import event
from app import db

# Logger para terminal e arquivo
logger = logging.getLogger('sqlalchemy')
logger.setLevel(logging.INFO)

# Log no terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Log em arquivo
file_handler = logging.FileHandler('logs/operacoes_banco.log')
file_handler.setLevel(logging.INFO)

# Formatação
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Adiciona handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

@event.listens_for(db.session, 'after_flush')
def log_operacoes(session, flush_context):
    for instance in session.new:
        logger.info(f"[INSERT] {instance.__class__.__name__} - {instance.__dict__}")
    for instance in session.dirty:
        if session.is_modified(instance):
            logger.info(f"[UPDATE] {instance.__class__.__name__} - {instance.__dict__}")
    for instance in session.deleted:
        logger.info(f"[DELETE] {instance.__class__.__name__} - {instance.__dict__}")
