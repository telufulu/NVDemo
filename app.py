from flask import Flask, request, send_file
import requests
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/number_verification')
def number_verification():
    # Datos necesarios para conseguir el resultado
    code = request.args.get('code', '')
    phone_number = request.args.get('state', '').replace(" ", "+")

    client_id = "your_client_id"
    client_secret = "your_client_secret"
    app_credentials = f"{client_id}:{client_secret}"
    credentials = base64.b64encode(app_credentials.encode('utf-8')).decode('utf-8')
    
    # headers y body para conseguir el token
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {credentials}"
    }
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://crispy-dollop-4rj67w465xr3j9gr-5000.app.github.dev/number_verification"
    }
    response = requests.post("https://sandbox.opengateway.telefonica.com/apigateway/token",
                             headers=headers,
                             data=body
                             )
    access_token = response.json().get("access_token")

    # headers y body para obtener el resultado final
    headers = {
       # "accept": "application/json"
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    body = {
        "phoneNumber": phone_number
    }
    response = requests.post("https://sandbox.opengateway.telefonica.com/apigateway/number-verification/v0/verify",
                             headers=headers,
                             json=body
                             )
    result = response.json().get("devicePhoneNumberVerified")
    return f"Phone number {'verified' if result else 'does not match mobile line'}"
    
app.run()