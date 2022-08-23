from shiny import ui
from htmltools import HTML, div


app_ui = ui.page_fluid(

    ui.panel_title("", "WebApp: The_Firefighter"),

    ui.layout_sidebar(

        ui.panel_sidebar(
            div(HTML("<h4> Fire Occurrences in Time: </h4>")),
            ui.input_slider("time_period_sl", "Time Period (years):", 1992, 2015, [1992,2015]),
            ui.input_text("state_txt", "State:", 'All'),

            div(HTML("<h5> ----------------------------------------------------------------------------- </h5>")),
            div(HTML("<h4> Counties prone to fire: </h4>")),
            ui.input_numeric("county_n", "Number of Counties:", 5, min=1, max=3456),
            ui.input_radio_buttons(
                "year_rb", "Period:", {"All": "1992-2015", "ni": "1992-2000", "tw": "2000-2010", "now": "2010-2015"}
            ),
            ui.input_radio_buttons(
                "county_rb", "Print:", {"t": "Most Prone", "b": "Least Prone"}
            ),

            div(HTML("<h5> ----------------------------------------------------------------------------- </h5>")),
            div(HTML("<h4> Fire Cause Prediction, for: </h4>")),
            ui.input_numeric("pred_coor_lo", "Longtitude:", -115, min=-180, max=180),
            ui.input_numeric("pred_coor_la", "Latitude:", 38, min=-90, max=90),
            ui.input_numeric("fire_size", "Fire Size \n (acres within the final perimeter of the fire):", 1, min=0, max=600000),
            ui.input_date("date", "Date:", value="1992-01-01"),

        ),

        ui.panel_main(
            ui.navset_tab(
                ui.nav("Welcome",
                        div(HTML("<h2> Welcome to The_Firefighter, </h2>")),
                        "The WebApp for the Analysis of fires in USA.",
                        div(HTML("<p> Check the rest of the tabs for the respective analysis resutls. </p>")),
                        ui.output_image("image"),
                       ),
                ui.nav("Fire Occurrences in Time",  div(HTML("<h3> - </h3>")), ui.output_plot("fotp"), div(HTML("<h5> ----------------------------------------------------------------------------- </h5>")), div(HTML("<h3> Dickey-Fuller Test: </h3>")), div(HTML("<h5> H0: Existence of Unit Root </h5>")), div(HTML("<h5> H1: Time Series being weakly stationary </h5>")), ui.output_text("fot"), div(HTML("<h5> ----------------------------------------------------------------------------- </h5>")), div(HTML("<h5> ----------------------------------------------------------------------------- </h5>")),),
                ui.nav("Counties prone to fire", div(HTML("<h3> - </h3>")), div(HTML("<h3> - </h3>")), div(HTML("<h3> - </h3>")), div(HTML("<h3> - </h3>")), div(HTML("<h3> - </h3>")), ui.output_text("counties_tb"), div(HTML("<h3> - </h3>")), ui.download_button("down_b", "Download Counties"), ),
                ui.nav("Fire Cause Prediction", div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> - </h5>")), div(HTML("<h5> By Adaptive Boosting (AdaBoost) Classifier, </h5>")), div(HTML("<h5> - </h5>")),ui.output_text("pred") ),
                ui.nav("State Codes", div(HTML("<h3> State Codes for State in Inputs (Grey Panel): </h3>")),
                       div(HTML("<h5> - </h5>")), ui.output_text("state_codes")),
            )
        )
    )
)


print("UI Loaded...")