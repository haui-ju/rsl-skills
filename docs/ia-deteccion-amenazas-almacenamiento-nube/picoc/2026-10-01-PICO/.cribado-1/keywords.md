# Rendimiento de los términos de la query (cribado 1)

Sobre 292 registros únicos (título, resumen y palabras clave). SI incluye las dudas. «Solo este término» = registros que ningún otro término de su componente recupera (se perderían si se quita).

| Comp. | Término | Registros | SI | NO | Solo este término (SI / NO) |
|---|---|---|---|---|---|
| P | `cloud storage` | 16 | 16 | 0 | 0 / 0 |
| P | `cloud storag*` | 16 | 16 | 0 | 0 / 0 |
| P | `object storage` | 1 | 1 | 0 | 1 / 0 |
| P | `data storage` | 39 | 33 | 6 | 29 / 6 |
| P | `s3` | 13 | 13 | 0 | 11 / 0 |
| P | `amazon s3` | 1 | 1 | 0 | 0 / 0 |
| P | `blob storage` | 1 | 1 | 0 | 0 / 0 |
| P | `data event*` | 1 | 1 | 0 | 1 / 0 |
| P | `access log*` | 5 | 5 | 0 | 4 / 0 |
| P | `audit log` | 1 | 1 | 0 | 1 / 0 |
| P | `cloud computing security` | 7 | 5 | 2 | 3 / 2 |
| P | `insider threat` | 6 | 6 | 0 | 4 / 0 |
| P | `credential` | 11 | 8 | 3 | 6 / 3 |
| P | `telemetry` | 133 | 85 | 48 | 81 / 48 |
| I | `artificial intelligence` | 47 | 40 | 7 | 18 / 3 |
| I | `machine learning` | 137 | 103 | 34 | 0 / 0 |
| I | `machine-learning` | 137 | 103 | 34 | 0 / 0 |
| I | `deep learning` | 91 | 74 | 17 | 30 / 7 |
| I | `anomaly detection` | 106 | 84 | 22 | 28 / 10 |
| I | `supervised learning` | 7 | 4 | 3 | 1 / 0 |
| I | `unsupervised learning` | 2 | 1 | 1 | 0 / 0 |
| I | `data mining` | 7 | 7 | 0 | 3 / 0 |
| C | `rule-based` | 32 | 26 | 6 | 17 / 3 |
| C | `signature` | 20 | 16 | 4 | 13 / 2 |
| C | `threshold` | 91 | 78 | 13 | 69 / 10 |
| C | `static rule` | 2 | 2 | 0 | 0 / 0 |
| C | `statistical method` | 1 | 0 | 1 | 0 / 0 |
| C | `intrusion detection` | 105 | 60 | 45 | 49 / 39 |
| C | `access control` | 35 | 30 | 5 | 21 / 4 |
| O | `measurement` | 18 | 15 | 3 | 9 / 0 |
| O | `metric` | 10 | 7 | 3 | 4 / 0 |
| O | `metrics` | 71 | 53 | 18 | 18 / 7 |
| O | `precision` | 106 | 81 | 25 | 18 / 4 |
| O | `recall` | 83 | 61 | 22 | 8 / 5 |
| O | `classification accuracy` | 17 | 11 | 6 | 8 / 3 |
| O | `false alarm` | 16 | 10 | 6 | 3 / 2 |
| O | `detection rate` | 20 | 15 | 5 | 3 / 3 |
| O | `latency` | 112 | 88 | 24 | 53 / 13 |
| O | `detection time` | 3 | 2 | 1 | 0 / 1 |

Sin registros: `storage bucket` (P).

## Palabras clave de las fuentes que ninguna query cubre (≥ 1 registro aceptado y al menos tantos SI como NO)

| Palabra clave | SI | NO |
|---|---|---|
| digital storage | 35 | 0 |
| cloud computing | 33 | 3 |
| internet of things | 28 | 9 |
| network security | 25 | 8 |
| cloud-computing | 19 | 1 |
| edge computing | 16 | 4 |
| learning systems | 15 | 2 |
| internet | 15 | 9 |
| blockchain | 14 | 5 |
| cybersecurity | 13 | 5 |
| diagnosis | 12 | 0 |
| cloud security | 12 | 0 |
| article | 12 | 1 |
| humans | 11 | 0 |
| human | 11 | 0 |
| feature extraction | 11 | 4 |
| iot | 10 | 8 |
| network architecture | 9 | 0 |
| data privacy | 9 | 1 |
| classification (of information) | 8 | 0 |
| algorithm | 8 | 1 |
| aerospace and electronic systems | 8 | 4 |
| federated learning | 8 | 5 |
| algorithms | 7 | 0 |
| information management | 7 | 0 |
| random forests | 7 | 1 |
| internet of things (iot) | 7 | 2 |
| classification | 7 | 2 |
| ensemble learning | 7 | 3 |
| feature selection | 7 | 5 |
| big data | 6 | 0 |
| predictive maintenance | 6 | 0 |
| random forest | 6 | 0 |
| controlled study | 6 | 0 |
| computer security | 6 | 1 |
| system | 6 | 1 |
| optimization | 6 | 1 |
| authentication | 6 | 2 |
| real-time systems | 6 | 2 |
| privacy | 6 | 3 |
| autoencoder | 6 | 3 |
| central processing unit | 6 | 3 |
| fog computing | 5 | 0 |
| predictive analytics | 5 | 0 |
| cloud computing architecture | 5 | 0 |
| convolutional neural network | 5 | 0 |
| outlier detection | 5 | 0 |
| digital twin | 5 | 1 |
| framework | 5 | 1 |
| cryptography | 5 | 1 |
| prediction | 5 | 1 |
| computer crime | 5 | 2 |
| modeling | 5 | 2 |
| computer architecture | 5 | 3 |
| medical computing | 4 | 0 |
| benchmarking | 4 | 0 |
| cloud | 4 | 0 |
| cloud securities | 4 | 0 |
| telemetering | 4 | 0 |
| telemetering equipment | 4 | 0 |
