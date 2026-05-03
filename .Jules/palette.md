## 2026-05-03 - [Explicit Step Sizes for Streamlit Number Inputs]
**Learning:** For Streamlit applications, explicitly set a custom `step` size for `st.number_input` widgets with large value ranges, as the default step of 1 provides poor UX for quick adjustments.
**Action:** Added `step=500` to the `Monthly Income ($)` number input and `step=1` to the `Distance From Home (km)` number input to improve usability and allow for quicker, more intuitive value adjustments using arrow keys.
