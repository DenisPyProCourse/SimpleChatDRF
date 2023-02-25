Hi!

Thank you for a really exciting task.
You can find the instruction how to run this Simple_Chat below:

Linux platform
1. Clone this repository: https://github.com/DenisPyProCourse/SimpleChatDRF.git
2. Install virtualenv: "pip install virtualenv" on the project directory
3. Create virtual environment: virtualenv venv
4. Activate: source venv/bin/activate
5. Run command: pip install -r requirements.txt
6. The following command: python manage.py createdb
7. Finally: python manage.py runserver

dump.json contains all necessary db data for testing. I use this dump in createdb command.

Use JWT Tokens for surfing the api. Header is Bearer. 
You can get JWT token: http://127.0.0.1:8000/api/v1/token/ (POST, you should input your login and pass)
You can verify JWT token: http://127.0.0.1:8000/api/v1/token/verify/
You can regresh JWT tokent: http://127.0.0.1:8000/api/v1/token/refresh/

You can registrate your own users (you don't need to be authenticated for registration), or use my with authentication details below:
Registration url: http://127.0.0.1:8000/api/v1/register/
1. Login: admin, password: 123
2. Login: Check, password: 123
3. Login: Den2, password: 12345ASDF
4. Login: Denchik, password: 123345
5. Login: Den, password: 12345ASDF

P.S. I didn't use .env here and left all environment variables in settings.
It was done in order not to complicate the setup process.
Sorry for that if it was important, usually I do it.
