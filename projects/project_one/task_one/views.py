from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings 
import ip2locationio
import requests


@csrf_exempt
def hello(request):
        """
        Handle a GET request to provide a personalized greeting and weather information.

        This view function extracts the visitor's IP address and city, retrieves the 
        current weather for that city, and returns a JSON response with the information.

        Args:
                request: The HTTP request object.

        Returns:
                JsonResponse: A JSON response containing the visitor's IP, city, and a 
                personalised greeting with the current weather.

        If the request method is not GET, returns a JSON response indicating only GET 
        requests are allowed with status 405.
        """
        if request.method == "GET":
                name = request.GET.get('visitor_name', 'Guest')
                
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                        client_ip = x_forwarded_for.split(',')[0]
                else:
                        client_ip = request.META.get('REMOTE_ADDR', '')
                
                # client_city = 'Kasoa'      
                client_city = get_location(client_ip)
                temperature = get_weather(client_city)
                
                response_data = {
        		"client_ip": client_ip,
        		"location": client_city,
        		"greeting": f"Hello, {name}!, the weather is {temperature} degree Celsius in {client_city}."
        	}
                
                return JsonResponse(response_data, status=200)
        
        message = {"message": "Only GET requests are allowed"}
        return JsonResponse(message, status=405)


def get_location(ip):
        """
        Get the city name for a given IP address using the IP2Location API.

        Args:
                ip (str): The IP address to lookup.

        Returns:
                str: The city name associated with the IP address. Returns 'Unknown Location' 
                if the city cannot be determined or an error occurs.
        """
        configuration = ip2locationio.Configuration(settings.GEOLOCATION_API_KEY)
        ipgeolocation = ip2locationio.IPGeolocation(configuration)
        
        try:
                rec = ipgeolocation.lookup(ip)
                return rec.get('city_name', 'Unknown Location')
        except Exception as e:
                return 'Unknown Location'


def get_weather(city):
        """
        Get the current temperature for a given city using the OpenWeatherMap API.

        Args:
                city (str): The city name to get the weather for.

        Returns:
                str: The current temperature in Celsius. Returns 'N/A' if the temperature 
                cannot be determined or an error occurs.
        """
        try:
                api_key = settings.WEATHER_API_KEY
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                        
                response = requests.get(url)
                weather_data = response.json()
                temperature = weather_data['main']['temp']
                return temperature
        except Exception as e:
                return "N/A"
