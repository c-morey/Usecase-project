import os
import json
import math
import time
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.key_generation import generate_key, ProcThread
from utils.param_validation import check_params
from utils.db_connections import Session, write_batch, fetch_batch, fetch_key, fetch_records, reset_results, check_results

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
    reset_results(Session)
    return {"status": "Params saved"}

@app.route('/process', methods=['GET'])
def process():
  start = time.perf_counter()
  with open('./params.json', 'r') as io:
    params = json.load(io)

  # batch = fetch_batch(Session)
  # Execute key generation (get batch)
  # for columns in batch:
  #   results.append(generate_key(columns, params))
  # write_batch(results)

  db_length = 2e6
  offset = check_results(Session)
  n_iter = math.ceil((db_length - offset) / 50000) # This gives the number of 50000-batch necessary to process the remaining data

  results = []
  threads = []

  for i in range(1,3,1):
    batch = fetch_batch(Session, batch_number=i, offset=offset)
    t = ProcThread(name='thread_{}'.format(i), target=generate_key, args=((batch,params),))
    t.start()
    threads.append(t)

  print(time.time() - start)

  for thread in threads:
    while thread.is_alive():
      time.sleep(0.5)
    results.extend(thread.data)

  print(time.time() - start)
  print(len(results))
  write_batch(results)
  end = time.perf_counter()
  return {"status": f"Keys generated in {end - start:.3f}s"}

@app.route('/reset', methods=['GET'])
def reset_table():
  reset_results(Session)
  return {'migration_status': "Table results successfully reset"}

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
      output = [str(x) for x in fetch_key(Session, inputs, params['type_of_address_priority'])]
      records = [str(x) for x in inputs]
      results = {
          'inputs': records,
          'output': output[1]
        }
      print(type(results['output'][1]))
      results = json.dumps(results)
      return results

    except Exception as e:
      return {"error": str(e)}, 400
    except:
      return {"error": "An unexpected error occured"}, 400


if __name__ == '__main__':
  app.run(debug=True, port=int(os.environ.get("PORT", 8080)), host='0.0.0.0')