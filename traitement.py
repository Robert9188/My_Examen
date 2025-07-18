import pandas as pd
from statistics import median, mode

def traiter_donnees_villas(data):
    # Étape 1 : Conversion en DataFrame
    df = pd.DataFrame(data)

    # Étape 2 : Suppression des doublons
    df = df.drop_duplicates()

    # Étape 3 : Traitement des valeurs manquantes
    # Prix manquants → moyenne
    if df["Prix"].isnull().sum() > 0:
        moyenne_prix = int(df["Prix"].mean())
        df["Prix"] = df["Prix"].fillna(moyenne_prix)

    # Pièces manquantes → mode
    if df["Pièces"].isnull().sum() > 0:
        try:
            mode_pieces = mode(df["Pièces"].dropna())
        except:
            mode_pieces = 3  # Valeur par défaut si aucun mode fiable
        df["Pièces"] = df["Pièces"].fillna(mode_pieces)

    # Étape 4 : Suppression des valeurs extrêmes (outliers)
    q1 = df["Prix"].quantile(0.25)
    q3 = df["Prix"].quantile(0.75)
    iqr = q3 - q1
    borne_inf = q1 - 1.5 * iqr
    borne_sup = q3 + 1.5 * iqr
    df = df[(df["Prix"] >= borne_inf) & (df["Prix"] <= borne_sup)]

    # Réinitialiser les index
    return df.reset_index(drop=True)




def traiter_donnees_terrains(data):
    df = pd.DataFrame(data)

    # 1. Suppression des doublons
    df = df.drop_duplicates()

    # 2. Traitement des valeurs manquantes
    superficie_median = df["Superficie"].median()
    prix_mean = df["Prix"].mean()

    df["Superficie"] = df["Superficie"].fillna(superficie_median)
    df["Prix"] = df["Prix"].fillna(prix_mean)

    # 3. Suppression des valeurs extrêmes avec méthode IQR
    def remove_outliers_iqr(df, column):
        while True:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            initial_len = len(df)
            df = df[(df[column] >= lower) & (df[column] <= upper)]
            if len(df) == initial_len:
                break
        return df

    df = remove_outliers_iqr(df, "Superficie")
    df = remove_outliers_iqr(df, "Prix")

    return df.reset_index(drop=True)


def traiter_donnees_appartements(data):
    df = pd.DataFrame(data)

    # 1. Suppression des doublons
    df = df.drop_duplicates()

    # 2. Traitement des valeurs manquantes
    if df["Prix"].isnull().sum() > 0:
        moyenne_prix = int(df["Prix"].mean())
        df["Prix"] = df["Prix"].fillna(moyenne_prix)

    if df["Pièces"].isnull().sum() > 0:
        try:
            mode_pieces = mode(df["Pièces"].dropna())
        except:
            mode_pieces = 3
        df["Pièces"] = df["Pièces"].fillna(mode_pieces)

    # 3. Suppression des valeurs extrêmes (outliers) sur le prix
    q1 = df["Prix"].quantile(0.25)
    q3 = df["Prix"].quantile(0.75)
    iqr = q3 - q1
    borne_inf = q1 - 1.5 * iqr
    borne_sup = q3 + 1.5 * iqr
    df = df[(df["Prix"] >= borne_inf) & (df["Prix"] <= borne_sup)]

    return df.reset_index(drop=True)