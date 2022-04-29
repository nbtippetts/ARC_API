#main.py
import os
from app.app import create_app

app = create_app('production')
app.run()
