import pandas as pd
import requests
from pathlib import Path


BASE_URL = "https://fakestoreapi.com"
OUTPUT_DIR = Path("data/raw/api")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_endpoint(endpoint):
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )
    response.raise_for_status()

    return response.json()


def save_fallback_data():
    print("⚠️ API indisponible. Utilisation de données fallback.")

    products = pd.DataFrame([
        {
            "id": 1,
            "title": "Fallback Product",
            "price": 99.99,
            "category": "electronics",
            "description": "Produit fallback pour CI/CD"
        }
    ])

    users = pd.DataFrame([
        {
            "id": 1,
            "email": "fallback@example.com",
            "username": "fallback_user"
        }
    ])

    carts = pd.DataFrame([
        {
            "id": 1,
            "userId": 1,
            "date": "2026-01-01"
        }
    ])

    products.to_csv(OUTPUT_DIR / "fakestore_products.csv", index=False)
    users.to_csv(OUTPUT_DIR / "fakestore_users.csv", index=False)
    carts.to_csv(OUTPUT_DIR / "fakestore_carts.csv", index=False)


def extract_products():
    data = fetch_endpoint("products")
    df = pd.json_normalize(data)
    df.to_csv(OUTPUT_DIR / "fakestore_products.csv", index=False)
    print(f"{len(df)} produits récupérés depuis l'API.")


def extract_users():
    data = fetch_endpoint("users")
    df = pd.json_normalize(data)
    df.to_csv(OUTPUT_DIR / "fakestore_users.csv", index=False)
    print(f"{len(df)} users récupérés depuis l'API.")


def extract_carts():
    data = fetch_endpoint("carts")
    df = pd.json_normalize(data)
    df.to_csv(OUTPUT_DIR / "fakestore_carts.csv", index=False)
    print(f"{len(df)} carts récupérés depuis l'API.")


if __name__ == "__main__":
    try:
        extract_products()
        extract_users()
        extract_carts()
    except Exception as e:
        print(f"❌ Erreur API : {e}")
        save_fallback_data()
        print("✅ Fichiers API fallback générés avec succès.")
