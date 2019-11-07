from workerA import add_nums
from workerB import sub_nums
from flask import (
   Flask,
   request,
   jsonify,
)

app = Flask(__name__)

@app.route("/add")
def add():
   print('CHRIS')
   first_num = 5
#   first_num = request.args.get('first_num')
   second_num = 10
#   second_num = request.args.get('second_num')
   result = add_nums.delay(first_num, second_num )
   return jsonify({'result': result}), 200


@app.route("/subtract")
def subtract():
   print('CHRIS')
   first_num = request.args.get('first_num')
   second_num = request.args.get('second_num')
   result = sub_nums.delay(first_num, second_num )
   return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
