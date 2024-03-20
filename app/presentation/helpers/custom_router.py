# mypy: disable-error-code="no-any-return"
from typing import Any, Callable, Coroutine

from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute, APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.domain.shared.custom_exceptions import DomainException, InfraException, NotFoundException


class CustomRouter(APIRoute):
    def get_route_handler(  # type: ignore
        self,
    ) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                response: Response = await original_route_handler(request)
            except DomainException as exception:
                response = __to_json_response(status.HTTP_400_BAD_REQUEST, exception)
            except NotFoundException as exception:
                response = __to_json_response(status.HTTP_404_NOT_FOUND, exception)
            except InfraException as exception:
                response = __to_json_response(status.HTTP_500_INTERNAL_SERVER_ERROR, exception)
            except Exception as exception:
                response = __to_json_response(status.HTTP_500_INTERNAL_SERVER_ERROR, exception)

            return response

        def __to_json_response(status_code: int, exception: Exception) -> JSONResponse:
            return JSONResponse(
                status_code=status_code,
                content=jsonable_encoder({"description": str(exception)}),
            )

        return custom_route_handler


class APICustomRouter(APIRouter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.route_class = CustomRouter
