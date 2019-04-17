from utils import before_request


@before_request(priority=20)
def validate_login():
    print('validating login')
