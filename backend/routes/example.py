from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])

@router.get("/hello")
async def hello_javi():
    return {"message": "hola javi"}
