import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def get_teams(self, year):
        return self._model.get_teams(year)

    def handle_crea_grafo(self, e ):
        """ Handler per gestire creazione del grafo """""
        try:
            year = int(self._view.dd_anno.value)
        except Exception:
            self._view.show_alert("Anno Invalido")
            return

        self._model.build_graph(year)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""

        team_id = int(self._view.dd_squadra.value)
        team = self._model._id_map.get(team_id)
        if team is None: #
            print(f"Team con ID {team_id} non trovato!")
            return

        self._view.txt_risultato.controls.clear()
        for n, w in self._model.get_neighbors(self._model._id_map[team_id]):
            self._view.txt_risultato.controls.append(
                ft.Text(f"{n} - peso {w}")
            )

        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        pass
        # TODO

    """ Altri possibili metodi per gestire di dd_anno """""

    def get_years(self):
        return self._model.get_years()

    def handle_year_change(self, e):
        year = int(self._view.dd_anno.value)
        teams = (self._model.load_teams(year))

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(teams)}"))

        for t in teams:
            self._view.txt_out_squadre.controls.append(ft.Text(t))

        self._view.dd_squadra.options = [ft.dropdown.Option(key=str(t.id), text= t.team_code)
                                         for t in teams]

        self._view.update()