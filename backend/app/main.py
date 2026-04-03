from dotenv import load_dotenv

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions.exceptions import BaseAppException                   
from app.utils.logger import logger
from app.controllers import auth_controller, user_controller, grade_controller, purchase_controller, boiling_controller, humidifying_controller, drying_controller, husk_return_controller, peeling_after_drying_controller, peeling_before_drying_controller, production_controller, husk_rejection_sales_controller, rcn_sales_controller, cashew_kernel_sales_controller, cashew_shell_sales_controller, batch_controller, reports_controller

# creates your web application.
app = FastAPI() 

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create a versioned router
api_v1_router = APIRouter(prefix="/api/v1")

# Include all your routers under this versioned router
api_v1_router.include_router(auth_controller.router) 
api_v1_router.include_router(user_controller.router) 
api_v1_router.include_router(grade_controller.router)
api_v1_router.include_router(purchase_controller.router)
api_v1_router.include_router(boiling_controller.router)
api_v1_router.include_router(drying_controller.router)
api_v1_router.include_router(humidifying_controller.router)
api_v1_router.include_router(peeling_before_drying_controller.router)
api_v1_router.include_router(peeling_after_drying_controller.router)
api_v1_router.include_router(husk_return_controller.router)
api_v1_router.include_router(production_controller.router)
api_v1_router.include_router(rcn_sales_controller.router)
api_v1_router.include_router(husk_rejection_sales_controller.router)
api_v1_router.include_router(cashew_kernel_sales_controller.router)
api_v1_router.include_router(cashew_shell_sales_controller.router)
api_v1_router.include_router(batch_controller.router)
api_v1_router.include_router(reports_controller.router)

# Mount the versioned router to the app
app.include_router(api_v1_router)

# Generic handler for all custom exceptions
@app.exception_handler(BaseAppException)
async def base_exception_handler(request: Request, exc: BaseAppException):
    logger.error(f"{exc.__class__.__name__}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errors": [
                { "field": exc.field if hasattr(exc, "field") else "general", 
                  "message": exc.message }
            ]
        }
    )

# Specific handler for FastAPI validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    errors = [
        {
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"]
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={ "errors": errors }
    )