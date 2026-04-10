import smtplib
import socket
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def build_template(title, body):
    return f"""
    <html>
      <body style="margin:0;padding:0;background:#f4f6f8;font-family:Arial,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td align="center">

              <table width="420" style="
                background:white;
                margin-top:40px;
                border-radius:12px;
                padding:20px;
                box-shadow:0 4px 12px rgba(0,0,0,0.05);
              ">

                <tr>
                  <td align="center" style="
                    font-size:22px;
                    font-weight:bold;
                    color:#4a90e2;
                  ">
                    ZenCue ⏰
                  </td>
                </tr>

                <tr>
                  <td align="center" style="
                    padding:10px 0;
                    font-size:16px;
                    font-weight:500;
                    color:#333;
                  ">
                    {title}
                  </td>
                </tr>

                <tr>
                  <td align="center" style="
                    padding:20px 10px;
                    font-size:15px;
                    color:#555;
                    line-height:1.6;
                  ">
                    {body}
                  </td>
                </tr>

                <tr>
                  <td align="center">
                    <a href="#" style="
                      display:inline-block;
                      padding:10px 18px;
                      background:#4a90e2;
                      color:white;
                      text-decoration:none;
                      border-radius:6px;
                      font-size:14px;
                    ">
                      Open ZenCue
                    </a>
                  </td>
                </tr>

                <tr>
                  <td align="center" style="
                    padding-top:20px;
                    font-size:12px;
                    color:#999;
                  ">
                    Stay consistent. Stay healthy.
                  </td>
                </tr>

              </table>

            </td>
          </tr>
        </table>
      </body>
    </html>
    """


# ---------------- CORE SEND FUNCTION ---------------- #
def send_html_email(to_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    socket.setdefaulttimeout(10)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.connect("smtp.gmail.com", 465)
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent")

    except Exception as e:
        print("❌ Email error:", e)


# ---------------- OTP EMAIL ---------------- #
def send_otp_email(to_email, otp):
    html = build_template(
        "Verify Your Account",
        f"""
        Use the OTP below to verify your account:

        <h2 style="letter-spacing:3px;">{otp}</h2>

        <p>This OTP will expire in 5 minutes.</p>
        """
    )

    send_html_email(to_email, "ZenCue OTP Verification", html)


# ---------------- REMINDER EMAIL ---------------- #
def send_reminder_email(to_email, message):
    html = build_template(
        "Reminder ⏰",
        f"""
        {message}
        <br><br>
        Take a small step now 👇
        """
    )

    send_html_email(to_email, "ZenCue Reminder", html)