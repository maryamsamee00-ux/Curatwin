from sqlalchemy.orm import Session
from ..models.mood import MoodCheckin
from ..models.stress import StressPrediction
from datetime import datetime, timedelta
import numpy as np


def estimate_affective_state(user_id: int, db: Session) -> dict:
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)

    moods = db.query(MoodCheckin).filter(
        MoodCheckin.user_id == user_id,
        MoodCheckin.created_at >= week_ago
    ).order_by(MoodCheckin.created_at.desc()).all()

    stress_preds = db.query(StressPrediction).filter(
        StressPrediction.user_id == user_id,
        StressPrediction.timestamp >= week_ago
    ).order_by(StressPrediction.timestamp.desc()).all()

    if not moods and not stress_preds:
        return {
            "affective_state": "insufficient_data",
            "mood_trend": "no_data",
            "burnout_risk": "unknown",
            "recommendation": "Complete your first private wellness check-in to begin tracking.",
            "disclaimer": "This is an AI wellness estimate, not a clinical diagnosis."
        }

    mood_score = 0.5
    stress_score = 0.5

    if moods:
        mood_score = np.mean([m.mood for m in moods])
        energy = np.mean([m.energy_level for m in moods])
        sleep = np.mean([m.sleep_quality for m in moods])
    else:
        energy = 0.5
        sleep = 0.5

    if stress_preds:
        stress_map = {"low": 0.2, "moderate": 0.5, "high": 0.8}
        stress_score = np.mean([stress_map.get(s.stress_level, 0.5) for s in stress_preds])

    composite = mood_score * 0.35 + (1 - stress_score) * 0.35 + energy * 0.15 + sleep * 0.15

    if composite >= 0.65:
        state = "positive"
        trend = "stable_well"
        burnout = "low"
        rec = "Your wellness trends look positive. Keep maintaining your healthy routines."
    elif composite >= 0.4:
        state = "mixed"
        trend = "fluctuating"
        burnout = "moderate"
        rec = "Some wellness indicators suggest you may benefit from a break or coping exercise."
    else:
        state = "concerned"
        trend = "declining"
        burnout = "elevated"
        rec = "Your recent patterns suggest elevated stress. Consider reaching out for support or trying a coping exercise."

    return {
        "affective_state": state,
        "mood_trend": trend,
        "composite_score": round(composite * 100, 1),
        "burnout_risk": burnout,
        "mood_score": round(mood_score * 100, 1),
        "stress_score": round(stress_score * 100, 1),
        "energy_score": round(energy * 100, 1),
        "sleep_score": round(sleep * 100, 1),
        "recommendation": rec,
        "disclaimer": "This is an AI wellness estimate, not a clinical diagnosis."
    }
