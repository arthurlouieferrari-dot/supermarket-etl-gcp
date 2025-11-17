flowchart TB
    CS[Cloud Scheduler<br/>Cron Trigger]
    CR[Cloud Run Job<br/>Python ETL (Pandas)]
    SM[Secret Manager<br/>(API + BQ Credentials)]
    RAW[Cloud Storage<br/>Raw Kaggle Files]
    BQ[BigQuery<br/>Dim + Fact Tables]
    BQREP[BigQuery Scheduled Query<br/>Analytical Report]
    BI[Looker Studio / BI Tools]

    %% Data Flow
    CS --> CR
    SM --> CR
    CR --> RAW
    CR --> BQ
    BQ --> BQREP
    BQREP --> BI

    %% Scaling Strategy (Notes Only)
    subgraph notes [Scalability Strategy]
        A["Initial Lift & Shift: Pandas in Cloud Run (current)"]
        B["Next Phase: ELT in BigQuery SQL (when data grows)"]
        C["Advanced Scale: Dataflow / Dataproc (if needed for large batch/stream)"]
    end
