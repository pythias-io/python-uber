'''
configurations for the Uber library
'''

#
# `ENV` toggles settings for dev / prod environments
#
ENV = 'dev'  # prod

URL = dict(prod='https://api.uber.com/v1',
           dev='https://sandbox-api.uber.com/v1')
BASE_URL = URL[ENV]

STATUS = {}
STATUS['0'] = 'processing'
STATUS['1'] = 'accepted'
STATUS['2'] = 'arriving'
STATUS['3'] = 'in_progress'
STATUS['4'] = 'completed'
STATUS['5'] = 'rider_canceled'
STATUS['6'] = 'driver_canceled'
STATUS['7'] = 'no_driver_available'
