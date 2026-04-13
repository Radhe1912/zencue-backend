import html
import json
import os
import smtplib
import socket
import urllib.error
import urllib.request
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv


BACKEND_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(BACKEND_ENV_PATH)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
APP_URL = os.getenv("APP_URL", "https://zencue.vercel.app")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", EMAIL_USER or "onboarding@resend.dev")

REMINDER_THEMES = {
    "water": {
        "eyebrow": "Hydration reset",
        "title": "Time to drink some water 💧",
        "intro": "A quick water break can bring back energy, focus, and a little calm.",
        "accent": "#2b7fff",
        "header_gradient": "linear-gradient(135deg, #eef7ff 0%, #cfe6ff 100%)",
        "panel_bg": "linear-gradient(135deg, rgba(43,127,255,0.10), rgba(127,195,255,0.18))",
        "panel_border": "rgba(43,127,255,0.20)",
        "footer": "Hydration is one of the simplest ways to support your day well.",
        "steps": [
            "Fill your bottle or grab a glass.",
            "Take a few slow, steady sips.",
            "Come back feeling clearer and more refreshed.",
        ],
    },
    "posture": {
        "eyebrow": "Posture reset",
        "title": "Realign and reset your posture 🪑",
        "intro": "A small posture correction now can save your neck, shoulders, and back from extra strain later.",
        "accent": "#8a5a2b",
        "header_gradient": "linear-gradient(135deg, #fff6eb 0%, #ead3b3 100%)",
        "panel_bg": "linear-gradient(135deg, rgba(138,90,43,0.10), rgba(214,164,113,0.18))",
        "panel_border": "rgba(138,90,43,0.20)",
        "footer": "Good posture is not rigid. It is steady, supported, and easier on your body.",
        "steps": [
            "Relax your shoulders away from your ears.",
            "Bring your head gently back over your spine.",
            "Sit tall and breathe once before continuing.",
        ],
    },
    "motivation": {
        "eyebrow": "Momentum boost",
        "title": "Take the next step forward 🚀",
        "intro": "You do not need a perfect wave of motivation. You just need the next meaningful move.",
        "accent": "#d45c1f",
        "header_gradient": "linear-gradient(135deg, #fff4ea 0%, #f3d0b6 100%)",
        "panel_bg": "linear-gradient(135deg, rgba(212,92,31,0.10), rgba(241,164,102,0.18))",
        "panel_border": "rgba(212,92,31,0.20)",
        "footer": "Consistency grows when you keep choosing the next small action.",
        "steps": [
            "Pick the next useful task, not the whole mountain.",
            "Work on it for just a few focused minutes.",
            "Let action rebuild your momentum.",
        ],
    },
    "custom": {
        "eyebrow": "Your reminder",
        "title": "A note from your routine ✨",
        "intro": "You set this reminder for a reason. Here is your cue to follow through.",
        "accent": "#7b5cff",
        "header_gradient": "linear-gradient(135deg, #f6f0ff 0%, #ddd1ff 100%)",
        "panel_bg": "linear-gradient(135deg, rgba(123,92,255,0.10), rgba(181,157,255,0.18))",
        "panel_border": "rgba(123,92,255,0.20)",
        "footer": "A small reminder at the right time can change the whole day.",
        "steps": [
            "Pause and read your reminder once more.",
            "Do the thing now while the cue is fresh.",
            "Enjoy the win of following through.",
        ],
    },
}
def build_template(
    *,
    eyebrow,
    title,
    intro,
    body_html,
    footer_note,
    accent="#d66b2d",
    header_gradient="linear-gradient(135deg, #fff7ea 0%, #f4dfba 100%)",
):
    safe_eyebrow = html.escape(eyebrow)
    safe_title = html.escape(title)
    safe_intro = html.escape(intro)
    safe_footer = html.escape(footer_note)
    safe_app_url = html.escape(APP_URL, quote=True)

    return f"""
    <html>
      <body style="margin:0;padding:0;background-color:#f6efe2;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:
          radial-gradient(circle at top left, rgba(214,107,45,0.18), transparent 28%),
          linear-gradient(135deg, #f7f1e5 0%, #efe0c2 100%);
          background-color:#f6efe2;
          margin:0;
          padding:32px 16px;
        ">
          <tr>
            <td align="center">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:620px;">
                <tr>
                  <td style="padding-bottom:18px;text-align:center;font-family:Georgia,'Times New Roman',serif;color:{accent};font-size:14px;letter-spacing:1.8px;text-transform:uppercase;">
                    {safe_eyebrow}
                  </td>
                </tr>
                <tr>
                  <td style="
                    background:rgba(255,250,242,0.96);
                    border:1px solid rgba(63,52,38,0.12);
                    border-radius:28px;
                    padding:0;
                    overflow:hidden;
                    box-shadow:0 24px 60px rgba(96,69,27,0.16);
                  ">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td style="padding:30px 32px 20px;background:{header_gradient};">
                          <div style="font-family:Georgia,'Times New Roman',serif;font-size:31px;line-height:1;color:#2c2419;font-weight:bold;">
                            ZenCue
                          </div>
                          <div style="margin-top:10px;font-family:Arial,sans-serif;font-size:13px;color:#6f6559;line-height:1.7;">
                            Calm reminders, thoughtful routines, and better follow-through.
                          </div>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:32px 32px 12px;font-family:Georgia,'Times New Roman',serif;font-size:34px;line-height:1.08;color:#2c2419;font-weight:bold;">
                          {safe_title}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:0 32px 8px;font-family:Arial,sans-serif;font-size:16px;line-height:1.7;color:#6f6559;">
                          {safe_intro}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:12px 32px 18px;font-family:Arial,sans-serif;font-size:16px;line-height:1.7;color:#2c2419;">
                          {body_html}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:0 32px 28px;">
                          <a href="{safe_app_url}" style="
                            display:inline-block;
                            background:linear-gradient(135deg, {accent} 0%, #ea8c3f 100%);
                            color:#fffaf5;
                            text-decoration:none;
                            padding:14px 22px;
                            border-radius:16px;
                            font-family:Arial,sans-serif;
                            font-size:14px;
                            font-weight:700;
                          ">
                            Open ZenCue
                          </a>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:18px 32px 30px;border-top:1px solid rgba(63,52,38,0.08);font-family:Arial,sans-serif;font-size:13px;line-height:1.7;color:#8b7f70;">
                          {safe_footer}<br>
                          If you did not expect this email, you can safely ignore it.
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """


def send_via_resend(to_email, subject, html_content, text_content):
    if not RESEND_API_KEY:
        return False

    payload = {
        "from": RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content,
        "text": text_content,
    }

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "ZenCue/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            response.read()
        print("Email sent via Resend")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print("Email API error:", e.code, body)
    except Exception as e:
        print("Email API error:", e)

    return False


def send_via_smtp(to_email, subject, html_content, text_content):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("Email SMTP skipped: missing EMAIL_USER or EMAIL_PASSWORD")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    socket.setdefaulttimeout(10)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.connect("smtp.gmail.com", 465)
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent via SMTP")
        return True
    except Exception as e:
        print("Email SMTP error:", e)
        return False


def send_html_email(to_email, subject, html_content, text_content):
    if send_via_resend(to_email, subject, html_content, text_content):
        return True

    return send_via_smtp(to_email, subject, html_content, text_content)


def send_otp_email(to_email, otp):
    safe_otp = html.escape(str(otp))
    html_content = build_template(
        eyebrow="Account setup",
        title="Verify your account",
        intro="Use this one-time code to finish creating your ZenCue account.",
        body_html=f"""
        <div style="
          margin:10px 0 18px;
          padding:22px 18px;
          border-radius:22px;
          background:linear-gradient(135deg, rgba(214,107,45,0.12), rgba(234,140,63,0.18));
          border:1px solid rgba(214,107,45,0.18);
          text-align:center;
        ">
          <div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#a94914;margin-bottom:8px;">
            Verification code
          </div>
          <div style="font-family:Arial,sans-serif;font-size:34px;letter-spacing:8px;font-weight:700;color:#2c2419;">
            {safe_otp}
          </div>
        </div>
        <p style="margin:0 0 10px;">This code expires in 5 minutes.</p>
        <p style="margin:0;">You only need OTP during first-time account setup. After that, you can sign in with your password.</p>
        """,
        footer_note="Stay consistent, stay cared for.",
    )

    text_content = (
        "ZenCue account verification\n\n"
        f"Your verification code is: {otp}\n\n"
        "This code expires in 5 minutes.\n"
        "You only need OTP during first-time account setup."
    )

    return send_html_email(to_email, "ZenCue OTP Verification", html_content, text_content)


def send_reminder_email(to_email, message, reminder_type="custom"):
    theme = REMINDER_THEMES.get(reminder_type, REMINDER_THEMES["custom"])
    safe_message = html.escape(message)

    steps_html = "".join(
        f"""
        <tr>
          <td style="padding:0 0 10px;font-size:15px;line-height:1.7;color:#2c2419;">
            {index}. {html.escape(step)}
          </td>
        </tr>
        """
        for index, step in enumerate(theme["steps"], start=1)
    )

    html_content = build_template(
        eyebrow=theme["eyebrow"],
        title=theme["title"],
        intro=theme["intro"],
        accent=theme["accent"],
        header_gradient=theme["header_gradient"],
        body_html=f"""
        <div style="
          margin:10px 0 18px;
          padding:24px 22px;
          border-radius:22px;
          background:{theme["panel_bg"]};
          border:1px solid {theme["panel_border"]};
        ">
          <div style="font-family:Georgia,'Times New Roman',serif;font-size:26px;line-height:1.4;color:#2c2419;">
            {safe_message}
          </div>
        </div>
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:6px;">
          <tr>
            <td style="padding:0 0 10px;font-size:15px;color:#6f6559;">
              Try this next:
            </td>
          </tr>
          {steps_html}
        </table>
        """,
        footer_note=theme["footer"],
    )

    text_steps = "\n".join(
        f"{index}. {step}" for index, step in enumerate(theme["steps"], start=1)
    )
    text_content = (
        f"ZenCue reminder - {theme['title']}\n\n"
        f"{message}\n\n"
        "Try this next:\n"
        f"{text_steps}"
    )

    return send_html_email(to_email, "ZenCue Reminder", html_content, text_content)
