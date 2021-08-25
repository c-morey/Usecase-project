import os
import json
from flask import Flask, request

from utils.key_generation import generate_key
from utils.param_validation import check_params

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
      check_params(data)
    except Exception as e:
      return {"error": str(e)}, 400
    except:
      return {"error": "An unexpected error occured"}, 400
    # Save data to .json
    with open('./params.json', 'w') as io:
        json.dump(data, io)
    return {"status": "Params saved"}

@app.route('/process', methods=['POST'])
def process():
  with open('./params.json', 'r') as io:
    params = json.load(io)

  # Execute key generation (get batch)
  columns = ['0200.065.765', 'Intergemeentelijke Vereniging Veneco'] # This info should come from DB
  print(generate_key(columns, params)) # This should be saved in DB
  # Write batch (save the keys in table)
  return {}

@app.route('/results', methods=['GET', 'POST'])
def review_results():
  if request.method == 'GET':
    return {'results': "Ask for Entreprise Number"}
  elif request.method == 'POST':
    try:
      data = request.get_json()
      data = data['number']
      # Requests matching enterprise numbers, returns matching key
      '''
      return
        {
          'inputs': []
          'output': key
        }
      '''
    except Exception as e:
      return {"error": str(e)}, 400
    except:
      return {"error": "An unexpected error occured"}, 400


if __name__ == '__main__':
  app.run(debug=True, port=int(os.environ.get("PORT", 8080)), host='0.0.0.0')