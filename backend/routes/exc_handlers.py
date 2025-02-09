import starlette.requests
from starlette.responses import JSONResponse

from backend.exceptions import (AlreadyExists, InvalidParameters,
                                MissingParameters, ObjectNotFound)
from backend.schemas.base import StatusResponseModel

from .base import app


@app.exception_handler(ObjectNotFound)
async def not_found_handler(req: starlette.requests.Request, exc: ObjectNotFound):
    return JSONResponse(
        content=StatusResponseModel(
            status="Error", message=exc.eng, ru=exc.ru
        ).model_dump(),
        status_code=404,
    )


@app.exception_handler(AlreadyExists)
async def already_exists_handler(req: starlette.requests.Request, exc: AlreadyExists):
    return JSONResponse(
        content=StatusResponseModel(
            status="Error", message=exc.eng, ru=exc.ru
        ).model_dump(),
        status_code=409,
    )


@app.exception_handler(MissingParameters)
async def missing_parameter_handler(
    req: starlette.requests.Request, exc: MissingParameters
):
    return JSONResponse(
        content=StatusResponseModel(
            status="Error", message=exc.eng, ru=exc.ru
        ).model_dump(),
        status_code=400,
    )


@app.exception_handler(InvalidParameters)
async def invalid_parameter_handler(
    req: starlette.requests.Request, exc: InvalidParameters
):
    return JSONResponse(
        content=StatusResponseModel(
            status="Error", message=exc.eng, ru=exc.ru
        ).model_dump(),
        status_code=400,
    )
