from datetime import datetime

def check_reference_date(input):
    try:
        datetime.strptime(input,'%d %b %Y')
    except:
        raise Exception("Invalid datetime format.")

def check_time_precision_format(input):
    valid_format = ['hh','hh:mm','hh:mm:ss','hh:mm:ss.0','hh:mm:ss.00','hh:mm:ss.000']
    if input not in valid_format:
        raise Exception("Invalid time precision format.")

def check_algorithm_basis(input):
    if type(input) == int and input >= 0 and input <= 1000000:
        return True
    else:
        raise Exception("Invalid algorithm basis.")

def check_address_priority(input):
    type_of_address = ['REGO', 'ABBR']
    if input not in type_of_address:
        raise Exception("Invalid address priority")

def check_fields(input):
    fields = ['EnterpriseNumber','Denomination']
    for element in input:
        if element not in fields:
            raise Exception("Invalid field.")


def check_params(parameters):
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


# Example

parameters =  {'Algorithm basis': 3333, 'Reference date': '08 Jul 1969',
    'Time precision': 'hh:mm:ss.000', 'Type of address priority': 'REGO',
    'Selected fields': ['EnterpriseNumber', 'Denomination']}

check_params(parameters)









