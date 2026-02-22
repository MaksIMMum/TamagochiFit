Every time you install a new package in that environment, activate the environment again.

This makes sure that if you use a terminal (CLI) program installed by that package, you use the one from your virtual environment and not any other that could be installed globally, probably with a different version than what you need.

-->(run command)
!!!

activate virtual environment (very important)
--> python -m venv .venv
--> source .venv/Scripts/activate
check:
--> which python
/home/user/code/awesome-project/.venv/bin/python
--> pip install -r requirements.txt

fastapi dev app/main.py


once done working use (also important)
--> deactivate




fastapi login

You are logged in to FastAPI Cloud 🚀

Then deploy your app:


fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
