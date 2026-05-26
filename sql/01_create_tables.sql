-- Table principale : clients
CREATE TABLE customers (
    customer_id       VARCHAR(20) PRIMARY KEY,
    gender            VARCHAR(10),
    senior_citizen    SMALLINT,
    partner           BOOLEAN,
    dependents        BOOLEAN,
    tenure            INTEGER,
    phone_service     BOOLEAN,
    multiple_lines    VARCHAR(20),
    internet_service  VARCHAR(20),
    online_security   VARCHAR(20),
    online_backup     VARCHAR(20),
    device_protection VARCHAR(20),
    tech_support      VARCHAR(20),
    streaming_tv      VARCHAR(20),
    streaming_movies  VARCHAR(20),
    contract          VARCHAR(20),
    paperless_billing BOOLEAN,
    payment_method    VARCHAR(40),
    monthly_charges   NUMERIC(8,2),
    total_charges     NUMERIC(10,2),
    churn             BOOLEAN,
    created_at        TIMESTAMP DEFAULT NOW()
);

-- Vue analytique : segments clients
CREATE VIEW customer_segments AS
SELECT
    customer_id,
    tenure,
    monthly_charges,
    total_charges,
    contract,
    churn,
    CASE
        WHEN tenure <= 12  THEN 'Nouveau (0-1 an)'
        WHEN tenure <= 36  THEN 'Intermédiaire (1-3 ans)'
        WHEN tenure <= 60  THEN 'Fidèle (3-5 ans)'
        ELSE 'Très fidèle (5+ ans)'
    END AS tenure_segment,
    CASE
        WHEN monthly_charges < 35  THEN 'Petit compte'
        WHEN monthly_charges < 65  THEN 'Compte moyen'
        ELSE 'Grand compte'
    END AS value_segment
FROM customers;