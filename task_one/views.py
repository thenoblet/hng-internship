from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings 
import ip2locationio
import requests


@csrf_exempt
def hello(request):
        if request.method == "GET":
                name = request.GET.get('visitor_name', 'Guest')
                
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                        client_ip = x_forwarded_for.split(',')[0]
                else:
                        client_ip = request.META.get('REMOTE_ADDR', '')
                        
                client_city = get_location(client_ip)
                temperature = get_weather(client_city)
                
                response_data = {
        		"client_ip": client_ip,
        		"client_city": client_city,
        		"greeting": f"Hello, {name}!, the weather is {temperature} degree Celsius in {client_city}."
        	}
                
                return JsonResponse(response_data, status=200)
        
        message = {"message": "Only GET requests are allowed"}
        return JsonResponse(message, status=405)


def get_location(ip):
        configuration = ip2locationio.Configuration(settings.GEOLOCATION_API_KEY)
        ipgeolocation = ip2locationio.IPGeolocation(configuration)
        
        try:
                rec = ipgeolocation.lookup(ip)
                return rec.get('city_name', 'Unknown Location')
        except Exception as e:
                return 'Unknown Location'


def get_weather(city):
        try:
                WEATHER_API = settings.WEATHER_API_KEY
                response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric')
                weather_data = response.json()
                return weather_data['main']['temp']
        except Exception as e:
                return 'N/A'
