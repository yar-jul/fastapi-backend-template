from fastapi import APIRouter

from . import author, book, category, tag

router = APIRouter()
router.include_router(
    author.router,
    prefix="/author",
    tags=["author"],
)
router.include_router(
    category.router,
    prefix="/category",
    tags=["category"],
)
router.include_router(
    tag.router,
    prefix="/tag",
    tags=["tag"],
)
router.include_router(
    book.router,
    prefix="/book",
    tags=["book"],
)
