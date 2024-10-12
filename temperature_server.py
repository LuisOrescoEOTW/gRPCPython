#temperature_server.py

from concurrent import futures
import grpc
import temperature_pb2
import temperature_pb2_grpc

# Diccionario de ciudades con sus últimas 5 temperaturas
cities_temperatures = {
    "USH": [3.5, 4.1, 2.8, 3.9, 3.7],
    "BSA": [28.5, 27.8, 29.2, 30.0, 26.9],
    "COR": [21.3, 22.1, 23.0, 20.8, 21.5],
    "MEN": [18.0, 19.2, 17.5, 16.8, 19.1],
    "SAL": [25.7, 26.4, 24.9, 26.1, 27.0]
}

class TemperatureService(temperature_pb2_grpc.TemperatureServiceServicer):
    def uno_uno(self, request, context):
        temp = cities_temperatures.get(request.city_code, [])
        return temperature_pb2.TemperatureResponse(temperatures=temp)

    def uno_muchos(self, request, context):
        temps = cities_temperatures.get(request.city_code, [])
        for temp in temps:
            yield temperature_pb2.TemperatureResponse(temperatures=[temp])

    def muchos_uno(self, request_iterator, context):
        all_temperatures = []
        for request in request_iterator:
            all_temperatures.extend(cities_temperatures.get(request.city_code, []))
        return temperature_pb2.TemperatureResponse(temperatures=all_temperatures)
                
    def muchos_muchos(self, request_iterator, context):
        all_temperatures = []
        for request in request_iterator:
            temperatures = cities_temperatures.get(request.city_code, [])
            all_temperatures.extend(temperatures)
        for temp in all_temperatures:
            yield temperature_pb2.TemperatureResponse(temperatures=[temp])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    temperature_pb2_grpc.add_TemperatureServiceServicer_to_server(TemperatureService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
