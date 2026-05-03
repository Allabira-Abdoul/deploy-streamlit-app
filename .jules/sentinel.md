## 2026-05-03 - [Streamlit Exception Handling]
**Vulnerability:** Unhandled exceptions during file loading or model prediction could expose internal Python stack traces to the web UI.
**Learning:** Streamlit apps without explicit top-level exception handling will dump stack traces to the browser, potentially leaking application internals or deployment paths.
**Prevention:** Always wrap critical external or data-processing operations in try-except blocks, use st.error() for safe messaging, and st.stop() to halt execution securely.
