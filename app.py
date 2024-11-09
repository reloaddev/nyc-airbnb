from dash import Dash, html

app = Dash()

app.layout = [html.Div(children='International Students in Europe')]

if __name__ == '__main__':
    app.run(debug=True)