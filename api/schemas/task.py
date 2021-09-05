from typing import Optional

from pydantic import BaseModel, Field

#BaseModel はFastAPIのスキーマモデル
class TaskBase(BaseModel):
    #int,Optional[str], boolは型ヒントを表す
    #Noneはデフォルト値を表している
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")



class TaskCreate(TaskBase):
    pass



class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        #orm_mode = True は、このレスポンススキーマ TaskCreateResponse が、暗黙的にORMを受け取り、レスポンススキーマに変換することを意味します。
        orm_mode = True



class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True