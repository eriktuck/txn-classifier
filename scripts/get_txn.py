import argparse
import os
import pandas as pd
from monarchmoney import MonarchMoney
from dotenv import load_dotenv
import getpass
import asyncio

async def fetch_transactions(
        year: int, 
        email: str, 
        password: str, 
        device_uuid: str
    ):
    mm = MonarchMoney()
    mm._headers['Device-UUID'] = device_uuid

    try:
        await mm.login(
            email=email,
            password=password,
            use_saved_session=False,
            save_session=False
        )
        print("LOGIN SUCCESSFUL")
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    print(f"Getting transactions from {start_date} to {end_date}")

    transactions = await mm.get_transactions(start_date=start_date, end_date=end_date, limit=None)
    df = pd.DataFrame(transactions['allTransactions']['results'])
    df['date'] = pd.to_datetime(df['date'])
    outpath = f"data/{year}-transactions.pkl"
    df.to_pickle(outpath)
    print(f"Saved to {outpath}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch Monarch Money transactions for a given year.")
    parser.add_argument("year", type=int, help="Year for which to fetch transactions")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    device_uuid = os.getenv("DEVICE_UUID")
    if not device_uuid:
        raise EnvironmentError("DEVICE_UUID not found in environment")

    # Prompt for credentials
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")

    # Run async transaction fetcher
    asyncio.run(fetch_transactions(args.year, email, password, device_uuid))
