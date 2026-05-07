## 2024-05-24 - [Avoid Double Inference in Scikit-Learn]
**Learning:** Calling both `model.predict(X)` and `model.predict_proba(X)` on a scikit-learn model performs the full inference twice, effectively doubling the execution time.
**Action:** When both the class prediction and probabilities are needed, always call `predict_proba` once and compute the predicted class using `model.classes_[np.argmax(prob)]` to cut inference time in half.
## 2025-02-20 - Optimizing Scikit-learn Single Row Predictions
**Learning:** For scikit-learn models (like RandomForest) deployed in an interactive UI (like Streamlit), creating a `pd.DataFrame` for a single-row prediction introduces significant overhead compared to a plain list of lists or numpy array. Additionally, calling `predict()` followed by `predict_proba()` traverses the decision trees twice, doubling inference time.
**Action:** Always convert single-row inference inputs to a 2D list `[list(data.values())]` and use `predict_proba()` to compute both the probabilities and the class via `model.classes_[np.argmax(prob)]` in a single pass.
## 2024-05-24 - Model Prediction Overhead
**Learning:** Instantiating a Pandas DataFrame purely to feed into `model.predict()` adds overhead. However, the scikit-learn model here complains with warnings if feature names are absent, and avoiding the DataFrame only saves ~10% prediction time for a single row. The real bottleneck is Streamlit recreating the DataFrame every single interaction when state changes.
**Action:** Caching the dictionary keys/lists creation inside Streamlit is trivial. However, since the dictionary values change with inputs, we can't cache the DataFrame itself unless we use `st.cache_data`. But `predict` is fast enough anyway. What else? `freq_maps` is re-created every time. Can we cache it or move it outside if it's static?

## 2024-05-24 - predict vs predict_proba + argmax/thresholding
**Learning:** `model.predict_proba()` followed by thresholding/argmax in scikit-learn is significantly faster (~2x in some cases) than calling `model.predict()` and `model.predict_proba()` together. `model.predict()` just runs `predict_proba()` and takes the argmax under the hood anyway.
**Action:** Replace `model.predict()` + `model.predict_proba()` calls with a single `model.predict_proba()` call and manual thresholding.
## 2025-02-20 - Unnecessary Pandas Import in Streamlit
**Learning:** Importing heavy libraries like `pandas` (which takes ~0.6s and ~86MB RAM) when they are completely unused adds significant startup overhead to Streamlit apps, which rerun top-to-bottom on every user interaction.
**Action:** Always verify if heavy dependencies are actually used. If not, remove them to instantly improve load times and memory footprint without affecting functionality.
## 2024-05-24 - Streamlit Initialization Overhead from Heavy Imports
**Learning:** Streamlit's execution model reruns the entire script from top to bottom on every user interaction. Heavy imports like `pandas` (which takes ~0.5s to import) cause a significant and noticeable delay on every interaction even if they are minimally used (e.g., just for formatting a single prediction row).
**Action:** Avoid heavy unused or minimally used dependencies like `pandas` in Streamlit apps. Use native Python data structures (like list comprehensions) where possible to reduce initialization overhead and improve app responsiveness.
## 2025-02-24 - Streamlit Form Batching for Performance
**Learning:** Streamlit reruns the entire script top-to-bottom on every single widget interaction (like dragging a slider or changing a selectbox). In an application with many inputs, this causes significant lag and high CPU usage due to continuous script execution.
**Action:** Always wrap groups of input widgets and their final submission button inside an `st.form(...)` using `st.form_submit_button()`. This batches all user input state changes together, deferring the script rerun until the submit button is explicitly clicked, dramatically improving UI responsiveness.
