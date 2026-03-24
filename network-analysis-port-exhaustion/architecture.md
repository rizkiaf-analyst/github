```
[  TESTER / CLIENT  ]
( Python-based concurrent request generator (~500 concurrent requests) )
                     |
                     | HTTP Requests (20,000)
                     v
          +-------------------------+
          |    NGINX EDGE PROXY     |  <-- Layer 1: Client Entry Point & Routing/Reverse Proxy
          |      (Port 80)          |
          +----------+--------------+
                     |
                     v
          +-------------------------+
          |      VM-HAPROXY         |  <-- Layer 2: Load Balancer
          |   (Weight 80:20)        |      (Weighted Round Robin)
          +----------+--------------+
                     |
          ___________|___________
         | (80%)                 | (20%)
         v                       v
  +--------------+        +--------------+
  |     VM 1     |        |     VM 3     |
  |  (Nginx WS)  |        |  (Nginx WS)  |  <-- Layer 3: Web Servers
  | [Primary]    |        | [Secondary]  |
  +-------+------+        +-------+------+
          |                       |
          +-----------+-----------+
                      |
                      v
          +-------------------------+
          |          VM 2           |  <-- Layer 4: Shared Database
          |       (Shared DB)       |      (Persistence Layer)
          +-------------------------+

      [  MONITORING STACK  ]
      ( Grafana + Prometheus )
               |
      _________|_________
     |         |         |
     v         v         v
 [ VM 1 ]   [ VM 2 ]   [ VM 3 ]
 (Node Exporter Monitoring Flow)
```