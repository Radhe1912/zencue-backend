import random

MESSAGES = {
    "water": [
        "Time to hydrate 💧",
        "Take a sip of water",
        "Your body needs water right now",
        "Stay hydrated, stay focused",
        "Drink water and refresh your mind",
        "Hydration break!",
        "Water keeps you going—drink some",
        "Pause and take a sip",
        "Don't forget your water intake",
        "Keep your energy up—drink water",
        "A quick water break won't hurt",
        "Fuel your body with water",
        "Hydrate before you feel thirsty",
        "Your brain works better hydrated",
        "Take care of yourself—drink water",
        "Stay fresh—have some water",
        "Small sip, big benefit",
        "Drink water for better focus",
        "Water break = productivity boost",
        "Refresh your system with water",
        "Hydration is self-care",
        "Drink water, feel better instantly",
        "Your future self says: drink water",
        "Stay cool, stay hydrated",
        "Water time 💙"
    ],

    "posture": [
        "Straighten your back 🧘",
        "Check your posture",
        "Sit upright and relax shoulders",
        "Align your neck properly",
        "Don't slouch—sit straight",
        "Posture reset time",
        "Keep your spine happy",
        "Lift your chest slightly",
        "Relax your shoulders down",
        "Neck alignment check",
        "Fix your sitting position",
        "Sit tall, breathe easy",
        "Your posture matters",
        "Correct your stance now",
        "Take pressure off your spine",
        "Posture improvement time",
        "Balance your sitting position",
        "Adjust your chair and sit straight",
        "Don't let tech neck win",
        "Keep your head aligned",
        "Strong posture = strong presence",
        "Sit like you mean it",
        "Reset your posture now",
        "Your back will thank you",
        "Stay aligned, stay healthy"
    ],

    "stress": [
        "Take a deep breath 🌿",
        "Pause and relax your mind",
        "Inhale calm, exhale stress",
        "You're doing fine",
        "Relax your shoulders and breathe",
        "Take a mindful moment",
        "Let go of tension",
        "Breathe slowly and deeply",
        "Calm your thoughts",
        "It's okay to slow down",
        "Give yourself a break",
        "Focus on your breath",
        "Release stress gently",
        "Stay present in this moment",
        "Relax your body",
        "Don't rush—stay calm",
        "You're in control",
        "Take a mental pause",
        "Let your mind reset",
        "Peace begins with breath",
        "Slow down your thoughts",
        "You've handled tougher things",
        "Take it one step at a time",
        "Calm mind, better decisions",
        "Breathe and reset 🌱"
    ],

    "motivation": [
        "Keep going 💪",
        "You're making progress",
        "Stay consistent",
        "Small steps matter",
        "Don't give up",
        "You've got this",
        "Push a little more",
        "Discipline beats motivation",
        "Progress over perfection",
        "Stay focused",
        "You're improving daily",
        "Keep building momentum",
        "Effort counts",
        "Show up for yourself",
        "Stay committed",
        "You are stronger than excuses",
        "Focus on your goals",
        "Every step counts",
        "Keep grinding",
        "Believe in your journey",
        "Stay determined",
        "You're closer than you think",
        "Consistency wins",
        "Make today count",
        "Your effort matters"
    ]
}

def get_random_message(reminder_type: str, custom_message: str):
    if reminder_type in MESSAGES:
        return random.choice(MESSAGES[reminder_type])

    if reminder_type == "custom":
        if custom_message and custom_message.strip() != "":
            return custom_message

        random_category = random.choice(list(MESSAGES.keys()))
        return random.choice(MESSAGES[random_category])

    return "Stay consistent 🚀"