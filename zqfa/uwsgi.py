import sys
print("uwsgi zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz " + str(sys.path))
from zqfa.app import create_app

app = create_app()

