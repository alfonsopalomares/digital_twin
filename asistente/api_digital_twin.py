# -*- coding: utf-8 -*-
"""

"""

import requests
import pandas as pd
# from flujo_4IPCD import ejecutar_flujo

def consumir_api(usuario: str, url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()

        # Convertir a DataFrame
        df = pd.DataFrame(datos)

        # Ejecutar flujo
        # resultado = ejecutar_flujo(usuario, df)
        # return resultado
        
        return df

    except Exception as e:
        return {"error": str(e)}
