import pandas as pd
from pathlib import Path

from sqlalchemy import inspect, text

from utils import get_postgres_engine


def load_csv_folder_to_postgres(folder_path, schema="raw"):
    engine = get_postgres_engine()
    folder = Path(folder_path)

    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

    for file_path in folder.glob("*.csv"):
        table_name = file_path.stem
        df = pd.read_csv(file_path)

        print(f"📥 Chargement de {file_path.name} → {schema}.{table_name}")

        inspector = inspect(engine)
        table_exists = inspector.has_table(table_name, schema=schema)

        if table_exists:
            with engine.begin() as conn:
                conn.execute(
                    text(f'TRUNCATE TABLE {schema}.{table_name} RESTART IDENTITY CASCADE')
                )

            if_exists_mode = "append"
        else:
            print(f"⚠️ Table {schema}.{table_name} inexistante. Création de la table.")
            if_exists_mode = "replace"

        df.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists=if_exists_mode,
            index=False
        )

        print(f"✅ {len(df)} lignes chargées dans {schema}.{table_name}")


if __name__ == "__main__":
    load_csv_folder_to_postgres("data/raw/simulated", schema="raw")
    load_csv_folder_to_postgres("data/raw/api", schema="raw")
