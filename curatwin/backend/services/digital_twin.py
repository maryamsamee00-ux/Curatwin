from sqlalchemy.orm import Session
from ..models.wellness import WellnessData
from ..models.stress import StressPrediction
from ..models.mood import MoodCheckin
from ..models.cycle import CycleRecord
from datetime import datetime, timedelta
import numpy as np


def compute_digital_twin(user_id: int, db: Session) -> dict:
    now = datetime.utcnow()
    day_ago = now - timedelta(hours=24)

    recent_wellness = db.query(WellnessData).filter(
        WellnessData.user_id == user_id,
        WellnessData.timestamp >= day_ago
    ).order_by(WellnessData.timestamp.desc()).limit(20).all()

    recent_stress = db.query(StressPrediction).filter(
        StressPrediction.user_id == user_id,
        StressPrediction.timestamp >= day_ago
    ).order_by(StressPrediction.timestamp.desc()).limit(10).all()

    recent_moods = db.query(MoodCheckin).filter(
        MoodCheckin.user_id == user_id,
        MoodCheckin.created_at >= day_ago
    ).order_by(MoodCheckin.created_at.desc()).limit(5).all()

    # Compute wellness score (0-100, higher = better)
    score = 50.0  # baseline

    if recent_wellness:
        avg_hrv = np.mean([w.ppg_hrv for w in recent_wellness])
        avg_gsr = np.mean([w.gsr_amplitude for w in recent_wellness])
        avg_temp = np.mean([w.skin_temp for w in recent_wellness])
        # Higher HRV = better wellness
        score += min(avg_hrv - 50, 20)
        # Lower GSR = less stress
        score -= max(avg_gsr - 5, 0) * 3
        # Normal temp = better
        score -= abs(avg_temp - 36.5) * 10

    if recent_stress:
        stress_vals = {"low": 20, "moderate": 0, "high": -20}
        avg_stress_impact = np.mean([stress_vals.get(s.stress_level, 0) for s in recent_stress])
        score += avg_stress_impact * 0.3

    if recent_moods:
        avg_mood = np.mean([m.mood for m in recent_moods])
        avg_sleep = np.mean([m.sleep_quality for m in recent_moods])
        score += (avg_mood - 0.5) * 30
        score += (avg_sleep - 0.5) * 20

    score = max(0, min(100, score))

    if score >= 65:
        state = "well"
        stress_category = "Low"
    elif score >= 35:
        state = "moderate"
        stress_category = "Moderate"
    else:
        state = "stressed"
        stress_category = "High"

    # Cycle info
    cycle = db.query(CycleRecord).filter(
        CycleRecord.user_id == user_id
    ).order_by(CycleRecord.cycle_start.desc()).first()

    cycle_phase = ""
    if cycle and cycle.estimated_phase:
        cycle_phase = cycle.estimated_phase

    return {
        "wellness_score": round(score, 1),
        "state": state,
        "stress_category": stress_category,
        "cycle_phase": cycle_phase,
        "data_points_wellness": len(recent_wellness),
        "data_points_stress": len(recent_stress),
        "data_points_mood": len(recent_moods),
        "last_updated": now.isoformat(),
        "disclaimer": "This is an AI wellness estimate, not a clinical diagnosis."
    }
