import pandas as pd
import json
import argparse
import os

def process_transactions(
        df: pd.DataFrame, 
        config: dict, 
        user:str
    ):
    # Get config settings
    user_config = config["users"][user]
    category_names = config['cat_names']
    csp_from_group = user_config['csp_from_group']
    csp_from_category = user_config['csp_from_category']
    csp_labels = user_config['csp_labels']

    # Drop irrelevant columns
    df = df.drop(columns=[
        'pending', 'plaidName', 'notes', 
        'reviewStatus', 'needsReview', 'isSplitTransaction',
        'attachments', 'tags', 'account'
        ])

    # Extract data from dictionary columns
    df['merchant_name'] = df['merchant'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
    df['category_name'] = df['category'].apply(lambda x: x['name'] if isinstance(x, dict) else x)
    df['category_group'] = df['category_name'].map(category_names)

    # Drop categories
    drop_cats = user_config['drop_cats']
    filt = (df['category_name'].isin(drop_cats)) | (df['hideFromReports'] == True)
    df = df.loc[~filt]

    # Remap categories for CSP and set label (e.g., income, fixed)
    df = df.assign(
        csp_from_group=df['category_group'].map(csp_from_group),
        csp_from_category=df['category_name'].map(csp_from_category),
        cat_label=lambda x: x['csp_from_group'].fillna(x['csp_from_category']).fillna('guilt_free')
    )

    # Drop intermediate columns
    df = df.drop(columns=[
        'category', 'category_group', 'category_name', 
        'merchant', 'csp_from_group', 'csp_from_category',
        'hideFromReports', '__typename'
        ])

    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process transactions and export to CSV.")
    parser.add_argument("filepath", type=str, help="Path to the input .pkl file")
    parser.add_argument("--user", type=str, default="erik", help="User key in the config file")
    parser.add_argument("--config", type=str, default="data/config.json", help="Path to the config JSON file")
    args = parser.parse_args()

    # Load data
    df = pd.read_pickle(args.filepath)
    with open(args.config) as f:
        config = json.load(f)

    # Process
    dff = process_transactions(df, config, args.user)
    print(f'Processed {len(dff)} transactions.')

    # Save to CSV
    outpath = os.path.splitext(args.filepath)[0] + ".csv"
    dff.to_csv(outpath, index=False)
    print(f"Saved processed data to {outpath}")
