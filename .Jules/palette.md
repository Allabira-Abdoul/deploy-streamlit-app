## 2024-05-02 - Number Input Range Steps
**Learning:** Streamlit number inputs with large ranges (e.g. 1000-20000) default to step=1, which is a poor UX for quick adjustments. Setting a custom step size (e.g. 500) significantly improves usability.
**Action:** Always verify the default step size for number inputs with large value ranges and adjust it to match typical user interaction patterns.
## 2024-05-01 - Clarified Slider Meanings
**Learning:** Users lack context when inputs like Environment Satisfaction and Work-Life Balance are given on a 1-4 scale. They may not know what each value signifies.
**Action:** Always add `help` text on numerical sliders that map to semantic labels to clarify meaning for users.
