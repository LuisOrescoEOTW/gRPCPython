#temperature_client.py

import grpc
import temperature_pb2
import temperature_pb2_grpc

def run_uno_uno(stub):
    request = temperature_pb2.TemperatureRequest(city_code="USH")
    response = stub.uno_uno(request)
    print("Temperaturas (uno a uno):", response.temperatures)

def run_uno_muchos(stub):
    request = temperature_pb2.TemperatureRequest(city_code="MEN")
    responses = stub.uno_muchos(request)
    for response in responses:
        print("Temperaturas (uno a muchos):", response.temperatures)

def run_muchos_uno(stub):
    def generate_requests():
        for cities_codes in ["MEN", "BSA", "SAL"]:
            yield temperature_pb2.TemperatureRequest(city_code=cities_codes)

    response = stub.muchos_uno(generate_requests())
    print("Temperaturas (muchos a uno):", response.temperatures)

def run_muchos_muchos(stub):
    def generate_requests():
        for cities_codes in ["USH", "BSA", "COR"]:
            yield temperature_pb2.TemperatureRequest(city_code=cities_codes)

    responses = stub.muchos_muchos(generate_requests())
    for response in responses:
        print("Temperaturas (muchos a muchos):", response.temperatures)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = temperature_pb2_grpc.TemperatureServiceStub(channel)
        run_uno_uno(stub)
        run_uno_muchos(stub)
        run_muchos_uno(stub)
        run_muchos_muchos(stub)

if __name__ == '__main__':
    run()
