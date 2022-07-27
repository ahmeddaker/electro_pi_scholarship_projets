
def automate_eda(path):
    # importing libraries
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import sys
    import seaborn as sns
    import warnings
    warnings.filterwarnings('ignore')

    # loading data
    try:
        df = pd.read_csv(path)
        print("CSV file loaded successfully")
    except Exception:
        try:
            df = pd.read_excel(path)
            print("Excel file loaded successfully")
        except Exception:
            print("File not found")
            sys.exit()
    print('DataFrame : ')
    print('\n')
    display(df.head())
    print('\n')

    print('data info : ')
    display(df.info())
    print('\n')

    print('data describtion : ')
    display(df.describe())
    print('\n')

    total_missing = df.isnull().sum()
    total_missing = total_missing[total_missing > 0]
    total_missing.sort_values(inplace=True)
    print(total_missing)
    print('\n')

    # dropping id columns
    try:
        if 'id' in df.columns:
            df.drop('id', axis=1, inplace=True)
        elif 'ID' in df.columns:
            df.drop('ID', axis=1, inplace=True)
    except:
        print('ID column not found')

    # date column to datetime type
    try:
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date']).astype(str)
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).astype(str)
    except:
        print('Date column not found')

    # extract month from the date column
    try:
        if 'Date' in df.columns:
            df['month'] = df['Date'].dt.month
        elif 'date' in df.columns:
            df['month'] = df['date'].dt.month
    except:
        print('Date column not found')

    # spliting year into quarters by month and adding quarter column
    try:
        df['quarter'] = df['month'].apply(
            lambda x: 1 if x <= 3 else (2 if x <= 6 else (3 if x <= 9 else 4)))
    except:
        print('month column not found')

    # dropping name column
    try:
        if 'name' in df.columns:
            df.drop('name', axis=1, inplace=True)
        elif 'Name' in df.columns:
            df.drop('Name', axis=1, inplace=True)
    except:
        print('Name column not found')

    # dropping date column
    try:
        if 'Date' in df.columns:
            df.drop('Date', axis=1, inplace=True)
        elif 'date' in df.columns:
            df.drop('date', axis=1, inplace=True)
    except:
        print('Date column not found')
    
    # extracting numerical and categorical features
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns

    categorical_features = df.select_dtypes(
        include=['object', 'bool', 'category']).columns

    # fill missing values with mean in numerical features
    for feature in numeric_features:
        df[feature].fillna(df[feature].mean(), inplace=True)

    # fill missing values with mode in categorical features
    for feature in categorical_features:
        df[feature].fillna(df[feature].mode()[0], inplace=True)

    # check if there are any missing values
    total_missing = df.isnull().sum()
    print('total missing values : ')

    print('/n')

    # dataframe correlation
    corr = df.corr()
    sns.heatmap(corr, annot=True)

    # getting distribution of numeric features
    for col_name in numeric_features:
        col = df[col_name]
        rng = col.max() - col.min()
        var = col.var()
        std = col.std()
        print('\n{}:\n - Range: {:.2f}\n - Variance: {:.2f}\n - Std.Dev: {:.2f}'.format(col_name, rng, var, std))

    # getting distribution of numeric features with plots
    for col in numeric_features:
        fig = plt.figure(figsize=(9, 6))
        ax = fig.gca()
        feature = df[col]
        feature.hist(bins=100, ax=ax)
        ax.axvline(feature.mean(), color='magenta',
                   linestyle='dashed', linewidth=2, label='Mean')
        ax.axvline(feature.median(), color='cyan',
                   linestyle='dashed', linewidth=2, label='Median')
        ax.set_title(col)
        plt.legend()
        plt.show()

    # statistical analysis of categorical features
    for feature in categorical_features:
        print('\n')
        print('Statistical analysis of {}:'.format(feature))
        print(df[feature].value_counts())
        print('\n')
        print('Descriptive statistics of {}:'.format(feature))
        print(df[feature].describe())
        print('\n')
        print('Histogram of {}:'.format(feature))
        sns.countplot(x=feature, data=df)
        plt.xticks(rotation=90)
        plt.show()

    # bivariate data exploration
    for col_1 in categorical_features:
        for col_2 in numeric_features:
            plt.figure(figsize=(20,5))
            sns.catplot(x=col_1, y=col_2, data=df, kind='box')
            plt.xticks(rotation=90)
            plt.show();
