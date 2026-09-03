import random

COPING_LIBRARY = {
    "breathing": [
        {"title": "4-7-8 Breathing", "content": "Breathe in for 4 seconds, hold for 7 seconds, exhale slowly for 8 seconds. Repeat 4 times. This activates your parasympathetic nervous system and helps calm your body."},
        {"title": "Box Breathing", "content": "Inhale for 4 seconds, hold for 4 seconds, exhale for 4 seconds, hold for 4 seconds. Repeat for 2 minutes. Used by professionals to manage acute stress."},
        {"title": "Diaphragmatic Breathing", "content": "Place one hand on your chest and one on your belly. Breathe deeply through your nose so your belly rises. Exhale slowly through pursed lips. Do this for 5 minutes."},
    ],
    "mindfulness": [
        {"title": "5-4-3-2-1 Grounding", "content": "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. This brings your attention to the present moment."},
        {"title": "Body Scan Meditation", "content": "Close your eyes. Slowly focus attention on each body part from your toes to your head. Notice any tension and gently release it. Takes 5-10 minutes."},
        {"title": "Mindful Walking", "content": "Walk slowly and pay attention to each step — the feeling of your feet touching the ground, the rhythm of your breath. Even 5 minutes can reset your stress response."},
    ],
    "cbt_reframing": [
        {"title": "Thought Record", "content": "Write down: 1) The stressful thought, 2) The emotion and intensity (0-100), 3) Evidence for the thought, 4) Evidence against it, 5) A balanced alternative thought. This helps challenge unhelpful thinking patterns."},
        {"title": "Worst-Case Check", "content": "Ask yourself: What is the worst that could happen? How likely is it? What would I do if it happened? Have I handled difficult situations before? Often the worst case is more manageable than our anxiety suggests."},
        {"title": "Cognitive Defusion", "content": "Instead of 'I am stressed,' try 'I notice I am having the thought that I am stressed.' This creates distance between you and the thought, reducing its power over you."},
    ],
    "stretching": [
        {"title": "Desk Stretches", "content": "Neck rolls (5 each direction), shoulder shrugs (10 reps), seated spinal twist (30 seconds each side), wrist circles (10 each direction). Takes 3 minutes and reduces physical tension."},
        {"title": "Standing Reset", "content": "Stand up, reach arms overhead, gently lean side to side, do 10 calf raises, and roll your shoulders back 10 times. A quick physical reset between study sessions."},
    ],
    "study_breaks": [
        {"title": "Pomodoro Reset", "content": "Set a 25-minute focused study timer. When it rings, take a 5-minute break: stand, stretch, drink water, look out a window. After 4 cycles, take a 15-30 minute break."},
        {"title": "Micro-Break Protocol", "content": "Every 20 minutes, look at something 20 feet away for 20 seconds (20-20-20 rule). Every hour, take a 5-minute walk. This prevents mental fatigue buildup."},
    ],
    "sleep_hygiene": [
        {"title": "Wind-Down Routine", "content": "1 hour before bed: dim lights, stop screens, do a calming activity (reading, gentle stretching). Keep your room cool and dark. Aim for 7-9 hours of sleep consistently."},
        {"title": "Sleep Reset", "content": "If you can't sleep after 20 minutes, get up and do something quiet in dim light. Return to bed when sleepy. Avoid checking the clock. Keep the same wake time every day."},
    ],
    "emotional_stabilization": [
        {"title": "SAFE Technique", "content": "S - Slow down. A - Acknowledge your feelings. F - Feel your body (feet on floor). E - Engage with the present. Use this when emotions feel overwhelming."},
        {"title": "Butterfly Hug", "content": "Cross your arms over your chest. Alternately tap your shoulders in a slow, rhythmic pattern while breathing deeply. Continue for 2-3 minutes. This bilateral stimulation helps process difficult emotions."},
    ],
    "career_anxiety": [
        {"title": "Skills Inventory", "content": "List 5 skills you already have, 3 you're developing, and 2 you want to learn. Create one small action for this week toward a skill goal. Career anxiety often shrinks when we see our progress."},
        {"title": "Future Self Letter", "content": "Write a short letter to yourself 2 years from now. Describe what you hope to have learned and experienced. This helps reframe current uncertainty as part of a longer journey."},
    ],
    "digital_safety": [
        {"title": "Digital Boundary Setting", "content": "Review your social media privacy settings. Mute or unfollow accounts that trigger comparison or anxiety. Set a daily social media time limit. Your online space should support your well-being."},
        {"title": "Online Harassment Response", "content": "If experiencing harassment: 1) Don't respond, 2) Screenshot evidence, 3) Block and report, 4) Talk to someone you trust, 5) Contact campus support if needed. You deserve to feel safe online."},
    ],
}


def get_recommendations(stress_level: str = "moderate", cycle_phase: str = "", count: int = 3) -> list:
    if stress_level == "high":
        priority = ["breathing", "emotional_stabilization", "mindfulness"]
    elif stress_level == "moderate":
        priority = ["breathing", "study_breaks", "cbt_reframing"]
    else:
        priority = ["mindfulness", "stretching", "study_breaks"]

    if cycle_phase in ["menstrual", "pre_menstrual"]:
        priority = ["stretching", "sleep_hygiene", "mindfulness"]

    recs = []
    for cat in priority:
        items = COPING_LIBRARY.get(cat, [])
        if items:
            item = random.choice(items)
            recs.append({
                "category": cat,
                "title": item["title"],
                "recommendation": item["content"],
                "intervention_type": f"auto_{cat}"
            })

    while len(recs) < count:
        for cat in COPING_LIBRARY:
            if cat not in priority:
                items = COPING_LIBRARY[cat]
                item = random.choice(items)
                recs.append({
                    "category": cat,
                    "title": item["title"],
                    "recommendation": item["content"],
                    "intervention_type": f"auto_{cat}"
                })
                if len(recs) >= count:
                    break

    return recs[:count]


def get_library_categories() -> dict:
    return {cat: [{"title": i["title"], "content": i["content"]} for i in items] for cat, items in COPING_LIBRARY.items()}
