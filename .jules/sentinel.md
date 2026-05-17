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
## 2024-05-06 - [Backend Validation Bypass Leading to Stack Trace Leak]
**Vulnerability:** Input validation dict lookups crashing on unhashable types (like lists passed via websocket), bypassing UI restrictions and causing `TypeError` to leak stack traces.
**Learning:** Malicious actors can send unexpected types via WebSocket. If backend input validation relies on dictionary keys without type checking or try/except wrapping, it crashes before rejecting the input, resulting in unhandled exceptions and leaked internal info.
**Prevention:** Always wrap backend input validation logic in a `try...except Exception` block to catch type errors and return a generic secure error message. Also, ensure backend boundaries perfectly mirror frontend constraints to avoid abrupt errors on edge cases.
## 2026-05-09 - Incomplete Backend Validation in Streamlit Apps
**Vulnerability:** Not all numeric inputs from Streamlit frontend widgets had server-side bounds checking.
**Learning:** Frontend UI components in Streamlit (like `st.slider` min/max) only restrict normal browser interaction. A malicious user can intercept and modify WebSocket messages to send out-of-bounds data to the server, which could crash the application or cause unexpected behavior when processing the data in ML models.
**Prevention:** Always implement explicit, comprehensive backend bounds checking and validation logic for ALL input data received from Streamlit widgets as a defense-in-depth measure, regardless of frontend constraints.
## 2025-02-28 - Comprehensive Streamlit Input Validation
**Vulnerability:** Incomplete backend validation for Streamlit frontend widgets. Only a few fields were validated, leaving many numerical inputs (like daily_rate, hourly_rate, etc.) unprotected against WebSocket tampering.
**Learning:** Frontend widget constraints (e.g., `st.slider(..., min_value=1, max_value=5)`) do not provide true security, as malicious actors can directly manipulate the underlying WebSocket payload to send out-of-bounds data.
**Prevention:** Always implement comprehensive server-side bounds checking and categorical validation for ALL inputs received from Streamlit widgets before using them in backend processing (like ML predictions or database queries).
## 2024-05-10 - [Backend Type Validation for Streamlit Widgets]
**Vulnerability:** Missing explicit server-side type validation for Streamlit widgets.
**Learning:** Even though backend validation and boundary checks were present for Streamlit widgets, malicious actors could still bypass logic by manipulating WebSocket messages to send completely different data types, leading to potential type-confusion attacks or unhandled exceptions that could leak internal stack traces.
**Prevention:** Implement explicit type checking using `isinstance()` for all inputs received from the user on the backend (e.g. `isinstance(val, (int, float))` for numerical values and `isinstance(val, str)` for categorical features) before executing further bound-checking logic or machine learning operations.
## 2026-05-10 - Strict Input Type Validation for Streamlit Widgets
**Vulnerability:** Type confusion and potential bypass of bounds/logical checking logic.
**Learning:** While Streamlit UI elements theoretically restrict types, malicious users interacting via WebSocket can inject unintended data types (like nested arrays or dicts) which might pass numeric bounds checking or crash the backend validation layer unexpectedly before triggering a secure stop. Global `except Exception` handlers are a last resort, not primary validation.
**Prevention:** In addition to bounds and categorical validation, implement strict, explicit type checking (e.g., `isinstance(val, (int, float))`) at the beginning of the backend processing logic to ensure inputs received from widgets match the expected data structure.
## 2026-05-17 - [Strict Type Checking & Input Length Validation for Streamlit]
**Vulnerability:** Type confusion via boolean inputs passing `isinstance(x, (int, float))` and potential DoS via unbounded string inputs over WebSockets.
**Learning:** `bool` is a subclass of `int` in Python, so boolean values maliciously injected via WebSockets will pass `isinstance(x, int)` validation checks. Furthermore, Streamlit string inputs are inherently unbounded, creating a Denial of Service (DoS) risk if an attacker sends massive string payloads.
**Prevention:** Use explicit `type(x) in (int, float)` and `type(x) is str` instead of `isinstance` for backend input validation in Streamlit apps. Additionally, enforce explicit maximum length limits on all string payloads.
