from django.http import JsonResponse
import ip2locationio
import requests


def hello(request):
        
        name = request.GET.get('visitor_name', 'Guest')
        client_ip = request.META.get('REMOTE_ADDR', '')
        client_city = get_location(client_ip)
        temperature = get_weather(client_city)
        
        response_data = {
		"client_ip": client_ip,
		"client_city": client_city,
		"greeting": f"Hello, {name}!, the weather is {temperature} degree Celsius in {client_city}."
	}
        
        return JsonResponse(response_data)


def get_location(ip):
        GEOLOCATION_API_KEY = "ADB2AA9BE78EC4F52D61EDA4BB156F8A"
        configuration = ip2locationio.Configuration(GEOLOCATION_API_KEY)
        ipgeolocation = ip2locationio.IPGeolocation(configuration)
        
        try:
                rec = ipgeolocation.lookup(ip)
                return rec.get('city_name', 'Unknown Location')
        except Exception as e:
                return 'Unknown Location'


def get_weather(city):
        WEATHER_API_KEY = "5267f59717294cc8688c24d664ab19ca"
        try:
                response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')
                weather_data = response.json()
                return weather_data['main']['temp']
        except Exception as e:
                return 'N/A'
