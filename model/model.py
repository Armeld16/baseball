import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = None

    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)
        """"
        Siccome per gli archi mi servono i nodi, qui non ho bisogno di una query, ma devo collegarli , 
        la più semplice è questa 
        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v: 
                    self._grafo.add_edge(u,v)
        siccome non è la piu bella scriverla cosi, posso scrivere : con una combination"""

         # metto i nodi e quante cominazione voglio fare a 2 a 2

        myedges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(myedges)
        mapSalary = DAO.getSalariesOfTeam(year, self._idMapTeams)
        for e in self._grafo.edges:
            sal1 = mapSalary.get(e[0], 0)
            sal2 = mapSalary.get(e[1], 0)
            peso = sal1 + sal2
            self._grafo[e[0]][e[1]]["weight"] = sal1 + sal2
            # self._grafo[e[0]][e[1]]["weight"] = mapSalary[e[0]] + mapSalary[e[1]] le 4 righe prima le posso scrivere anche cosi
        print("test")

    def getVicini(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]["weight"]))

        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        return viciniTuples


    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYears(year)
        self._idMapTeams = {t.ID: t for t in self._teams}
        return self._teams


    def getYears(self):
        return DAO.getAllYears()

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

