import datetime
from threading import Thread

class ProcThread(Thread):
  '''
  This class defines a classic thread targetting a function. The only differences are:
  | 1) It relies on try statement so as not to break if the target function breaks
  | 2) It stores the returned values of the target function in a .data attribute
  '''

  def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
    Thread.__init__(self, group, target, name, args)
    self.data = []
    self._target = target
    self._args = args
    self._kwargs = kwargs

  def run(self):
    for batch, params in self._args:
      for columns in batch:
        try:
          self.data.append(self._target(columns, params))
        except:
          raise Exception('Key generation failed')

def generate_key(columns: list, settings: dict) -> dict:
  '''
    Concatenate timestamp and unicode modulo
  '''
  index = columns[0]
  columns = columns[1:]
  now = datetime.datetime.now()

  key = str(get_timestamp(datetime.datetime.strptime(settings.get('reference_date'), '%d %b %Y'), \
    now, settings.get('time_precision')))
  for column in columns:
    key += get_modulo(to_unicode(column), settings.get('algorithm_basis'))

  return {'id': index, 'algo_key': key}

def to_unicode(string: str) -> int:
  '''
    Converts string to sum of unicode caracters
  '''
  res = 0
  for i in string:
    res += ord(i)
  return res

def get_modulo(nbr: int, basis: int) -> str:
  '''
    Compute modulo on number, then convert to string and fill with Zeros to reach the same length as the modulo value
  '''
  basis_len = len(str(basis))
  modulo = str(nbr % basis)
  return modulo.zfill(basis_len)

def get_timestamp(reference_date: datetime.datetime, now: datetime.datetime, precision: str) -> int:
  '''
    Returns a timestamp between a given date & now
  '''
  if reference_date < now:
    seconds = (now - reference_date).total_seconds()
    if precision == 'hh:mm:ss':
      return int(round(seconds))
    elif precision == 'hh:mm:ss.0':
      return int(round(seconds, 1) * 10)
    elif precision == 'hh:mm:ss.00':
      return int(round(seconds, 2) * 100)
    elif precision == 'hh:mm:ss.000':
      return int(round(seconds, 3) * 1000)
    else:
      raise Exception ('Precision is not well formated')
  else:
    raise Exception ('Reference Date is in the future')