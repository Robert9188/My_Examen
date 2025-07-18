import pandas as pd
import numpy as np

def cap_outliers_iqr(df, column):
    """Caps outliers in a DataFrame column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])

    return df

def traiter_donnees_villas_(data):
    import pandas as pd
    import numpy as np

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    df = data[["Nombre_de_pieces", "Nombre_salles_bain", "Superficie", "Adresse"]].copy()
    df.drop_duplicates(inplace=True)

    # Nettoyage et conversion des données
    df['Superficie'] = pd.to_numeric(df['Superficie'].astype(str).str.replace(' m2', '').str.strip(), errors='coerce')
    df['Nombre_de_pieces'] = pd.to_numeric(df['Nombre_de_pieces'], errors='coerce')
    df['Nombre_salles_bain'] = pd.to_numeric(df['Nombre_salles_bain'], errors='coerce')

    df = df.rename(columns={
        "Nombre_de_pieces": "Pieces",
        "Nombre_salles_bain": "Salles_bain"
    })

    for col in ["Pieces", "Salles_bain", "Superficie"]:
        df = cap_outliers_iqr(df, col)
        df[col].fillna(df[col].median(), inplace=True)
        df[col] = df[col].astype(int)

    if df["Adresse"].isnull().sum() > 0:
        df["Adresse"].fillna(df["Adresse"].mode()[0], inplace=True)

    return df.reset_index(drop=True)



def traiter_donnees_terrains_(data):
    import pandas as pd
    import numpy as np

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    df = data[["Superficie", "Prix", "Adresse", "Lien_image-href"]].copy()
    df.drop_duplicates(inplace=True)

    # Nettoyage : suppression " m2", " CFA", etc.
    df['Superficie'] = pd.to_numeric(df['Superficie'].astype(str).str.replace(' m2', '').str.strip(), errors='coerce')
    df['Prix'] = pd.to_numeric(df['Prix'].astype(str).str.replace(' CFA', '').str.replace(' ', ''), errors='coerce')


    for col in ["Superficie", "Prix"]:
        df = cap_outliers_iqr(df, col)
        df[col].fillna(df[col].median(), inplace=True)
        df[col] = df[col].astype(int)

     # Renommer les colonnes
    df.rename(columns={
        'Lien_image-href': 'Lien_image	',
    }, inplace=True)

    if df["Adresse"].isnull().sum() > 0:
        df["Adresse"].fillna(df["Adresse"].mode()[0], inplace=True)

    return df.reset_index(drop=True)


def traiter_donnees_appartements_(data):
    # S'assurer que c’est bien un DataFrame
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Sélection des colonnes
    df = data[["Nombre_pieces", "Nombre_salles_bain", "Superficie", "Adresse"]].copy()

    # Supprimer les doublons
    df.drop_duplicates(inplace=True)

    # Nettoyage des champs texte et conversion en nombres
    df['Superficie'] = pd.to_numeric(df['Superficie'].astype(str).str.replace(' m2', '').str.strip(), errors='coerce')
    df['Nombre_pieces'] = pd.to_numeric(df['Nombre_pieces'], errors='coerce')
    df['Nombre_salles_bain'] = pd.to_numeric(df['Nombre_salles_bain'], errors='coerce')

    # Renommer
    df = df.rename(columns={
        "Nombre_pieces": "Pieces",
        "Nombre_salles_bain": "Salles_bain"
    })

    # Supprimer les outliers
    for col in ['Pieces', 'Salles_bain', 'Superficie']:
        df = cap_outliers_iqr(df, col)

    # Remplir les valeurs manquantes avec la médiane (arrondi à l'entier)
    for col in ['Pieces', 'Salles_bain', 'Superficie']:
        mediane = int(df[col].median())
        df[col].fillna(mediane, inplace=True)
        df[col] = df[col].astype(int)

    # Remplir les adresses manquantes
    if df["Adresse"].isnull().sum() > 0:
        df["Adresse"].fillna(df["Adresse"].mode()[0], inplace=True)

    return df.reset_index(drop=True)