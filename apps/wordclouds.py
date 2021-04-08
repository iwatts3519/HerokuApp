import dash_bootstrap_components as dbc
import dash_html_components as html
import base64

image1 = "assets/wordcloud1.png"
encoded_image1 = base64.b64encode(open(image1, 'rb').read())
image2 = "assets/wordcloud2.png"
encoded_image2 = base64.b64encode(open(image2, 'rb').read())
# -------------------------------------------------------------------------------------
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image1.decode()), top=True),
                        dbc.CardBody([
                            html.H3("Exhibitor Messages Wordcloud"),
                            html.P
                            ("A wordcloud showing the most common words from the Exhibitor Messages")
                        ])
                    ]), width={"size": 4, "offset": 1}
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image2.decode()), top=True),
                        dbc.CardBody([
                            html.H3("Meeting Messages Wordcloud"),
                            html.P
                            ("A wordcloud showing the most common words from the Meeting Messages")
                        ])
                    ]), width={"size": 4, "offset": 2}
                )
            ])

    ]
)

# Not sure why the above code works but I got the answer from here after trying all sorts of different ways to get
# the images to display https://stackoverflow.com/questions/59811030/dash-plotly-image-doesnt-render-in-browser-but
# -displays-in-jupyter-note-book-py
