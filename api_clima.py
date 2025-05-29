import requests
import json

api_key = "f01887007c8fa3a0cacd8b1154c4f96f"

def pegar_Coordenadas():
    print("Buscando coordenadas IP")
    try:
        # timeout é o tempo maximo para obter a resposta
        r = requests.get('http://www.geoplugin.net/json.gp', timeout=10)
        print(f"Status da requisição geoplugin: {r.status_code}") # Para depuração
        r.raise_for_status()
        
        local = r.json()
        coordenadas = {}
        coordenadas['lat'] = local.get('geoplugin_latitude')
        coordenadas['long'] = local.get('geoplugin_longitude')

        if coordenadas['lat'] and coordenadas['long']:
            print(f"Coordenadas obtidas por IP: Lat={coordenadas['lat']}, Long={coordenadas['long']}")
            return coordenadas
        else:
            print('Não foi possível extrair latitude/longitude da resposta do geoplugin.')
            return None

    except requests.exceptions.Timeout:
        print('Timeout ao tentar obter localização por IP.')
        return None

def obter_nome_local(lat, long, api_key_param): 
    if lat is None or long is None:
        print("Latitude ou longitude invalida")
        return None
    reverse_geo_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={long}&limit=1&appid={api_key_param}"
    try:
        r = requests.get(reverse_geo_url, timeout=10)
        print(f"Status da requisição reverse geocoding OWM: {r.status_code}")
        r.raise_for_status()
        location_response = r.json()
        if location_response: # Resposta é uma lista
            nome_local_info = location_response[0]
            cidade = nome_local_info.get('name', 'N/A')
            pais = nome_local_info.get('country', 'N/A')
            info_formatada = f"{cidade}, {pais}"
            print(f"Nome do local obtido: {info_formatada}")
            return {"nomeLocal": info_formatada}
        else:
            print("Não foi possível obter o nome do local pela OpenWeatherMap.")
            return None       
    except requests.exceptions.Timeout:
        print('Timeout ao tentar obter nome do local pela OpenWeatherMap.')
        return None

def obter_previsao_dias(lat, long, api_key_param, num_dias_cnt=5): 
    if lat is None or long is None:
        print("latitude ou longitude invalida para buscar previsão do tempo.")
        return None 

    url_previsao_diaria= f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={long}&cnt={num_dias_cnt}&appid={api_key_param}&units=metric&lang=pt_br"
    try:
        r = requests.get(url_previsao_diaria, timeout=10)
        print(f"Status da requisição /forecast/daily OWM: {r.status_code}") # Adicionado print de status
        r.raise_for_status()
        forecast_response = r.json()
        if 'list' in forecast_response and forecast_response['list']:
            # A mensagem agora reflete o número de dias de fato retornados pela API (controlado por 'cnt')
            print(f"\n--- Previsão para os Próximos {len(forecast_response['list'])} Dias ---")
            infoClima = []
            for i, dia_forecast in enumerate(forecast_response['list']): 
                climaDia = {}
                climaDia['dia'] = i + 1
                climaDia['chuva_mm'] = dia_forecast.get('rain', 0) 
                climaDia['pop'] = dia_forecast.get('pop', 0) * 100      
                infoClima.append(climaDia)
            return infoClima
        else:         
            print("Não foi encontrada a chave 'list' na resposta da previsão ou ela está vazia.")
            return None 
    except requests.exceptions.Timeout:
        print('Timeout ao tentar obter previsão do tempo pela OpenWeatherMap (/forecast/daily).')
        return None 

def calcula_Probabilidade(lista_previsoes):
    # para calcular a probabilidade de chuva nos proximos dias 
    soma_probabilidades = 0
    count_dias = 0
    for dia in lista_previsoes:
        # pra saber se pop vei e é um  numero
        if 'pop' in dia and isinstance(dia['pop'], (int,float)):
            soma_probabilidades += dia['pop']
            count_dias += 1
        else:
            print(f"Aviso dia sem 'pop' válido ou 'pop' não é numérico.")
    media = soma_probabilidades / count_dias
    return media

def volume_NextDays(lista_previsoes):
    # para estimar o volume de chuva nos proximos dias 
    volume = 0
    for prev in lista_previsoes:
        volume += prev['chuva_mm']
    return volume

if __name__ == '__main__':   
    coordenadas_ip = pegar_Coordenadas()
    if coordenadas_ip and coordenadas_ip.get('lat') and coordenadas_ip.get('long'):
        lat_atual = coordenadas_ip['lat']
        long_atual = coordenadas_ip['long']

        info_do_local = obter_nome_local(lat_atual, long_atual, api_key) # Passando a api_key global
        if info_do_local:
            print(f"Informações do Local (baseado no IP): {info_do_local.get('nomeLocal', 'N/A')}")
        else:
            print("Não foi possível obter o nome do local para as coordenadas do IP.")

        previsoes = obter_previsao_dias(lat_atual, long_atual, api_key) 
        if previsoes: 
            print(previsoes) 
            proximos_volumes = volume_NextDays(previsoes)
            probabilidade_chuva = calcula_Probabilidade(previsoes)
            print(f'Estimativa volume chuva: {proximos_volumes}')
            print(f"Probabilidade média de chuva para os próximos {probabilidade_chuva:.2f}%")
        else:
            print("Não foi possível obter ou processar a previsão do tempo.")
    else:
        print("Não foi possível determinar as coordenadas baseadas no IP. Encerrando.")