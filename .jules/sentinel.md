## 2024-05-04 - [Insecure Deserialization of ML Model]
**Vulnerability:** CRITICAL: Loading an untrusted Random Forest model using `pickle.load()` (`rfc.pkl`).
**Learning:** `pickle` is inherently insecure as it can execute arbitrary code upon deserialization. This makes the application vulnerable if the `.pkl` file is modified.
**Prevention:** Always use secure persistence formats for machine learning models, such as `skops` for scikit-learn models. Replaced `pickle.load` with `skops.io.load` and checked for untrusted types dynamically.
## 2026-05-03 - [Streamlit Exception Handling]
**Vulnerability:** Unhandled exceptions during file loading or model prediction could expose internal Python stack traces to the web UI.
**Learning:** Streamlit apps without explicit top-level exception handling will dump stack traces to the browser, potentially leaking application internals or deployment paths.
**Prevention:** Always wrap critical external or data-processing operations in try-except blocks, use st.error() for safe messaging, and st.stop() to halt execution securely.
## 2024-05-24 - [Medium] Prevent stack trace leakage in Streamlit\n**Vulnerability:** Unhandled exceptions in Streamlit applications render stack traces directly in the UI, potentially exposing internal file paths and logic.\n**Learning:** In Streamlit, unhandled exceptions are a security risk due to default UI rendering.\n**Prevention:** Wrap risky operations (like file loading or model prediction) in try-except blocks, log errors securely if needed, and use st.stop() to halt execution cleanly after displaying a generic error message.
## 2024-06-25 - [Streamlit Exception Handling]
**Vulnerability:** Information Disclosure
**Learning:** Default unhandled exceptions in Streamlit applications often render the full Python stack trace directly in the UI for the user. This exposes application internals, potentially leaking file paths or database structure.
**Prevention:** Always wrap critical data loading (`pickle.load`, file operations) and model inference (`model.predict`) sections in `try/except` blocks. Use `st.error()` to provide a sanitized, generic message to the user while employing `st.stop()` to halt further execution gracefully.
## 2026-05-04 - [Streamlit Session State Limitations for Rate Limiting]
**Vulnerability:** DoS mitigation using `st.session_state` is ineffective and acts as security theater.
**Learning:** Streamlit creates a new, isolated `session_state` for every websocket connection (i.e., every new browser tab or programmatic connection). An attacker can easily open multiple connections to bypass per-session rate limits.
**Prevention:** Do not use `st.session_state` for global rate limiting or DoS protection. Implement true global rate limiting at the proxy/web server layer.

## 2026-05-04 - [Backend Input Validation for Streamlit Widgets]
**Vulnerability:** Relying solely on frontend Streamlit widgets for input constraint validation.
**Learning:** While Streamlit frontend widgets restrict user inputs under normal browser interactions, malicious actors can directly interact with the underlying WebSocket to send out-of-bounds or invalid payload data.
**Prevention:** Always implement explicit server-side backend input validation (e.g., bounds checking and categorical validation) for data received from Streamlit widgets before processing it in the backend.
