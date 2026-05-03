import requests
import pandas as pd


BASE_URL = "https://fakestoreapi.com"


def fetch_endpoint(endpoint):
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()


def extract_products():
    data = fetch_endpoint("products")
    df = pd.json_normalize(data)
    df.to_csv("data/raw/api/fakestore_products.csv", index=False)
    print(f"{len(df)} produits récupérés depuis l'API.")


def extract_users():
    data = fetch_endpoint("users")
    df = pd.json_normalize(data)
    df.to_csv("data/raw/api/fakestore_users.csv", index=False)
    print(f"{len(df)} users récupérés depuis l'API.")


def extract_carts():
    data = fetch_endpoint("carts")
    df = pd.json_normalize(data)
    df.to_csv("data/raw/api/fakestore_carts.csv", index=False)
    print(f"{len(df)} carts récupérés depuis l'API.")


if __name__ == "__main__":
    extract_products()
    extract_users()
    extract_carts()