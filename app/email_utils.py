import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import List, Dict
import logging
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "procurement@company.com")
        self.from_name = os.getenv("FROM_NAME", "Procurement Compliance AI")
    
    def get_email_templates(self, language: str) -> Dict[str, str]:
        """Get email templates in different languages"""
        logo_url = "https://your-domain.com/static/img/simad_logo.png"  # Update with your actual domain or use relative path if served
        templates = {
            "en": {
                "subject": "Request for Quotation (RFQ) - Simad University",
                "body": f"""
<html>
  <body style='font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px;'>
    <div style='max-width: 600px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #eee; padding: 24px;'>
      <div style='text-align: center; margin-bottom: 24px;'>
        <img src='{logo_url}' alt='Simad University Logo' style='max-width: 120px; margin-bottom: 12px;'>
        <h2 style='color: #1a4d8f;'>Simad University Procurement</h2>
      </div>
      <p>Dear {{vendor_name}},</p>
      <p>We are pleased to invite you to submit a quotation for the following procurement requirements:</p>
      <ul>
        <li><strong>Legal Entity ID:</strong> {{legal_entity_id}}</li>
        <li><strong>Item Type:</strong> {{item_type}}</li>
        <li><strong>Description:</strong> {{description}}</li>
        <li><strong>Quantity:</strong> {{quantity}}</li>
      </ul>
      <p><strong>Important Information:</strong></p>
      <ul>
        <li>Please review the attached RFQ document for detailed specifications.</li>
        <li>Submit your quotation within {{deadline}} days.</li>
        <li>Ensure compliance with all procurement regulations.</li>
        <li>Contact us if you have any questions.</li>
      </ul>
      <p><strong>Submission Requirements:</strong></p>
      <ul>
        <li>Technical specifications</li>
        <li>Pricing details</li>
        <li>Delivery timeline</li>
        <li>Quality certifications</li>
        <li>Compliance documentation</li>
      </ul>
      <p>Best regards,<br>Simad University Procurement Team</p>
    </div>
  </body>
</html>
"""
            },
            "ar": {
                "subject": "طلب عرض سعر (RFQ) - جامعة سيماد",
                "body": f"""
<html>
  <body style='font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px;'>
    <div style='max-width: 600px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #eee; padding: 24px;'>
      <div style='text-align: center; margin-bottom: 24px;'>
        <img src='{logo_url}' alt='Simad University Logo' style='max-width: 120px; margin-bottom: 12px;'>
        <h2 style='color: #1a4d8f;'>جامعة سيماد - قسم المشتريات</h2>
      </div>
      <p>عزيزي/عزيزتي {{vendor_name}}،</p>
      <p>يسرنا دعوتكم لتقديم عرض سعر للمتطلبات التالية:</p>
      <ul>
        <li><strong>رقم الكيان القانوني:</strong> {{legal_entity_id}}</li>
        <li><strong>نوع العنصر:</strong> {{item_type}}</li>
        <li><strong>الوصف:</strong> {{description}}</li>
        <li><strong>الكمية:</strong> {{quantity}}</li>
      </ul>
      <p><strong>معلومات مهمة:</strong></p>
      <ul>
        <li>يرجى مراجعة وثيقة طلب العرض المرفقة للمواصفات التفصيلية.</li>
        <li>قدم عرضك خلال {{deadline}} يوم.</li>
        <li>تأكد من الامتثال لجميع لوائح المشتريات.</li>
        <li>اتصل بنا إذا كان لديك أي أسئلة.</li>
      </ul>
      <p><strong>متطلبات التقديم:</strong></p>
      <ul>
        <li>المواصفات التقنية</li>
        <li>تفاصيل الأسعار</li>
        <li>الجدول الزمني للتسليم</li>
        <li>شهادات الجودة</li>
        <li>وثائق الامتثال</li>
      </ul>
      <p>مع أطيب التحيات،<br>فريق المشتريات - جامعة سيماد</p>
    </div>
  </body>
</html>
"""
            },
            "fr": {
                "subject": "Demande de Devis (RFQ) - Université Simad",
                "body": f"""
<html>
  <body style='font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px;'>
    <div style='max-width: 600px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #eee; padding: 24px;'>
      <div style='text-align: center; margin-bottom: 24px;'>
        <img src='{logo_url}' alt='Logo Université Simad' style='max-width: 120px; margin-bottom: 12px;'>
        <h2 style='color: #1a4d8f;'>Université Simad - Achats</h2>
      </div>
      <p>Cher/Chère {{vendor_name}},</p>
      <p>Nous avons le plaisir de vous inviter à soumettre un devis pour les exigences d'approvisionnement suivantes :</p>
      <ul>
        <li><strong>ID de l'entité légale :</strong> {{legal_entity_id}}</li>
        <li><strong>Type d'article :</strong> {{item_type}}</li>
        <li><strong>Description :</strong> {{description}}</li>
        <li><strong>Quantité :</strong> {{quantity}}</li>
      </ul>
      <p><strong>Informations importantes :</strong></p>
      <ul>
        <li>Veuillez examiner le document RFQ joint pour les spécifications détaillées.</li>
        <li>Soumettez votre devis dans les {{deadline}} jours.</li>
        <li>Assurez-vous de respecter toutes les réglementations d'approvisionnement.</li>
        <li>Contactez-nous si vous avez des questions.</li>
      </ul>
      <p><strong>Exigences de soumission :</strong></p>
      <ul>
        <li>Spécifications techniques</li>
        <li>Détails de prix</li>
        <li>Calendrier de livraison</li>
        <li>Certifications de qualité</li>
        <li>Documentation de conformité</li>
      </ul>
      <p>Cordialement,<br>L'équipe des achats - Université Simad</p>
    </div>
  </body>
</html>
"""
            }
        }
        return templates.get(language, templates["en"])
    
    def send_rfq_notification(self, vendor_email: str, vendor_name: str, vendor_language: str, 
                             legal_entity_id: int, item_type: str, description: str, 
                             quantity: int, pdf_path: str = None, deadline: int = 14) -> bool:
        """Send RFQ notification to vendor in their preferred language"""
        try:
            # Get email template for vendor's language
            template = self.get_email_templates(vendor_language)
            
            # Prepare email content
            subject = template["subject"]
            body = template["body"].format(
                vendor_name=vendor_name,
                legal_entity_id=legal_entity_id,
                item_type=item_type,
                description=description,
                quantity=quantity,
                deadline=deadline
            )
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = vendor_email
            msg['Subject'] = subject
            
            # Add HTML body
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # Add PDF attachment if provided
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= RFQ_{legal_entity_id}.pdf'
                )
                msg.attach(part)
            
            # Send email
            if self.smtp_username and self.smtp_password:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                server.quit()
                logger.info(f"RFQ notification sent to {vendor_email} in {vendor_language}")
                return True
            else:
                # Log email content for development (no actual sending)
                logger.info(f"Email would be sent to {vendor_email}:")
                logger.info(f"Subject: {subject}")
                logger.info(f"Body: {body}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send email to {vendor_email}: {str(e)}")
            return False
    
    def send_bulk_rfq_notifications(self, vendor_data: List[Dict], pr_data: Dict, pdf_path: str = None) -> Dict[str, bool]:
        """Send RFQ notifications to multiple vendors"""
        results = {}
        
        for vendor in vendor_data:
            success = self.send_rfq_notification(
                vendor_email=vendor['email'],
                vendor_name=vendor['name'],
                vendor_language=vendor['language'],
                legal_entity_id=pr_data['legal_entity_id'],
                item_type=pr_data['item_type'],
                description=pr_data['description'],
                quantity=pr_data['quantity'],
                pdf_path=pdf_path
            )
            results[vendor['email']] = success
        
        return results

# Global email notifier instance
email_notifier = EmailNotifier() 