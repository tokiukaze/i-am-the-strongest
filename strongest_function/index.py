from http import HTTPStatus
from typing import Any
from uuid import uuid4

from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    Response,
    content_types,
)
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.utilities.typing import LambdaContext

app = APIGatewayRestResolver()


def handler(event: Any, context: LambdaContext) -> Any:
    return app.resolve(event, context)


@app.get("/status")
def get_helth() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/new-genesis")
def post_new_genesis() -> Response:
    custom_headers = {"uuid4": f"{uuid4()}"}
    return Response(
        status_code=HTTPStatus.OK.value,  # 200
        content_type=content_types.APPLICATION_JSON,
        body=app.current_event.body,  # bodyをそのまま返却する
        headers=custom_headers,
    )


@app.put("/new-genesis/i-am-invincible")
def put_i_am_invincible() -> None:
    raise BadRequestError("未実装")
