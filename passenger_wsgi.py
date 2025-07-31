import sys
import os

# Ensure your app directory is in the path (in case cPanel is weird about cwd)
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application