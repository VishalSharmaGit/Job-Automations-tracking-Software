import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"      # use Gmail App Password, not your real password
TO_EMAIL   = "recipient@gmail.com"

def build_html_table(df):
    rows = ""
    for _, row in df.iterrows():
        rows += f"""
        <tr>
          <td>{row['title']}</td>
          <td>{row['company']}</td>
          <td>{row['location']}</td>
          <td><a href="{row['link']}">Apply</a></td>
        </tr>"""
    return f"""
    <html><body>
    <h2>New Data Analyst Jobs Today</h2>
    <table border="1" cellpadding="6" style="border-collapse:collapse">
      <tr><th>Title</th><th>Company</th><th>Location</th><th>Link</th></tr>
      {rows}
    </table>
    </body></html>"""

def send_email_alert(df):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔔 {len(df)} New Data Analyst Jobs Found"
    msg["From"]    = FROM_EMAIL
    msg["To"]      = TO_EMAIL
    msg.attach(MIMEText(build_html_table(df), "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    print("Email alert sent.")