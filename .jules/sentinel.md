## 2024-05-04 - [Insecure Deserialization of ML Model]
**Vulnerability:** CRITICAL: Loading an untrusted Random Forest model using `pickle.load()` (`rfc.pkl`).
**Learning:** `pickle` is inherently insecure as it can execute arbitrary code upon deserialization. This makes the application vulnerable if the `.pkl` file is modified.
**Prevention:** Always use secure persistence formats for machine learning models, such as `skops` for scikit-learn models. Replaced `pickle.load` with `skops.io.load` and checked for untrusted types dynamically.
