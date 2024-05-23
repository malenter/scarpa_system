import json
from usuairo.models import Departamento, Ciudad


class DepartamentoSeed:
    def __init__(self) -> None:
        with open("colombia.json", encoding="utf8") as data:
            self.departamentos = json.load(data)

    def should_run(self):
        return Departamento.objects.count() == 0

    def run(self):
        for departamento in self.departamentos:
            departamento_model = Departamento(name=departamento["departamento"])
            departamento_model.save()
            ciudades = departamento["ciudades"]
            for ciudad in ciudades:
                ciudad_model = Ciudad(name=ciudad, departamento=departamento_model)
                ciudad_model.save()