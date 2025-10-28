from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from fastapi.exceptions import RequestValidationError
from app.operations import add, subtract, multiply, divide
import uvicorn
import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("calculator")

app = FastAPI(title="FastAPI Calculator", version="1.0.0", description="A simple calculator with FastAPI")
templates = Jinja2Templates(directory="templates")

class Operation(BaseModel):
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")

    @field_validator("a", "b")
    @classmethod
    def numbers_only(cls, v: Any) -> Any:
        if isinstance(v, (int, float)):
            return v
        raise ValueError("Operands must be numbers")

class OperationResponse(BaseModel):
    result: float

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("Validation error: %s", exc)
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.get("/", response_class=HTMLResponse, tags=["ui"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, tags=["operations"])
async def add_route(operation: Operation):
    try:
        result = add(operation.a, operation.b)
        logger.info("Add %s + %s = %s", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except Exception as e:
        logger.exception("Add internal error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/subtract", response_model=OperationResponse, tags=["operations"])
async def subtract_route(operation: Operation):
    try:
        result = subtract(operation.a, operation.b)
        logger.info("Subtract %s - %s = %s", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except Exception:
        logger.exception("Subtract internal error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/multiply", response_model=OperationResponse, tags=["operations"])
async def multiply_route(operation: Operation):
    try:
        result = multiply(operation.a, operation.b)
        logger.info("Multiply %s * %s = %s", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except Exception:
        logger.exception("Multiply internal error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/divide", response_model=OperationResponse, tags=["operations"])
async def divide_route(operation: Operation):
    try:
        result = divide(operation.a, operation.b)
        logger.info("Divide %s / %s = %s", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except ValueError as e:
        logger.warning("Bad request on divide: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Divide internal error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)