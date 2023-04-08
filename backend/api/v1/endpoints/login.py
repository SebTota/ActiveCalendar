from fastapi import APIRouter

router = APIRouter()


@router.post("/login/test")
def login_test():
    return 'yay! it works!'