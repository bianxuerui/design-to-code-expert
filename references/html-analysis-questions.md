# HTML Analysis Questions

Use these questions before writing implementation code.

## Structure

- What are the top-level semantic regions (header/main/section/footer/nav)?
- Which blocks repeat and should become reusable components?
- Which node groups are likely layout containers vs content items?
- Which elements indicate page-level responsibilities vs section-level responsibilities?

## Visual Tokens

- What are the primary, secondary, and accent colors?
- Which font sizes map to heading/body/caption levels?
- Which spacing values repeat and can become tokenized spacing scale?
- Which border radius values recur for cards/buttons/chips?
- Which shadow patterns represent elevation levels?

## Interaction

- Which nodes are explicitly interactive (button/link/input/select)?
- Are there hover/focus/active hints in class names or inline styles?
- Which actions are primary vs secondary call to action?
- Are there form states, disabled states, or validation hints?

## Responsiveness and Edge Cases

- How does the layout behave on narrow widths?
- Which blocks overflow and need wrapping or truncation rules?
- Are there long text, empty data, and missing image scenarios?
- Which sections must remain accessible with keyboard navigation?

## Fidelity Decision Questions

- What must be pixel-close and what can be implementation-equivalent?
- Which visual details are unavailable in source HTML and require assumptions?
- Which assumptions must be confirmed with the user before coding?
