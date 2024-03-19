from fastapi import APIRouter


health_check_router = APIRouter(prefix="/health", tags=["Health Check"])


@health_check_router.get("")
def health_check() -> dict[str, str]:
    return { "msg" : "Health check passed"}

