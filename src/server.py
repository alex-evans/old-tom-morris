
from flask import Flask

import data_pull


app = Flask(__name__)


@app.route('/')
def hello_world() -> str:
   return 'Hello Golf'


@app.route('/pulldata')
def pull_data() -> str:
   data_pull.run_data_init()

   return 'Data Successfully Pulled'

if __name__ == '__main__':
   app.run()
