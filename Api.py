"""
UBER API Client Library

Usage:
    >>> from uber import Api
    >>> api = Api.Uber(**credentials)
    >>> api.get_profile()
"""

__all__ = ['Api']

import json
import config
import urllib
import requests
from config import BASE_URL


class UberApiError(Exception):
  '''Base class for Uber API errors'''

  @property
  def message(self):
    '''Returns the first argument used to construct this error.'''
    return self.args[0]


class Uber(object):
    """
    """
    def __init__(self, **credentials):
        self.url = BASE_URL
        self.server_token = credentials.get('SERVER_TOKEN')
        self.user_token = credentials.get('user_token')
        print self.url


    def authenticate(self, bearer=False, user_token=''):
        '''
        returns authentication header
        '''
        if bearer:
            request_headers = dict(Authorization='Bearer {}'.format(
                self.user_token))
        else:
            request_headers = dict(Authorization='Token {}'.format(
                self.server_token))
        return request_headers


    def validate_response(self, resp):
        '''
        validates response from Uber API.
        No action if status code is 200
        Else, raise custom exception
        '''
        msg = "Unexpected response - HTTP:{} - payload: {}".format(
                resp.status_code, resp.content)
        if resp.status_code not in (200, 202):
            # 202 for Request
            raise UberApiError(msg)


    def get_products(self, latitude, longitude):
        '''
        returns information about the Uber products offered at a 
        given location
        '''
        url = self.url + '/products'
        params = dict(latitude=latitude,
                longitude=longitude)
        resp = requests.get(url, data=params, headers=self.authenticate())
        self.validate_response(resp)
        return json.loads(resp.content)


    def get_product(self, product_id):
        '''
        return individual product details
        '''
        url = self.url + '/products/{}'.format(str(product_id))
        params = dict(product_id=product_id)
        resp = requests.get(url, data=params, headers=self.authenticate())
        self.validate_response(resp)
        return json.loads(resp.content)


    def get_price_estimate(self, start, end):
        '''
        returns an estimated price range for each product
        offered at a given location

        @param   start   <dict>   contains keys: `latitude` and `longitude`
        @param   end     <dict>   contains keys: `latitude` and `longitude`
        '''
        try:
            assert isinstance(start, dict)
            assert isinstance(end, dict)
            assert 'latitude' in start
            assert 'longitude' in start
            assert 'latitude' in end
            assert 'longitude' in end
        except AssertionError:
            raise UberApiError("Incorrect request parameters - "
                    "start: {} - end: {}".format(start, end))
        url = self.url + '/estimates/price'
        params = dict(start_latitude=start.get('latitude'),
                    start_longitude=start.get('longitude'),
                    end_latitude=end.get('latitude'),
                    end_longitude=end.get('longitude'))
        url = url + '?%s' % urllib.urlencode(params)
        resp = requests.get(url, headers=self.authenticate())
        self.validate_response(resp)
        return json.loads(resp.content)

    
    def get_time_estimate(self, start, customer_id=None, product_id=None):
        '''
        returns ETAs for all products offered at a given location

        @param   start   <dict>  contains keys: `latitude` and `longitude`
        @param   customer_id  <str>   Optional
        @param   product_id   <str>   Optional
        '''
        try:
            assert isinstance(start, dict)
            assert 'latitude' in start
            assert 'longitude' in start
        except AssertionError:
            raise UberApiError("Incorrect request parameters - "
                    "start: {} - end: {}".format(start, end))
        url = self.url + '/estimates/time'
        params = dict(start_latitude=start.get('latitude'),
                    start_longitude=start.get('longitude'))
        if customer_id:
            params['customer_uuid'] = str(customer_id)
        if product_id:
            params['product_id'] = str(product_id)
        url = url + '?%s' % urllib.urlencode(params)
        resp = requests.get(url, headers=self.authenticate())
        self.validate_response(resp)
        return json.loads(resp.content)


    def get_promotions(self, start={}, end={}):
        '''
        returns information about the promotion that will be
        available to a new user based on their activity's location

        @param   start   <dict>   contains keys: `latitude` and `longitude`
        @param   end     <dict>   contains keys: `latitude` and `longitude`

        At least one valid set of coordinates is required.
        '''
        try:
            assert (isinstance(start.get('latitude'), float) and\
                            isinstance(start.get('longitude'), float)) or\
                            (isinstance(end.get('latitude'), float) and\
                            isinstance(end.get('longitude'), float))
        except AssertionError:
            raise UberApiError("Incorrect parameters - start: {} - end: {}".format(start, end))
        url = self.url + '/promotions'

        params = dict(start_latitude=start.get('latitude'),
                    start_longitude=start.get('longitude'),
                    end_latitude=end.get('latitude'),
                    end_longitude=end.get('longitude'))
        url = url + '?%s' % urllib.urlencode(params)
        resp = requests.get(url, headers=self.authenticate())
        self.validate_response(resp)
        return json.loads(resp.content)


    def get_profile(self,):
        try:
            url = self.url + '/me'
            resp = requests.get(url, headers=self.authenticate(bearer=True))
            self.validate_response(resp)
            return json.loads(resp.content)
        except Exception, err:
            error = 'cannot get profile - {}'.format(str(err))
            raise UberApiError(error)


    def request(self, product_id, start, end):
        '''
        allows a ride to be requested on behalf of an Uber user
        given their desired product, start, and end locations

        @param  product_id  <str>  product requested
        @param   start   <dict>  contains keys: `latitude` and `longitude`
        @param   end     <dict>  contains keys: `latitude` and `longitude`
        '''
        try:
            assert isinstance(start, dict)
            assert isinstance(end, dict)
            assert 'latitude' in start
            assert 'longitude' in start
            assert 'latitude' in end
            assert 'longitude' in end

            url = self.url + '/requests'
            params = dict(product_id=str(product_id),
                        start_latitude=start.get('latitude'),
                        start_longitude=start.get('longitude'),
                        end_latitude=end.get('latitude'),
                        end_longitude=end.get('longitude'))
            request_headers = self.authenticate(bearer=True)
            request_headers['Content-Type'] = 'application/json'
            resp = requests.post(url, data=json.dumps(params),
                    headers=request_headers)
            self.validate_response(resp)
            return json.loads(resp.content)
        
        except AssertionError:
            raise UberApiError("Incorrect request parameters - "
                    "start: {} - end: {}".format(start, end))

        except Exception, err:
            error = 'Uber.request() fail - {}'.format(str(err))
            raise UberApiError(error)


    def request_details(self, request_id):
        '''
        Get the real time status of an ongoing trip that was
        created using the Ride Request endpoint
        '''
        try:
            url = self.url + '/requests/{}'.format(str(request_id).strip())
            resp = requests.get(url, headers=self.authenticate(bearer=True))
            self.validate_response(resp)
            return json.loads(resp.content)

        except Exception, err:
            error = 'Uber.request_details() fail - {}'.format(str(err))
            raise UberApiError(error)

    def sandbox_modify_request(self, request_id, new_status):
        '''
        modifies the status of an ongoing sandbox Request

        @param   request_id   <str>    id of the request to modify
        @param   status       <str>    status to modify to
         ( see config for all possible values for `status` )
        '''
        try:
            url = self.url + '/sandbox/requests/{}'.format(request_id)
            status_update = dict(status=new_status)
            params = json.dumps(status_update)
            request_headers = self.authenticate(bearer=True)
            request_headers['Content-Type'] = 'application/json'
            resp = requests.put(url, data=params, headers=request_headers)
            if resp.status_code == 204:
                return True
            else:
                return False
        except Exception, err:
            error = 'SANDBOX: could not update request status - {}'.format(str(err))
            raise UberApiError(error)
