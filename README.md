Hi!

Thank you for a really exciting task.
You can find the instruction how to run this Simple_Chat below:

1. Clone this repository 
2. Run command: pip install -r requirements.txt
3. The following command: python manage.py createdb
4. Finally: python manage.py runserver

dump.json contains all necessary db data for testing. I use this dump in createdb command.

Use JWT Tokens for surfing the api. Header is Bearer.

You can registrate your own users (you don't need to be authenticated for registration), or use my with authentication details below:
1. Login: admin, password: 123
2. Login: Check, password: 123
3. Login: Den2, password: 12345ASDF
4. Login: Denchik, password: 123345
5. Login: Den, password: 12345ASDF

P.S. I didn't use .env here and left all environment variables in settings.
It was done in order not to complicate the setup process.
Sorry for that if it was important, usually I do it.