import os
import json
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.key_generation import generate_key
from utils.param_validation import check_params
from utils.db_connections import Session, write_batch, fetch_batch, fetch_key, fetch_records, reset_results

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
  batch = fetch_batch(Session)
  results = []
  for columns in batch:
    results.append(generate_key(columns, params)) # This should be saved in DB
  write_batch(results)
  return {}

@app.route('/results', methods=['GET', 'POST'])
def review_results():
  if request.method == 'GET':
    return {'results': "Ask for Entreprise Number"}
  elif request.method == 'POST':
    try:
      with open('./params.json', 'r') as io:
        params = json.load(io)
      data = request.get_json()
      enterprise_number = data['number']
      inputs = fetch_records(Session, enterprise_number)
      output = fetch_key(Session, inputs, params['type_of_address_priority'])
      return {
          'inputs': inputs,
          'output': output
        }

    except Exception as e:
      return {"error": str(e)}, 400
    except:
      return {"error": "An unexpected error occured"}, 400


if __name__ == '__main__':
  app.run(debug=True, port=int(os.environ.get("PORT", 8080)), host='0.0.0.0')