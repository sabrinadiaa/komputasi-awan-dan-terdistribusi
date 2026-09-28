   ```mermaid
   graph LR
      C[Pelanggan]
      O[Order Service]
      K[Catalog Service]
      P[Payment Service]
      B[Message Broker]
      R[Restaurant Service]
      Q[Courier notification service]

      C -->|HTTP Request| O

      O -->|Sinkron: Request| K
      K -->|Sinkron: Request| O

      O -->|Sinkron: Request| P
      P -->|Sinkron: Request| O

      O -->|Asinkron: OrderCreated| B
      B -->|Asinkron| R

      R -->|Asinkron: OrderReady| B
      B -->|Asinkron| Q

      Q -->|Asinkron: CourierAssigned| B
      B -->|Asinkron| O

      O -->|Status Pesanan|C
   ```
