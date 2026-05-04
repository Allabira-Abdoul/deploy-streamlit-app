## 2025-02-20 - Optimizing Scikit-learn Single Row Predictions
**Learning:** For scikit-learn models (like RandomForest) deployed in an interactive UI (like Streamlit), creating a `pd.DataFrame` for a single-row prediction introduces significant overhead compared to a plain list of lists or numpy array. Additionally, calling `predict()` followed by `predict_proba()` traverses the decision trees twice, doubling inference time.
**Action:** Always convert single-row inference inputs to a 2D list `[list(data.values())]` and use `predict_proba()` to compute both the probabilities and the class via `model.classes_[np.argmax(prob)]` in a single pass.
## 2024-05-24 - Model Prediction Overhead
**Learning:** Instantiating a Pandas DataFrame purely to feed into `model.predict()` adds overhead. However, the scikit-learn model here complains with warnings if feature names are absent, and avoiding the DataFrame only saves ~10% prediction time for a single row. The real bottleneck is Streamlit recreating the DataFrame every single interaction when state changes.
**Action:** Caching the dictionary keys/lists creation inside Streamlit is trivial. However, since the dictionary values change with inputs, we can't cache the DataFrame itself unless we use `st.cache_data`. But `predict` is fast enough anyway. What else? `freq_maps` is re-created every time. Can we cache it or move it outside if it's static?

## 2024-05-24 - predict vs predict_proba + argmax/thresholding
**Learning:** `model.predict_proba()` followed by thresholding/argmax in scikit-learn is significantly faster (~2x in some cases) than calling `model.predict()` and `model.predict_proba()` together. `model.predict()` just runs `predict_proba()` and takes the argmax under the hood anyway.
**Action:** Replace `model.predict()` + `model.predict_proba()` calls with a single `model.predict_proba()` call and manual thresholding.
