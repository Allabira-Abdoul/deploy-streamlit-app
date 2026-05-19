## 2026-05-03 - [Explicit Step Sizes for Streamlit Number Inputs]
**Learning:** For Streamlit applications, explicitly set a custom `step` size for `st.number_input` widgets with large value ranges, as the default step of 1 provides poor UX for quick adjustments.
**Action:** Added `step=500` to the `Monthly Income ($)` number input and `step=1` to the `Distance From Home (km)` number input to improve usability and allow for quicker, more intuitive value adjustments using arrow keys.
## 2024-05-02 - Number Input Range Steps
**Learning:** Streamlit number inputs with large ranges (e.g. 1000-20000) default to step=1, which is a poor UX for quick adjustments. Setting a custom step size (e.g. 500) significantly improves usability.
**Action:** Always verify the default step size for number inputs with large value ranges and adjust it to match typical user interaction patterns.
## 2024-05-01 - Clarified Slider Meanings
**Learning:** Users lack context when inputs like Environment Satisfaction and Work-Life Balance are given on a 1-4 scale. They may not know what each value signifies.
**Action:** Always add `help` text on numerical sliders that map to semantic labels to clarify meaning for users.
## 2026-05-04 - Streamlit Button State Reset
**Learning:** Streamlit's interaction model causes button states (like 'analyze_clicked') to reset when any other input parameter is changed. This leads to the prediction results disappearing, leaving a confusing empty space and no feedback for the user.
**Action:** Always provide a clear empty state (e.g., using `st.info`) for conditional blocks triggered by buttons, guiding users on the required action to populate the space.
## 2026-05-04 - [Align UI Input Constraints with Backend Validation]
**Learning:** If the UI widget (like `st.number_input`) allows values outside the strict backend validation bounds (e.g., UI `max_value=50` but backend `< 30`), users encounter abrupt error messages when interacting normally.
**Action:** Always check the backend constraints (Sentinel) and ensure the frontend UI widget parameters (`min_value`, `max_value`) precisely match them to naturally prevent invalid inputs and provide a smoother user experience.
## 2024-05-24 - Streamlit Slider Ordinal Tooltips
**Learning:** Streamlit sliders used for encoded ordinal data require explicit `help` text since Streamlit doesn't natively support custom text labels for slider ticks. Users can find 1-4 scales ambiguous without context.
**Action:** Always add `help` tooltips to clarify the meaning of ordinal numeric values in Streamlit sliders to reduce cognitive load.
## 2026-05-09 - [Dynamically Constrained Sliders Disabled State]
**Learning:** In Streamlit applications, dynamically constrained sliders that drop to an operational range of zero should be set with `disabled=True` and paired with a `help` tooltip to clarify the constrained UI state and prevent user confusion.
**Action:** Disabled the dependent tenure sliders (`num_cos`, `years_at_co`, etc.) when their maximum constraint dropped to 0, providing a tooltip explaining the dependency.

## 2024-05-24 - Disabling Contextually Constrained Sliders
**Learning:** In Streamlit, dynamically constrained sliders (where max_value changes based on another input, dropping to 0) can result in sliders that appear interactive but cannot be moved, leading to a confusing UX.
**Action:** Add `disabled=condition` and a corresponding `help="Reason"` tooltip to Streamlit widgets when their constraints drop their operational range to zero, ensuring clear feedback and preventing user frustration.
## 2024-05-24 - Formatting Slider Values
**Learning:** Streamlit's `st.slider` `format` parameter accepts arbitrary text strings combined with printf-style formatting (e.g., `format="%d%%"` or `format="%d km"`). This is highly useful for clarifying measurement units directly on the slider handle.
**Action:** Use the `format` parameter on Streamlit sliders to display relevant units directly to the user to improve clarity and reduce ambiguity.
## $(date +%Y-%m-%d) - Streamlit Number Input Formatting
**Learning:** In Streamlit, `st.slider`'s `format` parameter accepts arbitrary text suffixes (e.g., `format="%d years"`), making it excellent for inline units. However, `st.number_input`'s `format` parameter strictly requires Python printf-style types (`%d`, `%f`) and throws errors for text prefixes/suffixes.
**Action:** When adding units to Streamlit numeric widgets, use the `format` parameter for `st.slider`, but append the unit directly to the label string (e.g., `'MONTHLY RATE ($)'`) for `st.number_input`.
## 2026-05-19 - [Radio Buttons over Selectboxes for Small Categorical Inputs]
**Learning:** For categorical inputs with only 2-3 options (like Gender or Marital Status), `st.selectbox` hides the options behind a click, increasing interaction cost.
**Action:** Use `st.radio` with `horizontal=True` instead of `st.selectbox` for short categorical lists to immediately expose all options, reducing cognitive load and saving clicks.
