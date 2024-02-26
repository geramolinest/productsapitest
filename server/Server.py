from fastapi import FastAPI
from routes.products_router import  products_router

class Server:
    def __init__(self) -> None:
        self.server = FastAPI()
        self.include_routes()

    def include_routes(self) -> None:
        self.server.include_router(products_router)

    def middlewares(self) -> None:
        pass
