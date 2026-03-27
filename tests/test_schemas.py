import pytest
from pydantic import ValidationError

from schemas.meeting import MeetingSummary
from schemas.prd import PRDOutput
from schemas.roadmap import RoadmapItem


def test_prd_valid():
    prd = PRDOutput(
        title="Export to PDF",
        problem_statement="Users cannot share reports externally.",
        user_segments=["analysts"],
        goals=["Reduce time to share reports"],
    )
    assert prd.title == "Export to PDF"
    assert prd.risks == []  # default_factory list


def test_prd_missing_required_field():
    with pytest.raises(ValidationError):
        PRDOutput(problem_statement="Missing title field")


def test_prd_defaults_are_empty_lists():
    prd = PRDOutput(title="T", problem_statement="P")
    assert prd.user_segments == []
    assert prd.goals == []
    assert prd.assumptions == []
    assert prd.risks == []
    assert prd.open_questions == []


def test_meeting_valid():
    m = MeetingSummary(
        summary="Discussed Q2 roadmap priorities.",
        decisions=["Ship feature X in May"],
        action_items=["Write spec for feature X"],
        owners=["Alice"],
    )
    assert m.risks == []


def test_meeting_missing_required_field():
    with pytest.raises(ValidationError):
        MeetingSummary(decisions=["Something"])


def test_roadmap_priority_score_computed():
    item = RoadmapItem(
        initiative_name="Search",
        impact=8,
        effort=4,
        confidence=5,
        rationale="High user demand, low technical risk.",
    )
    assert item.priority_score == round((8 * 5) / 4, 2)


def test_roadmap_score_out_of_range():
    with pytest.raises(ValidationError):
        RoadmapItem(
            initiative_name="X", impact=11, effort=5, confidence=5, rationale="test"
        )


def test_roadmap_score_minimum_values():
    item = RoadmapItem(
        initiative_name="Low priority",
        impact=1,
        effort=10,
        confidence=1,
        rationale="Barely worth doing.",
    )
    assert item.priority_score == round((1 * 1) / 10, 2)
