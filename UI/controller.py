import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare prima un anno!", color="red"))
            self._view.update_page()
            return
        self._model.creaGrafo(self._view._ddAnno.value)
        n, m = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grefo correttamente creato."
                                                       f"Il grafo è costituto di {n} nodi e {m} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        if self._choiceTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Non è stata effettuata una scelta del team", color="red"))
            self._view.update_page()
            return
        viciniTuple = self._model.getVicini(self._choiceTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"il nodo {self._choiceTeam} ha {len(viciniTuple)} vicini"))
        self._view._txt_result.controls.append(ft.Text(f"di seguito una lista ordinata di vicini"))
        for v in viciniTuple:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))
        self._view.update_page()
        return

    def handlePercorso(self, e):
            pass

    def fillDDYears(self):
        """
        Questo metodo mi aggiorna i campi nel DropDown
        """
        years = self._model.getYears()

        # per riempire il dropdown o faccio cosi
        # v1
        # yearsDD = []
        # for y in years:
        #     yearsDD.append(ft.dropdown.Option(y))

        # v2
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years)) # quando uso il metodo map devo metterlo per forza in una lista
        self._view._ddAnno.options = yearsDD
        self._view.update_page()


    def handleYearSelection(self, e):
        # questo metodo viene chiamato quando qualcuno ha selezionato un anno, deve recuperare tutti
        # i team che hanno giocato quell'anno, e stamparli nel textfield, e anceh riempire
        # il dropdown sotto.
        if self._view._ddAnno.value is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text("Selezionare un anno dal menu"))
            return


        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._ddSquadra.options.clear()  # ← AGGIUNGERE QUESTO
        self._choiceTeam = None
        self._view._txtOutSquadre.controls.append(ft.Text(f"Per il {self._view._ddAnno.value} sono iscritte al campionato "
                                                       f"{len(teams)} squadre."))
        for t in teams:
            self._view._txtOutSquadre.controls.append(
                ft.Text(t))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data = t,
                                                                    text=t.name,
                                                                    on_click=self.readDDTeams))
        self._view.update_page()


    def readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam = None
        else:
            self._choiceTeam = e.control.data
        print(f"Selezionato il team {self._choiceTeam}")



