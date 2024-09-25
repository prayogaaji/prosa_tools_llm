import pandas as pd

# Given text
text = """
## fakta
## kebijakan dan pemerintahan
## artikel ini membahas tentang pertemuan menteri pembangunan g20 di belitung, yang membahas tentang pemulihan ekonomi dan ketahanan negara berkembang. artikel ini menitikberatkan pada peran pemerintah dalam mendorong pemulihan ekonomi, khususnya di negara berkembang.
## artikel ini membahas tentang pertemuan menteri pembangunan g20 di belitung. menteri ppn/kepala bappenas suharso monoarfa menekankan pentingnya pemulihan dan ketahanan bagi negara-negara berkembang di tengah krisis global.
## artikel ini membahas tentang pertemuan menteri pembangunan g20 di belitung, indonesia.
## peran pemerintah lokal
## perjanjian internasional
"""

# Split the text by lines and remove empty ones
lines = [line.strip() for line in text.split("\n") if line.strip()]

# Remove '## ' from each line
lines_cleaned = [line.replace("## ", "") for line in lines]
print(lines_cleaned)
# Create the DataFrame with cleaned lines
df_result_cleaned = pd.DataFrame([lines_cleaned], columns=[f'kolom_{i+1}' for i in range(len(lines_cleaned))])

# Show the result
print(df_result_cleaned)
