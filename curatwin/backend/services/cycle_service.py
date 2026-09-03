from datetime import datetime, timedelta


def estimate_phase(cycle_start: datetime, cycle_length: int = 28, reference_date: datetime = None) -> str:
    if reference_date is None:
        reference_date = datetime.utcnow()

    days_since_start = (reference_date - cycle_start).days
    if days_since_start < 0:
        return "pre_cycle"

    day_in_cycle = days_since_start % cycle_length

    if day_in_cycle <= 5:
        return "menstrual"
    elif day_in_cycle <= 13:
        return "follicular"
    elif day_in_cycle <= 16:
        return "ovulation"
    elif day_in_cycle <= cycle_length - 1:
        return "luteal"
    return "pre_menstrual"


def get_cycle_insights(cycle_start: datetime, cycle_length: int = 28) -> dict:
    phase = estimate_phase(cycle_start, cycle_length)

    phase_info = {
        "menstrual": {
            "description": "Menstrual phase",
            "energy": "lower",
            "study_suggestion": "Light study sessions, take frequent breaks, stay hydrated.",
            "mood_note": "You may feel more tired than usual — this is normal."
        },
        "follicular": {
            "description": "Follicular phase",
            "energy": "rising",
            "study_suggestion": "Good time for focused study and tackling challenging tasks.",
            "mood_note": "Energy and focus typically improve during this phase."
        },
        "ovulation": {
            "description": "Ovulation phase",
            "energy": "peak",
            "study_suggestion": "Peak cognitive performance — ideal for exams or presentations.",
            "mood_note": "You may feel more social and confident."
        },
        "luteal": {
            "description": "Luteal phase",
            "energy": "declining",
            "study_suggestion": "Moderate study pace, prioritize rest and self-care.",
            "mood_note": "Mood may fluctuate — be gentle with yourself."
        },
        "pre_menstrual": {
            "description": "Pre-menstrual phase",
            "energy": "low",
            "study_suggestion": "Reduce workload if possible, focus on lighter review tasks.",
            "mood_note": "PMS symptoms may appear — prioritize comfort and rest."
        },
        "pre_cycle": {
            "description": "Before cycle start",
            "energy": "normal",
            "study_suggestion": "Normal study schedule.",
            "mood_note": ""
        }
    }

    return phase_info.get(phase, phase_info["pre_cycle"])
