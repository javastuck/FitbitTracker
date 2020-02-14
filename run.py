from fitbit_tracker.fitbit_client import FitbitClient

if __name__ == "__main__":
    client = FitbitClient()
    print(client.get_one_day_data(2019, 12, 31))