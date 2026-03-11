"""
Email Module - Send reports and data via email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from typing import List, Optional, Dict, Any
import io
import os


class EmailService:
    """Service for sending emails with reports and attachments"""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587,
                 username: str = None, password: str = None):
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port
        self.username = username or os.getenv('EMAIL_USERNAME', '')
        self.password = password or os.getenv('EMAIL_PASSWORD', '')
        self.is_configured = bool(self.username and self.password)
    
    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body_html: str,
        body_text: str = None,
        attachments: List[Dict[str, Any]] = None,
        cc_emails: List[str] = None,
        bcc_emails: List[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email with optional attachments
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            body_html: HTML content of email
            body_text: Plain text content (optional, will be auto-generated from HTML)
            attachments: List of dicts with 'filename', 'content', and 'content_type'
            cc_emails: List of CC email addresses
            bcc_emails: List of BCC email addresses
        
        Returns:
            Dict with status and message
        """
        if not self.is_configured:
            return {
                "success": False,
                "message": "Email service not configured. Please set SMTP credentials."
            }
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = ', '.join(to_emails)
            
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
            
            # Add body
            if body_text:
                msg.attach(MIMEText(body_text, 'plain'))
            
            msg.attach(MIMEText(body_html, 'html'))
            
            # Add attachments
            if attachments:
                for attachment in attachments:
                    self._add_attachment(msg, attachment)
            
            # Send email
            all_recipients = to_emails + (cc_emails or []) + (bcc_emails or [])
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, all_recipients, msg.as_string())
            
            return {
                "success": True,
                "message": f"Email sent successfully to {len(to_emails)} recipient(s)"
            }
        
        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "message": "Authentication failed. Please check email credentials."
            }
        except smtplib.SMTPException as e:
            return {
                "success": False,
                "message": f"SMTP error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }
    
    def _add_attachment(self, msg: MIMEMultipart, attachment: Dict[str, Any]):
        """Add an attachment to the email"""
        filename = attachment.get('filename', 'attachment')
        content = attachment.get('content', b'')
        content_type = attachment.get('content_type', 'application/octet-stream')
        
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        part = MIMEApplication(content, Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)
    
    def send_report_email(
        self,
        to_emails: List[str],
        report_html: str,
        report_title: str = "TechXcel Report",
        additional_attachments: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a report email with the report as both body and attachment"""
        
        subject = f"📊 {report_title} - {self._get_current_date()}"
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #8b5cf6; margin: 0;">⚡ TechXcel</h1>
                    <p style="color: #666;">Your data report is ready!</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #8b5cf6, #06b6d4); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h2 style="margin: 0 0 10px 0;">{report_title}</h2>
                    <p style="margin: 0; opacity: 0.9;">Generated on {self._get_current_date()}</p>
                </div>
                
                <p style="color: #333; line-height: 1.6;">
                    Your comprehensive data analysis report is attached to this email. 
                    Open the HTML file in your browser for an interactive experience.
                </p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #333; margin: 0 0 10px 0;">📎 Attachments included:</h3>
                    <ul style="color: #666; margin: 0; padding-left: 20px;">
                        <li>Interactive HTML Report</li>
                        {self._get_attachment_list_items(additional_attachments)}
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <p style="color: #999; font-size: 12px;">
                        Powered by TechXcel - Smart Excel Analytics with AI
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Prepare attachments
        attachments = [
            {
                'filename': f'report_{self._get_file_date()}.html',
                'content': report_html,
                'content_type': 'text/html'
            }
        ]
        
        if additional_attachments:
            attachments.extend(additional_attachments)
        
        return self.send_email(
            to_emails=to_emails,
            subject=subject,
            body_html=body_html,
            attachments=attachments
        )
    
    def send_data_email(
        self,
        to_emails: List[str],
        csv_content: str,
        filename: str = "data.csv",
        message: str = None
    ) -> Dict[str, Any]:
        """Send data as CSV attachment"""
        
        subject = f"📊 Data Export - {filename}"
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
                <h1 style="color: #8b5cf6;">⚡ TechXcel Data Export</h1>
                <p style="color: #666;">{message or 'Your data export is attached.'}</p>
                <p style="color: #333;">📎 Attached: <strong>{filename}</strong></p>
            </div>
        </body>
        </html>
        """
        
        attachments = [
            {
                'filename': filename,
                'content': csv_content,
                'content_type': 'text/csv'
            }
        ]
        
        return self.send_email(
            to_emails=to_emails,
            subject=subject,
            body_html=body_html,
            attachments=attachments
        )
    
    def send_alert_email(
        self,
        to_emails: List[str],
        alert_type: str,
        alert_message: str,
        data_summary: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Send an alert email"""
        
        alert_colors = {
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#3b82f6',
            'success': '#22c55e'
        }
        
        color = alert_colors.get(alert_type, '#8b5cf6')
        
        subject = f"🔔 TechXcel Alert: {alert_type.upper()}"
        
        summary_html = ""
        if data_summary:
            summary_html = f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h3 style="margin: 0 0 10px 0;">Data Summary:</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    {"".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in data_summary.items()])}
                </ul>
            </div>
            """
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
                <div style="background: {color}; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h1 style="margin: 0;">🔔 Alert: {alert_type.upper()}</h1>
                </div>
                <p style="color: #333; font-size: 16px; line-height: 1.6;">{alert_message}</p>
                {summary_html}
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; text-align: center;">
                    <p style="color: #999; font-size: 12px;">Sent by TechXcel Analytics</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_emails=to_emails,
            subject=subject,
            body_html=body_html
        )
    
    def _get_current_date(self) -> str:
        """Get current date formatted"""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")
    
    def _get_file_date(self) -> str:
        """Get current date for filenames"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _get_attachment_list_items(self, attachments: List[Dict[str, Any]]) -> str:
        """Generate list items for attachments"""
        if not attachments:
            return ""
        return "".join([f"<li>{att.get('filename', 'Attachment')}</li>" for att in attachments])
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def get_configuration_status(self) -> Dict[str, Any]:
        """Get email configuration status"""
        return {
            "configured": self.is_configured,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
            "username_set": bool(self.username),
            "password_set": bool(self.password)
        }


class ScheduledEmailService:
    """Service for scheduling automated emails"""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.scheduled_jobs = []
    
    def schedule_daily_report(
        self,
        to_emails: List[str],
        report_generator_func,
        hour: int = 9,
        minute: int = 0
    ) -> Dict[str, Any]:
        """Schedule a daily report email"""
        # This would integrate with APScheduler or similar
        # For now, return configuration info
        return {
            "job_type": "daily_report",
            "recipients": to_emails,
            "scheduled_time": f"{hour:02d}:{minute:02d}",
            "status": "configured"
        }
    
    def schedule_weekly_summary(
        self,
        to_emails: List[str],
        report_generator_func,
        day_of_week: str = "monday",
        hour: int = 9
    ) -> Dict[str, Any]:
        """Schedule a weekly summary email"""
        return {
            "job_type": "weekly_summary",
            "recipients": to_emails,
            "day": day_of_week,
            "hour": hour,
            "status": "configured"
        }
    
    def schedule_threshold_alert(
        self,
        to_emails: List[str],
        column: str,
        threshold: float,
        condition: str = "greater_than"
    ) -> Dict[str, Any]:
        """Schedule an alert when threshold is crossed"""
        return {
            "job_type": "threshold_alert",
            "recipients": to_emails,
            "monitored_column": column,
            "threshold": threshold,
            "condition": condition,
            "status": "configured"
        }
