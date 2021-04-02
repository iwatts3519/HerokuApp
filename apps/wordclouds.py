import dash_bootstrap_components as dbc
import dash_html_components as html
import base64

image = "assets/wordcloud2.png"
encoded_image = base64.b64encode(open(image, 'rb').read())
# -------------------------------------------------------------------------------------
layout = html.Div(
    [
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
    ]
)

# Not sure why the above code works but I got the answer from here after trying all sorts of different ways to get
# the images to display https://stackoverflow.com/questions/59811030/dash-plotly-image-doesnt-render-in-browser-but
# -displays-in-jupyter-note-book-py
