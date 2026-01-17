import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):

        self.G = nx.Graph()
        self._nodes = []
        self._edges = []
        self._id_map = {}

        self._lista_teams= []
        self._lista_coppie = []

    def get_years(self):
        return DAO.get_years_from_1980()

    def get_teams(self, year):
        return DAO.get_teams(year)

    def load_teams(self, year):
        self._lista_teams = DAO.get_teams(year)
        return self._lista_teams

    def load_coppie(self, year):
        self._lista_coppie = DAO.get_all_coppie(year)
        return self._lista_coppie

    def build_graph(self, year):
        self._nodes = []
        self._edges = []
        self._id_map = {}
        self.load_teams(year)
        self.load_coppie(year)
        self.G.clear()

        for team in self._lista_teams:
            self._nodes.append(team)
            self._id_map[team.id] = team
        self.G.add_nodes_from(self._nodes)

        # recuperiamo i salari dal dao (è già un dict {team_code: total})
        mappa_salari = DAO.get_team_salary(year) or {}

        for id1, id2 in self._lista_coppie:
            if id1 in self._id_map and id2 in self._id_map:

                t1 = self._id_map[id1]
                t2 = self._id_map[id2]
                #peso = self._calcola_peso(coppia)
                #if peso is not None:
                    #self.G.add_edge(t1, t2, weight=peso)

                peso = self._calcola_peso(t1,t2, mappa_salari)
                if peso > 0:
                    self.G.add_edge(t1, t2, weight=peso)
        self._id_map = {t.id : t for t in self._lista_teams}

    def get_neighbors(self, team):
        vicini = [] #lista vuota per la coppia (squadra vicina, peso)
        for neighbor in self.G.neighbors(team): #ciclo for che itera su tutti i nodi vicini della squadra
            w = self.G[team][neighbor]["weight"] #accede ai dati dell'arco che collega team a neighbor per estrarre il valore salvato sotto chiave 'weight'
            vicini.append((neighbor, w))  #aggiunge la lista 'vicini' una tupla contenente l'oggetto squadra vicina e il peso
        return sorted(vicini, key=lambda x: x[1], reverse=True)# Restituisce la lista ordinata: 'key=lambda x: x[1]' dice di ordinare in base al secondo elemento (il peso),
    #    e 'reverse=True' mette i pesi più alti all'inizio della lista.

    def _calcola_peso(self, t1, t2, mappa_salari):
        salario_t1 = mappa_salari.get(t1.team_code, 0.0)
        salario_t2 = mappa_salari.get(t2.team_code, 0.0)
        return salario_t1 + salario_t2



