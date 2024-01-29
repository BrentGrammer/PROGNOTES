Convert Jupyter notebook to Python file:
You can convert the notebooks to .py files by using nbconvert or just by clicking Save As -> .py file.

TIP:

-Use shift-Tab Tab in jupyter notebook to get documentation on any method or class etc.

Common Data types:

-object (any python obj incl strings etc)
-Integer/Float
-Boolean
-Datetime (You need to tell python to convert dates to this type)

Missing types: NaN, None, NaT (Not a time type)
Note: No missing value object for Booleans or Ints - Pandas will convert the data type of the entire column if a value of this data type is missing.

## Accessing row (use .loc[]) vs. col

- Row: df.loc['rowname']
- Col: df['colname']
  - You don't need .loc for cols

## INDEX COLS AND VALUES:

-A Dataframe has 3 components accessible as attrs on the df object:
index
columns
values

indexes:

#Set the index column to be a specific column:
df = pd.read_csv('../path', index_col=1)

### set index on a dataframe (returns a new copy of the dataframe):

new_df = df.set_index('colNameLabel')

### Get a list of the index column indexes:

df.index

### List columns:

df.columns

### list values in the cells:

df.values

### select a column by index

df['colLabel']

Note: you can run index and values atributes on the selected column if you save it to a variable

### Access index label by index in the array:

idx = df.index

idx[0]

### returns label for first index label of the dataframe)

idx[[1,4,5]]

### returns labels for multiple positions

idx[5:10]

### returns sliced label list

### Find index of a value in a column:

col1 = df['colName']
fixed_costs_row_idx = df[col1 == 'Fixed Costs'].index[0]

Note: index returns an int64Index type which holds an array of index positions that are ints - you need to access this if using for slicing (i.e. df[my_idx:])

---

DROP EMPTY COLS AND ROWS:

# Drop empty rows:

fixed_df = fixed_df.dropna(how='all')

# Drop empty cols:

df2 = fixed_df.dropna(axis=1, how='all')

Note: returns a new dataframe - need to save to a variable

COMBINE COLS:

# if you have two cols with varying empty and nonnull values to combine them:

print df['feedback_id'].combine_first(df['_id'])

print df['feedback_id'].fillna(df['_id'])

RENAME COLS:

# single or selected cols:

df.rename(columns={'pop':'population'}, inplace=True)

# rename all cols:

df.columns = ['country','year','population',
'continent','life_exp','gdp_per_cap']

DROP COLS:

df = df.drop('column_name', 1)

# where 1 is the axis number (0 for rows and 1 for columns.)

# To delete the column without having to reassign df you can do:

df.drop('column_name', axis=1, inplace=True)

# Finally, to drop by column number instead of by column label, try this to delete, e.g. the 1st, 2nd and 4th columns:

df = df.drop(df.columns[[0, 1, 3]], axis=1)

DROP ROWS:

df.drop(df.index[range(0,5)], inplace=True)

ADD ROWS:

average_df = pd.DataFrame([OrderedDict( ( (expense_col_name, 'Avg/Month'), (amount_col_name, mean(lst)) ) )])  
grand_total_df = pd.DataFrame([OrderedDict( ( (expense_col_name, 'Total/Yr'), (amount_col_name, total) ) )])
df = df.append([average_df, grand_total_df], ignore_index=True)

---

FIND VALUE IN CELL:

SEARCH FOR ROW BY STRING PATTERN:
df[df[col_name].str.contains(searchString, case=False)]

---

FIND ROWS THAT MATCH ONE OF SEVERAL VALUES:

df.loc[df[col_name].isin([fixed_total, semi_total, var_total])]

ROWS MATCH A VALUE:

df.loc[df[col_name] == stringval]

---

# List types of data in columns in a series (column index name on left, data type on the right):

df.dtypes

# get number of rows and columns in a tuple:

df.shape

# return num of rows:

len(df)

# get info on df with number of non-null values:

df.info() # note: memory usage may be incorrect

# Get true memory usage with result:

df.info(memory_usage="deep")

# turn values into datetime types:

file = pd.read_csv('path/file.csv', parse_dates=['dateColName1', 'dateColName2'])

GET VALUE FROM A SERIES:

df[df[expense_col_name] == fixed_total]['Amount'].values[0]

## String Manipulation

- Use `df['col'].str.{method}`
- Concat: `df['Full Name'] = df['Name'].str.cat(df['Email'], sep=', ')`
- Replace: `df['Clean Phone'] = df['Phone'].str.replace('-', '')`
- Str Match/Filter: `filtered_df = df[df['Email'].str.contains('mark')]`
  - Main pattern is `df[df['col'].str.{method}]` to filter and get whole new dataframe
- count specific chars: `df['Name Vowel Count'] = df['Name'].str.count('[aeiou]')`

#### Conditional manipulation

- Conditional based on containing substring: `df.loc[df['Name'].str.contains('john', case=False), 'Name'] = 'John Smith'`
- filter starts with: `filtered_df = df[df[‘Name’].str.startswith(‘J’)]`
- Extract part of string: `df[‘First Initial’] = df[‘Name’].str.extract(r’^(\w)’, expand=False)`
  - If expand=True were used instead, the result would be a DataFrame with one column for each capturing group in the regular expression. In this case, since there is only one capturing group (the first letter), expand=True and expand=False would produce similar results. However, using expand=False is more concise in this context where only one piece of information is being extracted.

#### Cleaning String data

- Replace None or empty cells with a value: `df['Name'].fillna('Unknown', inplace=True)`
  - fillna finds all None/empty and replaces with 'Unknown' in this case for the name col
  - Note: the fillna method in Pandas, as used in your example, will not replace empty strings ("") in the 'Name' column. It specifically deals with NaN (Not a Number) values, which represent missing or undefined data.
- Replace emtpy strings: `df['Name'].replace("", "Unknown", inplace=True)`
- Remove trailing characters with rstrip() (whitespace is default if nothing passed in)
  - has unexpected behavior sometimes - how does it decide the word and where it ends?

```python
txt = "banana,,,,,ssqqqww....."

x = txt.rstrip(",.qsw") # removes chars as many times as they occur
```

## EXCEL:

- Use ExcelFile class for some built in functionality and methods when working with excel files with multiple spreadsheets

# sheet names of a excel workbook:

my_workbook = ExcelFile('myfile.xlsx)
my_workbook.sheet_names
#-> list of sheet names as strings
