import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
  return {'status': 'alive'}

@app.route('/parameters', methods=['GET', 'POST'])
def parameters():
  if request.method == 'GET':
    with open('./params.json', 'r') as io:
      params = json.load(io)
    return {'params': params}
  elif request.method == 'POST':
    try:
      data = request.get_json()
      data = data['params']
      # Check data values with Ceren code
    except:
      return {"error": "Invalid data"}, 400
    # Save data to .json
    with open('./params.json', 'w') as io:
        json.dump(data, io)
    # Execute key generation 
    return {"satatus": "Params saved"}


if __name__ == '__main__':
  app.run(debug=True, port=int(os.environ.get("PORT", 8080)), host='0.0.0.0')