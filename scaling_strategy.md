## Scaling Strategy
```mermaid
    %% Strategy Notes (Not connected to graph)
    subgraph Scale [Scaling Strategy]
        A["Phase 1: Initial Lift & Shift<br/>• Pandas in Cloud Run<br/>(current implementation)"]
        B["Phase 2 (if required): Scale in Warehouse<br/>• Transformations in BigQuery SQL"]
        C["Phase 3 (if required): High Volume ETL<br/>• Dataflow / Dataproc for big/streaming jobs"]
    end
```
