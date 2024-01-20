import pandas as pd
import calendar

df1 = pd.read_csv('data.csv')

# Create a new column 'date_astro' by combining 'day' and 'month' columns
df1['date_astro'] = df1.apply(lambda row: f"{row['day']}-{calendar.month_abbr[row['month']]}", axis=1)

# Fill missing values in 'hour' and 'minute' columns with zeros
df1[['hour', 'minute']] = df1[['hour', 'minute']].fillna(0)
df1['time'] = pd.to_datetime(df1[['hour', 'minute']].astype(int).astype(str).agg(':'.join, axis=1), format='%H:%M', errors='coerce')
df1 = df1.dropna(subset=['time'])
df1['time'] = df1['time'].dt.strftime('%I:%M%p')

df1 = df1[df1['tides'] == 'h']

df1['HI1_TIME'] = df1.apply(lambda row: row['time'] if row['tides'] == 'h' else None, axis=1)
df1['HI1'] = df1.apply(lambda row: row['value'] if row['tides'] == 'h' else None, axis=1)
df1['HI1_TODAY'] = df1.apply(lambda row: 'TODAY' if not pd.isnull(row['HI1_TIME']) else None, axis=1)

# Assuming your DataFrame is named df
df1['HI2_TIME'] = df1[df1['tides'] == 'h'].groupby('date_astro')['HI1_TIME'].transform('last')
df1['HI2'] = df1[df1['tides'] == 'h'].groupby('date_astro')['HI1'].transform('last')
df1['HI2_TODAY'] = df1.apply(lambda row: 'TODAY' if not pd.isnull(row['HI1_TIME']) else None, axis=1)

df1 = df1.drop_duplicates(subset='date_astro', keep='first')
df1 = df1.sort_values(by='date_astro')

columns_to_drop = ['year',  'month', 'day', 'hour',  'minute',  'value', 'tides', 'time']

df1 = df1.drop(columns=columns_to_drop)
# Display the sorted DataFrame
print(df1)

df2 = pd.read_csv('data.csv')

# Create a new column 'date_astro' by combining 'day' and 'month' columns
df2['date_astro'] = df2.apply(lambda row: f"{row['day']}-{calendar.month_abbr[row['month']]}", axis=1)

# Fill missing values in 'hour' and 'minute' columns with zeros
df2[['hour', 'minute']] = df2[['hour', 'minute']].fillna(0)
df2['time'] = pd.to_datetime(df2[['hour', 'minute']].astype(int).astype(str).agg(':'.join, axis=1), format='%H:%M', errors='coerce')
df2 = df2.dropna(subset=['time'])
df2['time'] = df2['time'].dt.strftime('%I:%M%p')

df2 = df2[df2['tides'] == 'l']

df2['LO1_TIME'] = df2.apply(lambda row: row['time'] if row['tides'] == 'l' else None, axis=1)
df2['LO1'] = df2.apply(lambda row: row['value'] if row['tides'] == 'l' else None, axis=1)
df2['LO1_TODAY'] = df2.apply(lambda row: 'TODAY' if not pd.isnull(row['LO1_TIME']) else None, axis=1)

# Assuming your DataFrame is named df
df2['LO2_TIME'] = df2[df2['tides'] == 'l'].groupby('date_astro')['LO1_TIME'].transform('last')
df2['LO2'] = df2[df2['tides'] == 'l'].groupby('date_astro')['LO1'].transform('last')
df2['LO2_TODAY'] = df2.apply(lambda row: 'TODAY' if not pd.isnull(row['LO1_TIME']) else None, axis=1)

df2 = df2.drop_duplicates(subset='date_astro', keep='first')
df2 = df2.sort_values(by='date_astro')

df2 = df2.drop(columns=columns_to_drop)
# Display the sorted DataFrame
print(df2)

merged_df = pd.merge(df1, df2, on='date_astro', how='left')

column_order = ['date_astro', 'HI1_TIME', 'HI1', 'HI1_TODAY', 'LO1_TIME', 'LO1', 'LO1_TODAY', 'HI2_TIME', 'HI2', 'HI2_TODAY', 'LO2_TIME', 'LO2', 'LO2_TODAY']
merged_df = merged_df[column_order]

merged_df['date_astro'] = pd.to_datetime(merged_df['date_astro'], errors='coerce', format='%d-%b')
merged_df = merged_df.sort_values(by='date_astro')

print(merged_df)

merged_df.to_csv('merged_data.csv', index=False)
