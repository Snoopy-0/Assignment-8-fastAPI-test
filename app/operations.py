import logging

logger = logging.getLogger(__name__)

def add(a: float, b: float) -> float:
    logger.info("add called with a=%s, b=%s", a, b)
    return a + b

def subtract(a: float, b: float) -> float:
    logger.info("subtract called with a=%s, b=%s", a, b)
    return a - b

def multiply(a: float, b: float) -> float:
    logger.info("multiply called with a=%s, b=%s", a, b)
    return a * b

def divide(a: float, b: float) -> float:
    logger.info("divide called with a=%s, b=%s", a, b)
    if b == 0:
        logger.error("Attempted division by zero")
        raise ValueError("Division by zero is not allowed.")
    return a / b