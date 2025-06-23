import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict


class Emails:
    def __init__(self, overdue_list):
        self.overdue_list = overdue_list
        self.sender_email = 'technology@university.edu'
        self.password = os.getenv('EMAIL_PASSWORD')  # Get from environment variable
        self.smtp_server = "smtp.office365.com"
        self.smtp_port = 587
    
    def group_overdue_by_borrower(self, overdue_list):
        """Group multiple overdue items per person"""
        grouped = defaultdict(list)
        
        for item in overdue_list:
            borrower = item['borrower']
            grouped[borrower].append(item)
        
        return dict(grouped)
    
    def create_email_content(self, borrower, overdue_items):
        """Generate subject and body for each person"""
        subject = f"Equipment Return Reminder - {len(overdue_items)} Item(s) Overdue"
        
        body = f"""Dear {borrower},

This is a friendly reminder that you have {len(overdue_items)} overdue equipment item(s):

"""
        
        for item in overdue_items:
            body += f"• {item['item']} - Due: {item['due_date']} ({item['days_overdue']} days overdue)\n"
        
        body += """
Please return these items as soon as possible to avoid any late fees.

If you have any questions, please contact us at technology@university.edu.

Best regards,
Technology Department
"""
        
        return subject, body
        
    def send_single_email(self, to_email, subject, body):
        """Send one email via SMTP"""
        if not self.password:
            print("Error: EMAIL_PASSWORD environment variable not set")
            return False
            
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject
            
            # Add body to email
            message.attach(MIMEText(body, "plain"))
            
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable security
                server.login(self.sender_email, self.password)
                
                # Send email
                text = message.as_string()
                server.sendmail(self.sender_email, to_email, text)
                
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            return False
        
    def send_all_reminders(self, overdue_list=None):
        """Orchestrate the whole process"""
        if overdue_list is None:
            overdue_list = self.overdue_list
            
        if not overdue_list:
            print("No overdue items to send reminders for.")
            return
        
        # Group items by borrower
        grouped_items = self.group_overdue_by_borrower(overdue_list)
        
        print(f"Sending reminders to {len(grouped_items)} borrower(s)...")
        
        success_count = 0
        for borrower, items in grouped_items.items():
            # For demo purposes, using a fake email format
            # In real usage, you'd have actual email addresses in your data
            borrower_email = f"{borrower.lower().replace(' ', '.')}@university.edu"
            
            subject, body = self.create_email_content(borrower, items)
            
            print(f"\nWould send to {borrower} ({borrower_email}):")
            print(f"Subject: {subject}")
            print("=" * 50)
            
            # Uncomment this line when you're ready to actually send emails:
            # if self.send_single_email(borrower_email, subject, body):
            #     success_count += 1
            
            # For now, just print what would be sent
            print("EMAIL PREVIEW:")
            print(body)
            print("=" * 50)
        
        print(f"\nEmail process complete. Would have sent {len(grouped_items)} emails.")
        # print(f"Successfully sent {success_count} emails.")