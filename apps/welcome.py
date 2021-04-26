import dash_bootstrap_components as dbc
import dash_html_components as html

# -------------------------------------------------------------------------------------
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.P(
                    "Following the recent pandemic many companies have been forced to reform their business models in "
                    "order to cater to a now remote form of work.  While this allows companies to record a good "
                    "amount of data about events, speakers and attendees,  in this situation it is more difficult to "
                    "gauge which forms of data are significant and what this data suggests. ")
            )

        ]),
    dbc.Row(
        [
            dbc.Col(
                html.P(
                    "This app prototype provides a method of obtaining information on attendees and sponsors of "
                    "virtual conference and exhibition models and separating the information to help form "
                    "conclusions. This specifically looks at the data regarding seminar and exhibition attendance, "
                    "discussions and provides word clouds of the most discussed topics within messages among "
                    "attendees.")

            )

        ]),
    dbc.Row(
        [
            dbc.Col(
                html.P(
                    "The aim of this app is to provide an easier method of drawing conclusions from the data which in "
                    "turn will allow the company to discern which parts of the conferences are most successful in "
                    "attracting and retaining attendees and sponsors.")

            )

        ])

])
