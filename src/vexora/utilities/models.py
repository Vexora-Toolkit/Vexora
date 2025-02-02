"""Base models for vexora."""

from pydantic import BaseModel, ConfigDict


class vexoraModel(BaseModel):
    """Base model for all vexora models.

    This model:
    - Is strict (no extra fields allowed)
    - Uses modern Pydantic v2 features
    """

    model_config = ConfigDict(
        extra="forbid",  # no extra fields allowed
        frozen=False,  # allow mutation
        validate_assignment=True,  # validate on attribute assignment
        validate_default=True,  # validate default values
    )
