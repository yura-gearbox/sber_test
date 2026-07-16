from pydantic import BaseModel, IPvAnyAddress, Field
from pydantic.networks import AnyUrl


class BaseResponse(BaseModel):
    args: dict[str, str]
    headers: dict[str, str]
    origin: IPvAnyAddress
    url: AnyUrl


class BaseResponseExt(BaseResponse):
    data: str
    files: dict[str, str]
    form: dict[str, str]


class GetResponse(BaseResponse):
    pass


class PostResponse(BaseResponseExt):
    pass


class PostResponseJson(BaseResponseExt):
    json_data: dict[str, str] = Field(..., alias="json")


class PostResponseForm(BaseResponseExt):
    json_data: None = Field(..., alias="json")


class PostResponseFile(BaseResponseExt):
    json_data: None = Field(..., alias="json")


class GetResponseWithDelay(BaseResponseExt):
    pass

