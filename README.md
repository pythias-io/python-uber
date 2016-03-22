# Python library for Uber API #

### Dependencies ###

* python ( tested on 2.7 )
* [python-requests](http://docs.python-requests.org/en/latest/)
* Uber developer account and application client ID: https://developer.uber.com/

### Usage ###
    
```
#!python

from uber import Api
uber = Api.Uber(SERVER_TOKEN = '123456ABCDEF9876XYZ', user_token='ghij3456klmnop89101112')
start = {'latitude': -1.2919211, 'longitude': 36.8248215}
stop = {'latitude': -1.2866975, 'longitude': 36.8252936}
price = uber.get_price_estimate(start, stop)
time = uber.get_time_estimate(start, stop)
req = uber.request('mnoxp-123abc-stuv456-lmnoq-trf32', start, stop)
status = uber.request_details(req['request_id'])
```

### Endpoints Implemented ###

* /products
* /products/{product_id}
* /estimates/price
* /estimates/time
* /promotions
* /me
* /requests
* /requests/{request_id}
* /sandbox/requests/{request_id}


### Who do I talk to? ###

engineering@pythias.tech
