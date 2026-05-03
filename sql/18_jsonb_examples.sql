-- =====================================================
-- 18 - JSONB EXAMPLES
-- =====================================================

-- Créer une table pour stocker des événements API en JSONB

DROP TABLE IF EXISTS raw.api_events;

CREATE TABLE raw.api_events (
    event_id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    event_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Insérer des exemples JSONB

INSERT INTO raw.api_events (source, event_data)
VALUES
(
    'fakestoreapi',
    '{
        "event_type": "product_view",
        "product_id": 10,
        "user_id": 5,
        "device": "mobile"
    }'
),
(
    'fakestoreapi',
    '{
        "event_type": "add_to_cart",
        "product_id": 3,
        "user_id": 8,
        "device": "desktop"
    }'
);


-- Lire des champs JSONB

SELECT
    event_id,
    event_data ->> 'event_type' AS event_type,
    event_data ->> 'device' AS device,
    (event_data ->> 'product_id')::integer AS product_id
FROM raw.api_events;


-- Filtrer sur JSONB

SELECT *
FROM raw.api_events
WHERE event_data ->> 'device' = 'mobile';


-- Index JSONB

CREATE INDEX IF NOT EXISTS idx_api_events_event_data
ON raw.api_events
USING GIN (event_data);