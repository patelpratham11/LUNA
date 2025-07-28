from __future__ import print_function
import weatherapi 
import time
from pprint import pprint

def setup_weather():
    return ""

def get_weather():
    # Configure API key authorization: ApiKeyAuth
    configuration = weatherapi.Configuration()
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['key'] = 'Bearer'

    # create an instance of the API class
    api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
    q = '19335' # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
    dt = '2013-07-15' # date | Date on or after 1st Jan, 2015 in yyyy-MM-dd format

    try:
        # Astronomy API
        api_response = api_instance.forecast_weather(q, dt)
        return api_response
    except Exception as e:
        print("Exception when calling APIsApi->astronomy: %s\n" % e)




