import pandas as pd

file_name_input = "abc.csv"
file_name_output = "abc_without_dupes.csv"

df = pd.read_csv(file_name_input, encoding="ISO-8859-1", engine='python')

df.drop_duplicates(subset=None, inplace=True)

# Write the results to a different file
df.to_csv(file_name_output, index=False)