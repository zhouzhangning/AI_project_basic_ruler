# Spec-First Standard

Use a Spec to remove ambiguity before implementation. Keep it short enough to execute, but precise enough to test.

## Required Sections

```markdown
# Spec: <feature or fix name>

## Goal
What user-visible or system behavior must change.

## Scope
In scope:
- ...

Out of scope:
- ...

## Inputs And Outputs
Inputs:
- file/API/UI/action:

Outputs:
- file/API/UI/state:

## Behavior
- Normal path:
- Empty/missing data:
- Invalid data:
- Compatibility:

## Risk
- Data loss:
- Security/permission:
- Performance:
- Release/update:

## Acceptance Tests
- Given ... when ... then ...
- Command/artifact verification:

## Implementation Notes
- Existing module/pattern to follow:
- Files likely touched:
```

## When A Full Spec Is Not Needed

Use a short plan instead for:

- typo or text-only change
- one-line bug fix with obvious behavior
- build/test command execution
- pure documentation wording with no process impact

Even then, state verification.
