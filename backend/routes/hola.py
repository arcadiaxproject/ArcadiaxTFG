from fastapi import APIRouter

router = APIRouter()

@router.get("/hola")
async def hola():
    return {"mensaje": "hola"}
