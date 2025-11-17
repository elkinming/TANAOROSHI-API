from pydantic import BaseModel
from typing import List

class GenericError(BaseModel):
  level: str = ""
  message: str = ""

class CommitRecordError(BaseModel):
  uuid: str = ""
  level: str = ""
  message: str = ""
  detail: str = ""
  code: str = ""

class ErrorResponse(BaseModel):
  errorList: List[CommitRecordError]