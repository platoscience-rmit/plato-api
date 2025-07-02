import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def test_smtp_connection():
    username = "500e555c92fb04"
    password = "a5e87b456ae609"
    
    configs = [
        ('sandbox.smtp.mailtrap.io', 2525, True),
        ('sandbox.smtp.mailtrap.io', 587, True),
        ('sandbox.smtp.mailtrap.io', 465, False),
        ('live.smtp.mailtrap.io', 587, True),
    ]
    
    for host, port, use_tls in configs:
        try:
            print(f"\n🔄 Testing {host}:{port} (TLS: {use_tls})")
            
            if use_tls:
                server = smtplib.SMTP(host, port, timeout=15)
                print("📡 Connected, starting TLS...")
                server.starttls()
                print("🔒 TLS started")
            else:
                print("📡 Connecting with SSL...")
                server = smtplib.SMTP_SSL(host, port, timeout=15)
            
            print("🔑 Logging in...")
            server.login(username, password)
            print(f"✅ SUCCESS: {host}:{port} works!")
            
            # Send test email
            server.sendmail(
                "noreply@plato-api.com",
                ["test@example.com"],
                "Subject: Test\n\nThis is a test email."
            )
            print("📧 Test email sent!")
            
            server.quit()
            return host, port, use_tls
            
        except Exception as e:
            print(f"❌ FAILED {host}:{port}: {str(e)}")
    
    return None

if __name__ == "__main__":
    print("Testing Mailtrap SMTP connection...")
    result = test_smtp_connection()
    
    if result:
        host, port, use_tls = result
        print(f"\n🎉 Working configuration found: {host}:{port} (TLS: {use_tls})")
    else:
        print("\No working configuration found. Possible issues:")
        print("Corporate firewall blocking SMTP ports")
        print("ISP blocking SMTP connections")
        print("Windows Firewall blocking outbound connections")
        print("Antivirus software interference")