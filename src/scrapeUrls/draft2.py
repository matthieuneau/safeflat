import pandas as pd

df = pd.DataFrame(
    {"a": 1, "b": 2, "description": "This is a test description"}, index=[0]
)

desc = df.loc[0, "description"]

print(desc)
