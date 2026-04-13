import random


MESSAGES = {
    "water": [
        "💧 Hydration check: pause for one full glass of water. Your energy, focus, and mood all work better when you are well hydrated.",
        "💙 Take a water break right now. A few slow sips can wake up your body and help your mind feel clearer for the next task.",
        "🥤 Refill your bottle and drink some water. Small hydration habits through the day make a bigger difference than waiting until you feel thirsty.",
        "💧 Your body is asking for a reset. Stand up, stretch once, and drink a glass of water before you continue.",
        "🌊 Water first, then work. Give yourself a quick hydration moment so you can come back feeling fresher and more focused.",
        "💦 Friendly reminder: drink water now, not later. Your future self will thank you for taking care of the basics.",
        "🧊 Cool down and hydrate. Even a short sip break can help with concentration, headaches, and that tired afternoon feeling.",
        "🚰 Time to top up your water intake. One simple glass right now is a smart move for your body and your brain.",
        "💙 Before you push through the next task, take a calm sip of water and give yourself a tiny recovery moment.",
        "💧 Hydrate gently and keep moving. Progress feels easier when your body has what it needs.",
        "🥤 This is your cue to drink water and recharge a little. You do not need a big break to care for yourself well.",
        "🌿 Water is one of the easiest wins today. Take a few good sips and let your system catch up.",
        "💦 Quick wellness break: straighten up, breathe once, and drink some water before you dive back in.",
        "💙 Keep your momentum without draining yourself. A small water break now can help you stay steady for longer.",
        "🚰 Hydration time. Pick up your bottle, take a few slow sips, and come back feeling more awake.",
        "🌊 Stay cool, steady, and hydrated. Your focus deserves support, and water is a great place to start.",
        "💧 A gentle nudge to drink water: your body works hard for you all day, so give it this small bit of care.",
        "🥤 One more reminder to hydrate well today. Tiny healthy choices repeated often create real results.",
        "💙 Your brain loves hydration more than another push-through. Drink some water now and help yourself think better.",
        "🚰 Take thirty seconds for a water break. That tiny reset can make the next hour feel much lighter.",
        "💦 Sip first, then continue. Giving your body what it needs is not a delay, it is smart support.",
        "🌿 Let this reminder be your excuse to refill your bottle, stretch your arms, and take care of yourself for a minute.",
        "🥤 Small hydration habits add up quietly. Drink now and keep building the kind of routine that actually supports you.",
        "💧 If you have been meaning to drink water later, this is later. Take the sip now and feel a little more refreshed.",
    ],
    "posture": [
        "🪑 Posture reset time: sit tall, relax your shoulders, and let your neck line up naturally over your spine.",
        "🧍 Straighten up for a moment. Unclench your jaw, soften your shoulders, and give your back a better position.",
        "💼 Check your sitting posture. Bring your screen into view, plant your feet, and let your body settle into a stronger alignment.",
        "🧘 Your back deserves a reset. Roll your shoulders back, lift your chest slightly, and stop the slump before it turns into strain.",
        "📏 Small correction, big payoff: stack your head over your shoulders and your shoulders over your hips.",
        "🪑 Take ten seconds to fix your posture. Sit deeper in the chair, relax the shoulders, and support your lower back.",
        "🧍 Neck and spine check: pull your chin back gently, lengthen through the crown of your head, and breathe.",
        "💻 Tech-neck pause. Bring your attention back to your posture before another hour disappears in the same position.",
        "🧘 Reset your posture now so your body is not carrying extra stress for the rest of the day.",
        "📌 Sit like you are giving your spine some respect: tall through the torso, shoulders easy, feet grounded.",
        "🪑 A quick posture check can prevent a long ache later. Adjust now while it is still easy.",
        "🧍 Lift, lengthen, and breathe. A strong posture is not stiff, it is supported and relaxed.",
        "💼 Your shoulders do not need to live near your ears. Drop them down and let your upper back open up.",
        "🧘 Take a posture pause: open the chest, align the neck, and let your body return to a healthier shape.",
        "📏 Make one small correction right now. Your spine will thank you later today.",
        "💻 Before you keep typing, sit upright and bring your body back into balance.",
        "🪑 Better posture, better breathing, better focus. Reset your position and keep going with less strain.",
        "🧍 Strong and easy is the goal. Sit tall without tension and give your back a smoother day.",
        "📌 Your body has been holding the same shape for a while. Reset it now before discomfort settles in deeper.",
        "🪑 Pull yourself gently upright, relax your shoulders, and let your lower back feel a little more supported.",
        "💻 Good posture can start with one small move. Bring the screen up, sit taller, and stop leaning into strain.",
        "🧘 Open your chest, lengthen your neck, and let your spine return to a calmer, stronger alignment.",
        "📏 Think tall, not tense. Let your posture support you instead of asking your muscles to fight all day.",
        "🧍 A quick reset now can help you breathe easier, focus better, and feel much less worn out by the end of the day.",
    ],
    "motivation": [
        "💪 Keep moving. You do not need perfect conditions to make progress, you just need the next small step.",
        "🚀 Momentum is built one action at a time. Start with the easiest useful step and let that carry you forward.",
        "🔥 You have already come too far to stop at hesitation. Begin now, even if the start is small.",
        "🌟 Progress does not need to look dramatic to be real. Quiet consistency still changes everything over time.",
        "💥 Focus on the next win, not the whole mountain. One completed step today is still real progress.",
        "🏁 Show up for this moment. The version of you that keeps going is built through decisions like this one.",
        "📈 Small effort still counts. A little work done now is stronger than waiting for the perfect mood later.",
        "💪 Discipline can carry you when motivation feels quiet. Start anyway and let action create the energy.",
        "🚀 You are closer than you think. Keep the promise you made to yourself and take the next step now.",
        "🔥 Progress over overthinking. Move one piece forward and trust the momentum to build from there.",
        "🌟 You do not need to do everything today. Just do the next meaningful thing with full attention.",
        "💥 Keep your standard high and your next step simple. That combination wins more often than inspiration alone.",
        "🏁 The goal is not speed, it is follow-through. Stay in motion and let consistency do the heavy lifting.",
        "📈 Every solid routine starts as a decision repeated often. Make this one repetition count.",
        "💪 You are capable of more than this temporary resistance wants you to believe. Keep going.",
        "🚀 Start before you feel fully ready. Confidence usually arrives after the work begins, not before.",
        "🔥 Today still matters. Even a focused 10-minute effort can protect your momentum and your self-trust.",
        "🌟 Let this reminder pull you back to your goal. You do not need a fresh start, just a clean next move.",
        "🏁 Do not negotiate with the part of you that wants to drift. Choose the next action and let that choice lead.",
        "📈 You build confidence every time you follow through. This moment counts more than you think it does.",
        "💥 Even modest progress can change the day. Start with one useful action and let the rhythm return.",
        "💪 Your future results are hiding inside small repeated efforts. Make one of those efforts right now.",
        "🚀 Begin with what you can do in the next five minutes. Action creates clarity much faster than hesitation.",
        "🌟 Protect your momentum today. You do not need a heroic push, just an honest next step done well.",
    ],
}


def get_random_message(reminder_type: str, custom_message: str):
    if reminder_type in MESSAGES:
        return random.choice(MESSAGES[reminder_type])

    if reminder_type == "custom":
        if custom_message and custom_message.strip() != "":
            return custom_message

        random_category = random.choice(list(MESSAGES.keys()))
        return random.choice(MESSAGES[random_category])

    return "✨ Stay consistent and take one small step right now."
