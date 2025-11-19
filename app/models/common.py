from pydantic import BaseModel
from typing import List
from models.koujyou import KoujyouReact

class GenericError(BaseModel):
  level: str = ""
  message: str = ""

class CommitRecordError(BaseModel):
  record: KoujyouReact = KoujyouReact()
  level: str = ""
  message: str = ""
  detail: str = ""
  code: str = ""

class ErrorResponse(BaseModel):
  errorList: List[CommitRecordError]