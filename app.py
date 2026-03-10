from flask import Flask, render_template, request, jsonify
import ollama
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

app = Flask(__name__)
app.secret_key = 'coldmail-secret-key-change-in-production'

email_accounts_file = 'email_accounts.json'

def load_email_accounts():
    if os.path.exists(email_accounts_file):
        try:
            with open(email_accounts_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_email_accounts(accounts):
    with open(email_accounts_file, 'w') as f:
        json.dump(accounts, f)

email_accounts = load_email_accounts()

@app.route('/')
def index():
    return render_template('connect.html')

@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/generate')
def generate_page():
    return render_template('generate.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    model = data.get('model', 'llama3.2')
    tone = data.get('tone', 'Professional')
    recipient_name = data.get('recipient_name', '')
    recipient_role = data.get('recipient_role', '')
    company = data.get('company', '')
    your_name = data.get('your_name', '')
    your_role = data.get('your_role', '')
    context = data.get('context', '')

    prompt = f"""Write a cold email with the following details:
- Recipient: {recipient_name} ({recipient_role} at {company})
- Sender: {your_name} ({your_role})
- Tone: {tone}
- Additional Context: {context}

Write a compelling, personalized cold email that:
1. Has a catchy subject line
2. Opens with a personalized hook
3. Briefly introduces the sender
4. Provides value or addresses a pain point
5. Ends with a clear call to action
6. Stays concise (150-200 words max)

Subject line format: "Subject: ..."

Response format:
Subject: [subject line]

[Email body]"""

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response['message']['content']
        return jsonify({'success': True, 'email': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/models', methods=['GET'])
def get_models():
    try:
        models = ollama.list()
        model_names = []
        if hasattr(models, 'models'):
            for m in models.models:
                name = getattr(m, 'model', None) or getattr(m, 'name', None)
                if name:
                    model_names.append(name)
        return jsonify({'success': True, 'models': model_names})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'models': []})

@app.route('/connect-email', methods=['POST'])
def connect_email():
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')
    provider = data.get('provider', 'gmail')

    try:
        if provider == 'gmail':
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            imap_server = 'imap.gmail.com'
        else:
            smtp_server = 'smtp.outlook.com'
            smtp_port = 587
            imap_server = 'imap.outlook.com'

        smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
        smtp_conn.starttls()
        smtp_conn.login(email, password)
        smtp_conn.quit()

        imap_conn = imaplib.IMAP4_SSL(imap_server)
        imap_conn.login(email, password)
        imap_conn.logout()

        email_accounts[email] = {
            'provider': provider,
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'email': email,
            'password': password
        }
        
        save_email_accounts(email_accounts)

        return jsonify({'success': True, 'message': f'Connected to {email}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-connected-accounts', methods=['GET'])
def get_connected_accounts():
    accounts = [{'email': email, 'provider': acc['provider']} for email, acc in email_accounts.items()]
    return jsonify({'success': True, 'accounts': accounts})

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    from_email = data.get('from_email', '')
    to_email = data.get('to_email', '')
    subject = data.get('subject', '')
    body = data.get('body', '')

    if from_email not in email_accounts:
        return jsonify({'success': False, 'error': 'Email account not connected'})

    try:
        account = email_accounts[from_email]
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        smtp_conn = smtplib.SMTP(account['smtp_server'], account['smtp_port'])
        smtp_conn.starttls()
        smtp_conn.login(account['email'], account['password'])
        smtp_conn.sendmail(from_email, to_email, msg.as_string())
        smtp_conn.quit()

        return jsonify({'success': True, 'message': 'Email sent successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/disconnect-email', methods=['POST'])
def disconnect_email():
    data = request.json
    email = data.get('email', '')
    
    if email in email_accounts:
        del email_accounts[email]
        save_email_accounts(email_accounts)
        return jsonify({'success': True, 'message': f'Disconnected {email}'})
    return jsonify({'success': False, 'error': 'Account not found'})

if __name__ == '__main__':
    app.run(debug=False, port=5000, use_reloader=False)
