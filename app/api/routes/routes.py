from fastapi import APIRouter

routes=APIRouter(prefix="/api/v1")

@routes.get("/health")
def health_check():
    return {"status": "ok"}