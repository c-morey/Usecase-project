from datetime import datetime

def check_reference_date(input: datetime):
    '''
    Check if given reference date format is correct. If not, raise exception.
    '''
    try:
        datetime.strptime(input,'%d %b %Y')
    except:
        raise Exception("Invalid datetime format.")

def check_time_precision_format(input: str):
    '''
    Check if given precision format is correct. If not, raise exception.
    '''
    valid_format = ['hh','hh:mm','hh:mm:ss','hh:mm:ss.0','hh:mm:ss.00','hh:mm:ss.000']
    if input not in valid_format:
        raise Exception("Invalid time precision format.")

def check_algorithm_basis(input: int):
    '''
    Check if given algorithm basis is correct. It shoudl be an int type, bigger than 0 and less than 1e6. If not, raise exception.
    '''
    if type(input) == int and 0 <= input <= 1000000:
        return True
    else:
        raise Exception("Invalid algorithm basis.")

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
            raise Exception("Invalid field.")

def check_params(parameters: dict):
    '''
    The main function that will run each parameter validation.
    :param parameters: dict of user input
    :return: No return
    '''
    check_time_precision_format(parameters.get('Time precision'))
    check_reference_date(parameters.get('Reference date'))
    check_algorithm_basis(parameters.get('Algorithm basis'))
    check_address_priority(parameters.get('Type of address priority'))
    check_fields(parameters.get('Selected fields'))


parameters =  {'Algorithm basis': 3333, 'Reference date': '08 Jul 1969',
    'Time precision': 'hh:mm:ss.000', 'Type of address priority': 'REGO',
    'Selected fields': ['EnterpriseNumber', 'Denomination']}

check_params(parameters)









