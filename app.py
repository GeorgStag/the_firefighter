from shiny import App
from scripts import server, ui


server = server.server
app_ui = ui.app_ui

app = App(app_ui, server)