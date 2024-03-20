from typing import Dict

from app.presentation.helpers.custom_router import APICustomRouter

router = APICustomRouter(prefix="/health")


@router.get("")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
