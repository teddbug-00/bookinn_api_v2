from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel

from app.models.activities import ActivityType, ActivityAction

class ActivityResponse(BaseModel):
    id: UUID
    type: ActivityType
    action: ActivityAction
    entity_type: Optional[str] = None
    entity_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime