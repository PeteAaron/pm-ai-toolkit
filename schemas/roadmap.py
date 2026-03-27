from pydantic import BaseModel, Field, model_validator


class RoadmapItem(BaseModel):
    initiative_name: str
    impact: int = Field(ge=1, le=10, description="Impact score 1–10")
    effort: int = Field(ge=1, le=10, description="Effort score 1–10 (higher = more effort)")
    confidence: int = Field(ge=1, le=10, description="Confidence score 1–10")
    rationale: str
    priority_score: float = Field(default=0.0, description="Computed: (impact × confidence) / effort")

    @model_validator(mode="after")
    def compute_priority_score(self) -> "RoadmapItem":
        if self.effort > 0:
            self.priority_score = round((self.impact * self.confidence) / self.effort, 2)
        return self
