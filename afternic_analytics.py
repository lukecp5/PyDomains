import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --------------------------------------------------------------
# Step 1: Load CSV
# --------------------------------------------------------------

def load_data(csv_file_path: str) -> pd.DataFrame:
    """
    Loads the Afternic CSV file into a pandas DataFrame.
        
    :param csv_file_path: The full path to the CSV file
    
    :return: pd.DataFrame(which is the loaded CSV file in a usable format) 
        if successful, None otherwise
    """
    df = pd.read_csv(csv_file_path, low_memory=False)
    return df

# --------------------------------------------------------------
# Step 2: Clean & Pre-process
# --------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame by:
      - Dropping rows with missing essential columns
      - Converting date columns to datetime
      - Converting numeric columns to correct dtypes
    """
    # Replace or drop missing data if needed
    # Example: If 'price' or 'startPrice' or 'registeredDate' is critical, drop rows missing them
    df = df.dropna(subset=['price', 'startPrice', 'registeredDate'])
    
    # Convert date columns to datetime
    date_cols = ['startDate', 'endDate', 'registeredDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Convert numeric columns
    numeric_cols = [
        'price', 'startPrice', 'renewPrice', 'bidCount',
        'ahrefsDomainRating', 'alexaRanking', 'umbrellaRanking',
        'backlinksCount', 'cloudflareRanking', 'estibotValue',
        'extensionsTaken', 'keywordSearchCount', 'lastSoldPrice'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows that are still missing required numeric columns after conversion
    df = df.dropna(subset=['price', 'bidCount'])
    
    return df

# --------------------------------------------------------------
# Step 3: Feature Engineering
# --------------------------------------------------------------
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds useful columns for analysis, e.g. domain length, domain age, etc.
    """
    # Domain length
    if 'url' in df.columns:
        df['domainLength'] = df['url'].apply(lambda x: len(x) if isinstance(x, str) else np.nan)
    
    # Domain age in years
    # (For domains with registeredDate)
    if 'registeredDate' in df.columns:
        current_year = datetime.now().year
        df['domainAge'] = df['registeredDate'].apply(lambda x: current_year - x.year if pd.notnull(x) else np.nan)
    
    # Price difference from start price
    if 'price' in df.columns and 'startPrice' in df.columns:
        df['priceDiff'] = df['price'] - df['startPrice']
    
    # Time left or time in auction
    if 'startDate' in df.columns and 'endDate' in df.columns:
        df['auctionDurationDays'] = (df['endDate'] - df['startDate']).dt.days
    
    return df

# --------------------------------------------------------------
# Step 4: Exploratory Analysis
# --------------------------------------------------------------
def basic_summary(df: pd.DataFrame):
    """
    Prints out descriptive statistics and correlation matrix.
    Also provides some insights into the distribution of key fields.
    """
    print("===== BASIC INFO =====")
    print(df.info())
    
    print("\n===== DESCRIPTIVE STATISTICS =====")
    print(df.describe())
    
    # Correlation matrix
    numeric_cols = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_cols.corr()
    print("\n===== CORRELATION MATRIX =====")
    print(corr_matrix)
    
    # Optional: Plot correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.show()
    
    # Example: distribution of final price
    if 'price' in df.columns:
        plt.figure()
        sns.histplot(data=df, x='price', bins=50, log_scale=(False, True))  # log scale y-axis
        plt.title('Distribution of Price')
        plt.show()

# --------------------------------------------------------------
# Step 5: Key Insights/Heuristics
# --------------------------------------------------------------
def suggest_domains(df: pd.DataFrame, price_threshold=500, rating_threshold=10) -> pd.DataFrame:
    """
    Example heuristic-based filter:
      - Price < price_threshold (cheap entry)
      - AHREFS domain rating > rating_threshold
    Returns a subset of df that meets the criteria.
    """
    # Make sure the columns exist
    for col in ['price', 'ahrefsDomainRating']:
        if col not in df.columns:
            print(f"Column {col} not found in DataFrame.")
            return pd.DataFrame()
    
    # Filter
    filtered_df = df[
        (df['price'] < price_threshold) & 
        (df['ahrefsDomainRating'] > rating_threshold)
    ].copy()
    
    # Sort by rating descending (just as an example)
    filtered_df.sort_values(by='ahrefsDomainRating', ascending=False, inplace=True)
    
    return filtered_df

# --------------------------------------------------------------
# Main Execution
# --------------------------------------------------------------
def main():
    # Update this path to point to your CSV file
    csv_file_path = "afternic_auctions.csv"
    
    # 1. Load data
    df = load_data(csv_file_path)
    
    # 2. Clean data
    df = clean_data(df)
    
    # 3. Feature Engineering
    df = feature_engineering(df)
    
    # 4. Exploratory Analysis
    basic_summary(df)
    
    # 5. Suggest some domains based on a simple heuristic
    suggested = suggest_domains(df, price_threshold=500, rating_threshold=20)
    print("\n===== SUGGESTED DOMAINS (Heuristic Example) =====")
    print(suggested[['url', 'price', 'ahrefsDomainRating', 'domainLength', 'domainAge']].head(20))

if __name__ == "__main__":
    main()
