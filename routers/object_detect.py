from fastapi import APIRouter

router=APIRouter(
    prefix='/detect'
)

@router.get('/')
def index():
    return 'Hello world'