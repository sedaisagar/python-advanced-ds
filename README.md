### Visualization Examples

Here are quick examples using pandas with matplotlib (and optional seaborn) to create common plots.

- [Bar Graph](#bar-graph)
- [Pie Chart](#pie-chart)
- [Scatter Plot](#scatter-plot)
- [Box Plot](#box-plot)
- [Line Graph](#line-graph)

```python
# Common imports & sample data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # optional

df = pd.DataFrame({
    'category': ['A', 'B', 'C'],
    'value': [10, 20, 15],
    'x': [1, 2, 3],
    'y': [5, 7, 4]
})
```

#### Bar Graph
```python
# Bar Graph
df.plot(kind='bar', x='category', y='value', title='Bar Graph Example')
plt.tight_layout()
plt.show()
```

#### Pie Chart
```python
# Pie Chart
df.set_index('category')['value'].plot(kind='pie', autopct='%1.1f%%', title='Pie Chart Example')
plt.ylabel('')
plt.show()
```

#### Scatter Plot
```python
# Scatter Plot
df.plot(kind='scatter', x='x', y='y', title='Scatter Plot Example')
plt.show()
```

#### Box Plot
```python
# Box Plot
df[['value']].plot(kind='box', title='Box Plot Example')
plt.show()
```

#### Line Graph
```python
# Line Graph
df.plot(kind='line', x='x', y='value', marker='o', title='Line Graph Example')
plt.show()
```

# 🐼 Pandas Essentials — Quick Guide

A concise cheat-sheet covering the most commonly used Pandas operations for data loading, cleaning, transformation, and analysis.

---

## 📦 Installation
```bash
pip install pandas

```
🚀 Getting Started
---
```python
import pandas as pd
import matplotlib.pyplot as plt  # for plotting
```

📥 Loading Data
--- 

```bash
df = pd.read_csv("file.csv")
df = pd.read_excel("file.xlsx")
df = pd.read_json("file.json")
```


### 🔍 Inspecting Data
```python
# Quick inspection helpers
df.head()       # first 5 rows
df.tail()       # last 5 rows
df.info()       # column types + nulls
df.describe()   # stats summary
df.shape        # (rows, columns)
df.columns      # list of column names
```

### 🎯 Selecting Data
```python
# Selecting columns
df['col']
df[['col1', 'col2']]
```

#### Rows (selecting/filtering)
```python
# Selecting rows
df.loc[5]                         # by label
df.iloc[5]                        # by index position
df[df['age'] > 25]                # filter
df[(df['age'] > 25) & (df['city'] == 'Kathmandu')]
```

### ✏️ Adding & Modifying Columns
```python
df['new_col'] = df['a'] + df['b']
df['email'] = ""                  # blank column
df['amount'] = df['amount'].astype(float)
```

### 🧹 Dropping & Cleaning
```python
df.drop(columns=['remarks'], inplace=True)
df.dropna(inplace=True)
df['amount'].fillna(0, inplace=True)
```

### 📊 Sorting
```python
df.sort_values('amount')
df.sort_values(['age', 'amount'], ascending=[True, False])
```

### 📦 Group By & Aggregations
```python
df.groupby('city')['amount'].sum()

df.groupby('city').agg({
    'amount': 'sum',
    'age': 'mean'
})
```

### 🔗 Merging DataFrames
```python
pd.merge(df1, df2, on='id')
pd.merge(df1, df2, on='id', how='left')
```

### 📤 Exporting Data
```python
df.to_csv("out.csv", index=False)
df.to_excel("out.xlsx", index=False)
```

### ⭐ Useful Tricks
```python
df['contact'] = df['contact'].astype('int64')   # convert type
df.rename(columns={"BOID NO": "boid_no"}, inplace=True)
df['remarks'].replace("N/A", "", inplace=True)
df['clean_name'] = df['name'].apply(lambda x: x.strip().title())
```

### 🗂 Topical Guide — Practical Topics & Mini Examples

A focused list of practical topics to progress from data loading to delivering models, each with a quick example or pointer.

#### Data Loading & Validation
```python
# Robust read with dtype and parse_dates
df = pd.read_csv('data.csv', dtype={'id': 'int64'}, parse_dates=['date'])
assert df['id'].notna().all()
```

#### Data Cleaning & Imputation
```python
# Replace values, drop duplicates, fill NaNs
df['amount'] = df['amount'].replace('N/A', np.nan).astype(float)
df.drop_duplicates(inplace=True)
df['amount'].fillna(df['amount'].median(), inplace=True)
```

#### Exploratory Data Analysis (EDA)
```python
# Quick EDA: summaries + visuals
print(df.describe(include='all'))
pd.plotting.scatter_matrix(df.select_dtypes(include='number'), figsize=(8,8))
plt.show()
```

#### Feature Engineering
```python
# Extract datetime features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
# create interaction
df['price_x_qty'] = df['price'] * df['quantity']
```

#### Handling Categorical Data
```python
# Label encoding and one-hot
df['cat_code'] = df['category'].astype('category').cat.codes
df = pd.get_dummies(df, columns=['category'], dummy_na=False)
```

#### Scaling & Normalization
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[['x','y']] = scaler.fit_transform(df[['x','y']])
```

#### Time Series Basics
```python
# Set index, resample, and rolling mean
ts = df.set_index('date').sort_index()
monthly = ts['value'].resample('M').sum()
ts['value'].rolling(7).mean()
```

#### Text Data Basics
```python
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer(stop_words='english', max_features=1000)
X_text = vec.fit_transform(df['text'])
```

#### Feature Selection & Dimensionality Reduction
```python
from sklearn.feature_selection import SelectKBest, f_classif
sel = SelectKBest(f_classif, k=10)
X_new = sel.fit_transform(X, y)
```

#### Building Models & Evaluation
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
clf = RandomForestClassifier(n_estimators=100, random_state=0)
print(cross_val_score(clf, X_train, y_train, cv=5).mean())
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
```

#### Cross-Validation & Pipelines
```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
pipe = Pipeline([
    ('impute', SimpleImputer(strategy='median')),
    ('model', RandomForestClassifier())
])
print(cross_val_score(pipe, X, y, cv=5).mean())
```

#### Model Serialization & Serving
```python
import joblib
joblib.dump(clf, 'model.joblib')
clf2 = joblib.load('model.joblib')
```

#### Performance & Vectorization Tips
```python
# Use vectorized ops instead of loops
df['total'] = df['price'] * df['qty']  # fast: uses numpy under the hood
```

#### Working with Large Datasets
```python
# chunked reading
for chunk in pd.read_csv('big.csv', chunksize=100_000):
    # process chunk
    print(chunk.shape)
```

#### Visualization Best Practices
```python
import seaborn as sns
sns.histplot(df['amount'], kde=True, bins=30)
plt.title('Distribution of Amount')
plt.xlabel('Amount')
plt.show()
```

#### Reproducibility & Environment
```text
# Save environment
pip freeze > requirements.txt
# With conda: conda env export > environment.yml
```

#### Testing & CI
```python
# Example pytest snippet
def test_positive_amounts():
    assert (df['amount'] >= 0).all()
```
