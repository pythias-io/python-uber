#
# `env` toggles settings for dev / prod environments
#
env = 'dev'  #prod

URL = dict(prod='https://api.uber.com/v1',
        dev='https://sandbox-api.uber.com/v1')
BASE_URL = URL[env]

STATUS = {}
STATUS['0'] = 'processing'
STATUS['1'] = 'accepted'
STATUS['2'] = 'arriving'
STATUS['3'] = 'in_progress'
STATUS['4'] = 'completed'
STATUS['5'] = 'rider_canceled'
STATUS['6'] = 'driver_canceled'
STATUS['7'] = 'no_driver_available'
