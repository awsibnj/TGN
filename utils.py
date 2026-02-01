import qrcode
from io import BytesIO
from datetime import datetime
import validators
import phonenumbers

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    bio = BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

def format_currency(amount):
    return f"₹{float(amount):,.2f}"

def validate_email(email):
    return validators.email(email)

def validate_mobile(mobile, region='IN'):
    try:
        parsed = phonenumbers.parse(mobile, region)
        return phonenumbers.is_valid_number(parsed)
    except:
        return False

def format_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d %b %Y, %I:%M %p')
    except:
        return date_str

def truncate_text(text, max_length=100):
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'

def create_keyboard_row(buttons, row_size=2):
    rows = []
    for i in range(0, len(buttons), row_size):
        rows.append(buttons[i:i+row_size])
    return rows
