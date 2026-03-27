from pydantic import BaseModel, Field


class MeetingSummary(BaseModel):
    summary: str
    decisions: list[str] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list)
    owners: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
