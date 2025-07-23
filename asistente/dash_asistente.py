# -*- coding: utf-8 -*-
"""

"""

import dash
from dash import html, dcc, dash_table as dcct
from typing import Dict
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.io as pio


from chat_asistente import create_asistente
from data import DataGetter

TIME_MONITOREO = 5*60 #cada 5 minutos
TIME_ONLINE = 15 #cada 15 segundos

def procesar_test(input_str: str = None):
    # Supongamos que ya tenés estos objetos generados:
    consulta = input_str if input_str is not None else "Mostrar el promedio de lecturas por sensor"
    respuesta = "El promedio de lecturas se muestra por sensor en el gráfico adjunto."
    
    # fig_plotly_json = fig_plotly.to_json()
    with open("data/fig_plotly.json") as f:
        # fig_plotly_json = json.load(f)
        fig_plotly_json = f.read()
    
    
    df_resultado = pd.read_csv("data/df_resultado.csv")
    
    return df_resultado, fig_plotly_json, respuesta

def procesar_consulta(consulta: str):
    try:
        # from agente_df import construir_agente
    
        # dfs_dict = obtener_datos_gemelo()
        dfs_dict = data_getter.obtener_datos()
        
        # consulta = "Mostrá el promedio de lecturas por metrica en una figura Plotly"
        print(f"Consulta: {consulta}")
        procesar = create_asistente(dfs_dict)
        
        # respuesta, el_entorno, df_resultado, fig_plotly, respuesta_usuario = procesar(consulta)
        
        respuesta, el_entorno = procesar(consulta)
        df_resultado = el_entorno["df_resultado"]
        fig_plotly = el_entorno["fig_plotly"]
        # respuesta_usuario = el_entorno["respuesta_usuario"]
        
        # print(f"Respuesta: {respuesta_usuario}")
        
        print(f"RESPUESTA AGENTE: {respuesta}")
        
        fig_plotly_json = fig_plotly.to_json()
        
        # if not respuesta_usuario or respuesta_usuario == "":
        #     respuesta_usuario = respuesta["output"]
        respuesta_usuario = respuesta["output"]
        
        return df_resultado, fig_plotly_json, respuesta_usuario
    except Exception as e:
        print("procesar")
        print(e)
        raise e



# Historial de mensajes acumulado
historial_mensajes = []

data_getter = DataGetter(TIME_MONITOREO)



# App Dash
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
    "estilos.css"
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Panel de gemelo Digital
panel_gemelo = dbc.Card([
    dbc.CardHeader([
        dbc.Row([
            dbc.Col(html.Img(src="/assets/logo.png", height="30px"), width="auto"),
            dbc.Col(html.H3("Gemelo Digital"), width="auto"),
            dbc.Col(
                dbc.ButtonGroup([
                    dbc.Button("Analisis", id="btn-analytics", color="outline-info"),
                    dbc.Button("Anomalias", id="btn-anomalies", color="outline-info"),
                    dbc.Button("Metricas", id="btn-metrics", color="outline-info")
                ]),
                width="auto"
            ),
            dbc.Col([], id="estado-api", width="auto", className="ms-auto")
        ], align="center"),
    ]),
    dbc.CardBody([
        html.Iframe(
            id="iframe-gemelo",
            src="http://localhost:3000/metrics",
            # style={"width": "100%", "height": "100%", "border": "none"}
        )
    ])
], id="card-gemelo", className="cardpanel")

gemelo_online = [
       html.I(className="bi bi-check-circle-fill text-success me-2"),
       "api online"
    ]

gemelo_offline = dbc.Alert([
    html.I(className="bi bi-x-circle-fill text-danger me-2"),
    "API Gemelo No Disponible"
    ],color="danger", style={"padding":"5px","margin":"0px"})

# Panel de conversación
panel_chat = dbc.Card([
    dbc.CardHeader(html.H4([html.I(className="bi bi-chat-dots"), " Conversación"])),
    dbc.CardBody(
        id="chat-historial",
        children=[],
        # style={"overflowY": "auto", "padding": "0.5rem"}
    ),
    dbc.CardFooter([
        dbc.Row([
            dbc.Col(
                dcc.Textarea(
                    id="input-consulta",
                    placeholder="Escribí tu consulta...",
                    # style={"width": "100%", "height": "100px"},
                    className="form-control",
                    # debounce=True,
                    # n_submit=0
                ),
                width=9
            ),
            dbc.Col(
                dbc.Button(
                    ["Enviar ", html.I(className="bi bi-send me-2")],
                    id="btn-enviar",
                    color="primary",
                    className="w-100"
                ),
                width=3
            )
        ])
    ])
], id="card-chat", className="cardpanel")

# Panel gráfico
panel_plot = dbc.Card([
    dbc.CardHeader([html.I(className="bi bi-bar-chart"), " Visualización"]),
    dbc.CardBody([
        dcc.Graph(id="grafico-plotly")
    ])
], className="cardpanel")

# Panel tabla
panel_table = dbc.Card([
    dbc.CardHeader([html.I(className="bi bi-table"), " Datos Procesados"]),
    dbc.CardBody([
        dcct.DataTable(
            id="tabla-datos",
            columns=[],
            data=[],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
            page_size=10
        )
    ])
], className="cardpanel")

# Aplicación
app.title="Asistente Conversacional"
app.layout = dbc.Container([
    # navbar,
    
    dbc.Row([
        dbc.Col([
            panel_gemelo
        ], width=8),
        dbc.Col([
            panel_chat
        ], width=4),
    ]),
    # html.Hr(),
    dbc.Row([
        dbc.Col([
            panel_table
        ], width=6),
        dbc.Col([
            panel_plot
        ], width=6)
    ]),
    dcc.Interval(id="intervalo-online", interval=TIME_ONLINE*1000, n_intervals=0),
    dcc.Interval(id="intervalo-data", interval=TIME_MONITOREO*1000, n_intervals=0)
], fluid=True)



# Callback para enviar consulta
@app.callback(
    Output("grafico-plotly", "figure"),
    Output("tabla-datos", "data"),
    Output("tabla-datos", "columns"),
    Output("chat-historial", "children"),
    Input("btn-enviar", "n_clicks"),
    # Input("input-consulta", "n_submit"),
    State("input-consulta", "value")
)
# def actualizar_panel(n_clicks, n_submit, consulta):
def actualizar_panel(n_clicks, consulta):
    if not consulta:
        raise dash.exceptions.PreventUpdate

    # Llamar al agente
    # df_resultado, fig_json, respuesta_usuario = procesar_test(consulta)
    print("pre-llm")
    df_resultado, fig_json, respuesta_usuario = procesar_consulta(consulta)
    print("pos-llm")

    # Actualizar historial
    historial_mensajes.append(html.P([
        html.B("Usuario: "),
        dcc.Markdown(consulta)
        ], className="text-muted"))
    
    historial_mensajes.append(html.P([
        html.B("Asistente: "),
        dcc.Markdown(respuesta_usuario)
        ], className="text-primary"))

    # Preparar tabla
    data = df_resultado.to_dict("records") if df_resultado is not None else []
    columns = [{"name": col, "id": col} for col in df_resultado.columns] if df_resultado is not None else []

    # Preparar figura
    fig = pio.from_json(fig_json)

    return fig, data, columns, historial_mensajes


# Callback iframe
@app.callback(
    Output("iframe-gemelo", "src"),
    Input("btn-analytics", "n_clicks"),
    Input("btn-anomalies", "n_clicks"),
    Input("btn-metrics", "n_clicks"),
    prevent_initial_call=True
)
def actualizar_iframe(n1, n2, n3):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    boton = ctx.triggered[0]["prop_id"].split(".")[0]
    match boton:
        case "btn-analytics":
            return "http://localhost:3000/analytics#title"
        case "btn-anomalies":
            return "http://localhost:3000/anomalies#title"
        case "btn-metrics":
            return "http://localhost:3000/metrics#title"
        case _:
            return dash.no_update

@app.callback(
    Output("estado-api", "children"),
    Input("intervalo-online", "n_intervals")
)
def actualizar_online(n):
    estado = data_getter.cliente_online()
    return gemelo_online if estado else gemelo_offline
    

@app.callback(
    Input("intervalo-data", "n_intervals")
)
def actualizar_data(n):
    data_getter.actualizar()
    

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run(debug=True, port=3100)
