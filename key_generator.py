import datetime
import timeit

def to_unicode(string: str) -> int:
  '''
    Converts string to sum of unicode caracters
  '''
  res = 0
  for i in string:
    res += ord(i)
  return res

def get_modulo(nbr: int) -> str:
  '''
    Compute modulo on number, then convert to string and fill with Zeros to reach the same length as the modulo value
  '''
  modulo = str(nbr % settings.get("basis"))
  return modulo.zfill(basis_len)

def get_timestamp(reference_date: datetime.datetime, precision: str) -> int:
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

def generate_key(columns: list, settings: dict) -> str:
  '''
    Concatenate timestamp and unicode modulo
  '''
  key = str(get_timestamp(datetime.datetime.strptime(settings.get('reference_date'), '%d %b %Y'), \
    settings.get('precision')))
  for column in columns:
    key += get_modulo(to_unicode(column))

  return key


if __name__ == "__main__":
  settings = {'basis': 3333, 'reference_date': '08 Jul 1969',
    'precision': 'hh:mm:ss.000', 'address_priority': 'REGO', 
    'fields': ['EnterpriseNumber', 'Denomination']}
  now = datetime.datetime.now()
  basis_len = len(str(settings.get("basis")))

  # Columns values
  number = '0200.065.765'
  denomination = 'Intergemeentelijke Vereniging Veneco'
  print(generate_key([number, denomination], settings))

  