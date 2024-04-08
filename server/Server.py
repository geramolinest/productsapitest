from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from routes import products_router, owners_route, categories_router, health_check
from models import models
from db.DBConnection import engine
from middlewares.exceptions_middleware import ExceptionMiddleware, validation_error_handler


class Server:
    def __init__(self) -> None:
        self.server = FastAPI()
        self.include_routes()
        self.add_middlewares()
        self.create_models()

    def include_routes(self) -> None:
        self.server.include_router(products_router.products_router)
        self.server.include_router(owners_route.owners_router)
        self.server.include_router(categories_router.categories_router)
        self.server.include_router(health_check.health_check_router)

    def add_middlewares(self) -> None:
        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        self.server.add_middleware(ExceptionMiddleware)
        self.server.add_exception_handler(RequestValidationError, validation_error_handler)

    def create_models(self) -> None:
        try:
            models.Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(e.args)
