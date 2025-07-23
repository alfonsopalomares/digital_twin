# -*- coding: utf-8 -*-
"""

"""


from langchain_core.tools import Tool
# from langchain_experimental.tools import PythonREPLTool, PythonAstREPLTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from chat_llm import create_llm

def create_asistente(dfs_dict):
    # Diccionario de entorno compartido
    # datos de entrada
    entorno = {nombre: df for nombre, df in dfs_dict.items()}
    # datos de salida
    entorno = entorno | {
        "df_resultado": pd.DataFrame(),
        "fig_plotly": go.Figure(),
        # "respuesta_usuario": "",
        "ahora": pd.Timestamp(datetime.now())
        }
    

    # python_tool = PythonREPLTool(globals=entorno)
    # python_tool = PythonAstREPLTool(globals=entorno)
    
    def ejecutar_codigo(codigo: str) -> str:
        """
        Ejecuta el codigo usando el entorno de variables.
        Similar a PythonREPLTool pero permitiendo tomar variables de salida.

        Parameters
        ----------
        codigo : str
            Codigo Python.

        Returns
        -------
        str
            Mensaje de ejecución correcta o Error generado.

        """
        try:
            lineas, caracteres = (len(codigo.split()), len(codigo))
            print(f"ejecutando codigo: {lineas} lineas, {caracteres} caracteres")
            exec(codigo, entorno)
            return "Código ejecutado correctamente."
        except Exception as e:
            print("fallo ejecucion")
            return f"Error: {e}"


    # Crear herramienta LangChain
    python_tool = Tool.from_function(
        name="ejecutar_python",
        func=ejecutar_codigo,
        description="Ejecuta código Python sobre DataFrames precargados"
    )


    # Crear descripción de columnas y tipos
    def describir_columnas() -> str:
        """
        Genera un mensaje descriptivo sobre los DataFrame y sus columnas para darle contexto al LLM.

        Returns
        -------
        str
            Mensaje descriptivo sobre los DataFrame y sus columnas.

        """
        contexto = ""
        for nombre, df in dfs_dict.items():
            columnas = [f"- '{col}': {df[col].dtype}" for col in df.columns]
            contexto += f"\n - '{nombre}' ({df.shape[0]} filas):\n" + "\n".join(columnas)
        
        return contexto.strip()


    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""
        Sos un agente de análisis técnico. 
        Evaluaras el funcionamiento de un dispensador de agua atraves de los datos que nos brinda su gemelo digital.

        Usa la variable 'ahora' (de tipo pd.Timestamp) como la fecha y hora actual en que se hace la consulta.
        Tenés acceso a los siguientes DataFrames:
        {describir_columnas()}

        Para cada consulta siempre debes:
        - Generá un DataFrame con el resultado final en 'df_resultado' (variable con ese exacto nombre).
        - Genera un grafico usando Plotly y guardalo en 'fig_plotly' sin mostrarlo (variable con ese exacto nombre).
        - Generá una explicación general y comentarios con formato markdown como respuesta para el usuario.
        No muestres nada automáticamente. No .show() ni nigún tipo de archivo que pudieras generar (no se mostraran).
        """),
        ("human", "{input}"),
        # ("placeholder", "{agent_scratchpad}")
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    # incorporar LLM especificado en chat_llm
    llm = create_llm()

    agente = create_tool_calling_agent(llm, [python_tool], prompt)
    ejecutor = AgentExecutor(agent=agente, tools=[python_tool], 
                             verbose=True, return_intermediate_steps=True)
    

    def procesar_consulta(texto_usuario):
        respuesta = ejecutor.invoke({"input": texto_usuario})
        # print(entorno)
        return (respuesta, entorno)

    return procesar_consulta
