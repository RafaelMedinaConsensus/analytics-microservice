import pandas as pd
from typing import List, Dict, Any, Union

def get_top_n_records(
    data: List[Dict[str, Any]], 
    column: str, 
    n: int = 5, 
    ascending: bool = False
) -> List[Dict[str, Any]]:
    df = pd.DataFrame(data)
    if df.empty or column not in df.columns: return []
    
    # Asegurar ordenamiento numérico correcto
    try:
        df[column] = pd.to_numeric(df[column])
    except:
        pass # Si falla, ordena alfabéticamente

    df_sorted = df.sort_values(by=column, ascending=ascending)
    return df_sorted.head(n).to_dict(orient="records")