from datetime import datetime

def check_reference_date(input: datetime):
    '''
    Check if given reference date format is correct. If not, raise exception.
    '''
    try:
        date = datetime.strptime(input,'%d %b %Y')
    except:
        raise Exception("Invalid datetime format")
    now = datetime.now()
    if date > now:
      raise Exception ("Reference Date is in the future")

def check_time_precision_format(input: str):
    '''
    Check if given precision format is correct. If not, raise exception.
    '''
    valid_format = ['hh:mm:ss','hh:mm:ss.0','hh:mm:ss.00','hh:mm:ss.000']
    if input not in valid_format:
        raise Exception("Invalid time precision format")

def check_algorithm_basis(input: int):
    '''
    Check if given algorithm basis is correct. It shoudl be an int type, bigger than 0 and less than 1e6. If not, raise exception.
    '''
    if type(input) != int:
        raise Exception("Algorithm basis must be an integer")
    elif input < 0 or input > 10 ** 6:
      raise Exception("Algorithm basis value must be stricly positive and shorter than 10e6")

def check_address_priority(input: str):
    '''
    Check if given type of address is correct. If not, raise exception.
    '''
    type_of_address = ['REGO', 'ABBR']
    if input not in type_of_address:
        raise Exception("Invalid address priority")

def check_fields(input: str):
    '''
    Check if selected fields is inside the available fields list. If not, raise exception.
    '''
    fields = ['EnterpriseNumber','Denomination']
    for element in input:
        if element not in fields:
            raise Exception("Invalid fields")

def check_params(parameters: dict):
    '''
    The main function that will run each parameter validation.
    :param parameters: dict of user input
    :return: No return
    '''
    check_time_precision_format(parameters.get('time_precision'))
    check_reference_date(parameters.get('reference_date'))
    check_algorithm_basis(parameters.get('algorithm_basis'))
    check_address_priority(parameters.get('type_of_address_priority'))
    check_fields(parameters.get('selected_fields'))








