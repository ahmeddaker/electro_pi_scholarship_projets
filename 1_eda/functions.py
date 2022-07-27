#function to read csv or excel file
def read_file(file_name):
    try:
        if file_name.endswith('.csv'):
            return pd.read_csv(file_name)
        elif file_name.endswith('.xlsx'):
            return pd.read_excel(file_name)
        else:
            print('File format not supported')
            return None
    except:
        print('File not found')
        return None

def nun_missing_values(df):
    return df.isnull().sum().sum()
    total_missing = total_missing[total_missing > 0]
    total_missing.sort_values(inplace=True)
    return total_missing        

#returning the dataframe with the nun columns dropped
def drop_columns_40_percent_missing(df):
    nun_columns = df.isnull().sum()
    nun_columns = nun_columns[nun_columns > len(df) * 0.4]
    nun_columns.sort_values(inplace=True)
    df.drop(nun_columns.index, axis=1, inplace=True)
    print('\nDropped columns with more than 50% missing values: {}'.format(nun_columns.sum()))
    return df

def bool_to_datetime(df):
    try:
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        print('Date column not found')
        return None

#extract year from the date column
def extract_year(df):
    try:
        if 'Date' in df.columns:
            df['year'] = df['Date'].dt.year
        elif 'date' in df.columns:
            df['year'] = df['date'].dt.year
        return df['year']
    except:
        print('Date column not found')
        return None

#extract month from the date column
def extract_month(df):
    try:
        if 'Date' in df.columns:
            df['month'] = df['Date'].dt.month
        elif 'date' in df.columns:
            df['month'] = df['date'].dt.month
        return df['month']
    except:
        print('Date column not found')
        return None

#spliting year into quarters by month and adding quarter column
def split_month_into_quarters(df):
    try:
        df['quarter'] = df['month'].apply(lambda x: 1 if x <= 3 else (2 if x <= 6 else (3 if x <= 9 else 4)))
        return df['quarter']
    except:
        print('month column not found')
        return None

#function for extracting the numerical features
def numeric_features(df):
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
    return numeric_features

#function for extracting the categorical features
def categorical_features(df):
    categorical_features = df.select_dtypes(include=['object', 'bool', 'category']).columns
    return categorical_feature

#function for dropping id column
def drop_id(df):
    try:
        if 'id' in df.columns:
            df.drop('id', axis=1, inplace=True)
        elif 'ID' in df.columns:
            df.drop('ID', axis=1, inplace=True)
        return df
    except:
        print('ID column not found')
        return None

#function to get information about the data
def df_info(df):
    print('Dataframe info:')
    print(df.info())
    print('\n')
    print('Dataframe describe:')
    print(df.describe())

#automatic exploratory data analysis for each dataframe
def auto_explore(df):
    '''
    This function will automatically explore the dataframe
    '''
    # Create a figure for 2 subplots (2 rows, 1 column)
    fig, ax = plt.subplots(2, 1, figsize = (10,4))

    # Plot the histogram
    ax[0].hist(df)
    ax[0].set_ylabel('Frequency')

    # Add lines for the mean, median, and mode
    ax[0].axvline(x=df.mean(), color = 'cyan', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=df.median(), color = 'red', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=df.mode()[0], color = 'yellow', linestyle='dashed', linewidth = 2)

    # Plot the boxplot
    ax[1].boxplot(df, vert=False)
    ax[1].set_xlabel('Value')

    # Add a title to the Figure
    fig.suptitle('Distribution of ' + df.name)

    # Show the figure
    fig.show()

def show_density(var_data):
    fig = plt.figure(figsize=(10,4))

    # Plot density
    var_data.plot.density()

    # Add titles and labels
    plt.title(var_data.name + ' Data Density')

    # Show the mean, median, and mode
    plt.axvline(x=var_data.mean(), color = 'cyan', linestyle='dashed', linewidth = 2)
    plt.axvline(x=var_data.median(), color = 'red', linestyle='dashed', linewidth = 2)
    plt.axvline(x=var_data.mode()[0], color = 'yellow', linestyle='dashed', linewidth = 2)

    # Show the figure
    plt.show()

def show_distribution(var_data):
    '''
    This function will make a distribution (graph) and display it
    '''

    # Get statistics
    min_val = var_data.min()
    max_val = var_data.max()
    mean_val = var_data.mean()
    med_val = var_data.median()
    mod_val = var_data.mode()[0]

    print(var_data.name +'\n'+'Minimum:{:.2f}\nMean:{:.2f}\nMedian:{:.2f}\nMode:{:.2f}\nMaximum:{:.2f}\n'.format(min_val,
                                                                                            mean_val,
                                                                                            med_val,
                                                                                            mod_val,
                                                                                            max_val))

    # Create a figure for 2 subplots (2 rows, 1 column)
    fig, ax = plt.subplots(2, 1, figsize = (10,4))

    # Plot the histogram
    ax[0].hist(var_data)
    ax[0].set_ylabel('Frequency')

    # Add lines for the mean, median, and mode
    ax[0].axvline(x=min_val, color = 'gray', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=mean_val, color = 'cyan', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=med_val, color = 'red', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=mod_val, color = 'yellow', linestyle='dashed', linewidth = 2)
    ax[0].axvline(x=max_val, color = 'gray', linestyle='dashed', linewidth = 2)

    # Plot the boxplot
    ax[1].boxplot(var_data, vert=False)
    ax[1].set_xlabel('Value')

    # Add a title to the Figure
    fig.suptitle('Distribution of ' + var_data.name)

    # Show the figure
    fig.show()

#bivariate data exploration
def plot_bivariate (arr_1, arr_2, df, kind):
    '''
    This function will plot a bivariate graph and display it
    arr_1: first array
    arr_2: second array
    df: dataframe
    kind: kind of plot
    '''
    for col_1 in arr_1:
        for col_2 in arr_2:
            plt.figure(figsize=(20,5))
            sns.catplot(x=col_1, y=col_2, data=df, kind=kind)
            plt.xticks(rotation=90)
            plt.show();

