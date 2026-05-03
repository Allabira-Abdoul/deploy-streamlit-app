## 2024-05-24 - [Avoid Double Inference in Scikit-Learn]
**Learning:** Calling both `model.predict(X)` and `model.predict_proba(X)` on a scikit-learn model performs the full inference twice, effectively doubling the execution time.
**Action:** When both the class prediction and probabilities are needed, always call `predict_proba` once and compute the predicted class using `model.classes_[np.argmax(prob)]` to cut inference time in half.
