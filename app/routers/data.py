from fastapi import APIRouter, HTTPException, Query
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from app.utils import cache, is_rate_limited
from app.auth import get_current_user
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

ALERTS_API_TOKEN = os.getenv("ALERTS_API_TOKEN")

router = APIRouter()

@router.get("/alerts-state")
async def get_alerts(token: str = Query(...)):
    current_user = await get_current_user(token)
    username = current_user["username"]
    print(f"User {username} requested alerts")

    if "data" in cache:
        return cache["data"]

    if is_rate_limited():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    alerts_client = AsyncAlertsClient(token=ALERTS_API_TOKEN)
    try:
        active_alerts = await asyncio.wait_for(
            alerts_client.get_air_raid_alert_statuses_by_oblast(), timeout=10
        )
        cache["data"] = active_alerts
        return active_alerts
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request to Alerts API timed out")
