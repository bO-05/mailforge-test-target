```python
from fastapi import FastAPI, HTTPException
from datetime import datetime
import pytz

app = FastAPI()

@app.get("/current-time")
async def get_current_time(timezone: str = "UTC"):
    """
    Returns the current time in the specified timezone.

    Args:
        timezone (str): The timezone to get the current time for. Defaults to "UTC".

    Returns:
        dict: A dictionary containing the current time in the specified timezone.

    Raises:
        HTTPException: If the provided timezone is invalid.
    """
    try:
        # Get the timezone object
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(status_code=400, detail="Invalid timezone")

    # Get the current time in the specified timezone
    current_time = datetime.now(tz)

    return {"current_time": current_time.isoformat()}

```