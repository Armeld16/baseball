from model.model import Model

mymodel = Model()
mymodel.getTeamsOfYear(2012)
mymodel.creaGrafo(2012)
nodi, archi = mymodel.getGraphDetails()
print(f"Grafo creato!, il grafo ha {nodi} nodi {archi} archi")