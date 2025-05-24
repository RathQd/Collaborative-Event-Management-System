from typing import Any
from app.model.eventversion import EventVersion

async def compare_event_versions(version1: EventVersion, version2: EventVersion) -> dict[str, dict[str, Any]]:
        diffs = {}
        exclude_fields = {"id", "version_id", "edited_at"}  
        
        for field in version1.__fields__:
            if field in exclude_fields:
                continue

            val1 = getattr(version1, field)
            val2 = getattr(version2, field)

            if val1 != val2:
                diffs[field] = {
                    "old": val1,
                    "new": val2
                }

        return diffs