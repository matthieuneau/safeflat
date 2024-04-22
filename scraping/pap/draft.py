import pandas as pd

# Example DataFrame
data = {
    "details": [
        ["4 pièces", "3 chambres", "82 m²", "Terrain 200 m²"],
        ["3 pièces", "1 chambre", "55 m²"],
        ["5 pièces", "3 chambres", "115 m²"],
        ["4 pièces", "3 chambres", "82 m²", "Terrain 200 m²"],
        ["3 pièces", "1 chambre", "55 m²"],
    ]
}

df = pd.DataFrame(data)

# Create a new column 'pieces' by extracting the number of pièces
df["pieces"] = df["details"].apply(
    lambda x: next((int(s.split()[0]) for s in x if "pièce" in s), None)
)

print(df)
