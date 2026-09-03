from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import numpy as np
from ..database import get_db
from ..models.user import User
from ..models.wellness import WellnessData
from ..models.stress import StressPrediction
from ..models.mood import MoodCheckin
from ..models.cycle import CycleRecord
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/insights", tags=["insights"])

@router.get("/overview")
def get_overview(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    wellness_week = db.query(WellnessData).filter(
        WellnessData.user_id == user.id, WellnessData.timestamp >= week_ago
    ).all()
    
    stress_week = db.query(StressPrediction).filter(
        StressPrediction.user_id == user.id, StressPrediction.timestamp >= week_ago
    ).all()
    
    moods_week = db.query(MoodCheckin).filter(
        MoodCheckin.user_id == user.id, MoodCheckin.created_at >= week_ago
    ).all()
    
    moods_month = db.query(MoodCheckin).filter(
        MoodCheckin.user_id == user.id, MoodCheckin.created_at >= month_ago
    ).all()
    
    result = {"period": "7_days", "has_data": False}
    
    if wellness_week:
        result["has_data"] = True
        result["avg_heart_rate"] = round(np.mean([w.heart_rate for w in wellness_week if w.heart_rate > 0]), 1)
        result["avg_hrv"] = round(np.mean([w.ppg_hrv for w in wellness_week]), 1)
        result["avg_skin_temp"] = round(np.mean([w.skin_temp for w in wellness_week]), 2)
        result["avg_gsr"] = round(np.mean([w.gsr_amplitude for w in wellness_week]), 2)
    
    if stress_week:
        result["has_data"] = True
        stress_counts = {"low": 0, "moderate": 0, "high": 0}
        for s in stress_week:
            stress_counts[s.stress_level] = stress_counts.get(s.stress_level, 0) + 1
        result["stress_distribution"] = stress_counts
        dominant = max(stress_counts, key=stress_counts.get)
        result["dominant_stress"] = dominant
    
    if moods_week:
        result["has_data"] = True
        result["avg_mood"] = round(np.mean([m.mood for m in moods_week]) * 100, 1)
        result["avg_sleep"] = round(np.mean([m.sleep_quality for m in moods_week]) * 100, 1)
        result["avg_energy"] = round(np.mean([m.energy_level for m in moods_week]) * 100, 1)
        result["avg_stress_perception"] = round(np.mean([m.perceived_stress for m in moods_week]) * 100, 1)
    
    if moods_month:
        result["monthly_mood_trend"] = []
        by_day = {}
        for m in moods_month:
            day_key = m.created_at.strftime("%Y-%m-%d") if m.created_at else "unknown"
            if day_key not in by_day:
                by_day[day_key] = []
            by_day[day_key].append(m.mood)
        for day in sorted(by_day.keys()):
            result["monthly_mood_trend"].append({
                "date": day,
                "mood": round(np.mean(by_day[day]) * 100, 1)
            })
    
    return result

@router.get("/stress-trend")
def stress_trend(days: int = 14, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(StressPrediction).filter(
        StressPrediction.user_id == user.id,
        StressPrediction.timestamp >= since
    ).order_by(StressPrediction.timestamp.asc()).all()
    
    trend = []
    for r in records:
        trend.append({
            "timestamp": r.timestamp.isoformat(),
            "stress_level": r.stress_level,
            "confidence": r.confidence
        })
    return {"trend": trend, "count": len(trend)}

@router.get("/mood-trend")
def mood_trend(days: int = 30, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(MoodCheckin).filter(
        MoodCheckin.user_id == user.id,
        MoodCheckin.created_at >= since
    ).order_by(MoodCheckin.created_at.asc()).all()
    
    trend = []
    for r in records:
        trend.append({
            "date": r.created_at.isoformat(),
            "mood": r.mood,
            "stress": r.perceived_stress,
            "sleep": r.sleep_quality,
            "energy": r.energy_level
        })
    return {"trend": trend, "count": len(trend)}
