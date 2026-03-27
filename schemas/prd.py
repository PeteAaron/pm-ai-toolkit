from pydantic import BaseModel, Field


class PRDOutput(BaseModel):
    title: str
    problem_statement: str
    user_segments: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
