from app.routes import *
from app.models import *
import bcrypt

#Account Setting
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()   
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str,account: str) -> bool:
    hashed = User.query.filter_by(username=account).with_entities(User.password).scalar()
    if hashed is not None:
        checked = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    else:
        checked = "false"
    return checked


        # Create a dictionary with the data to send
        ###data = {
        ###    'account': account,
        ###    'password': password
        ###}

        # Make an HTTP POST request to the API Gateway endpoint
        ###response = requests.post('https://' + aws_api_id + '.execute-api.us-east-1.amazonaws.com/prod/data', json=data)

        ###response_data = response.json()

        # Access the message from the response
        ###message = response_data['message']
        ###session['ms'] = message

        ###if response.status_code == 200:
            # Handle a successful response from the API Gateway
        ###    return redirect(url_for('login'))
        ###else:
            # Handle an error response from the API Gateway
            # You can display an error message to the user or perform other error handling logic
        ###    session.pop('ac', None)  # 從session中移除'ac'
        ###    session.pop('pw', None)  # 從session中移除'pw'
        ###    return redirect(url_for('index'))