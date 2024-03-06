from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import products_router, owners_route, categories_router
from models import models
from db.DBConnection import engine


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

    def add_middlewares(self) -> None:
        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    def create_models(self) -> None:
        try:
            models.Base.metadata.create_all(engine)
        except Exception as e:
            print(e.args)
