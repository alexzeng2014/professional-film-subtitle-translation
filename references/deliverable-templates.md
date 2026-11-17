# Deliverable Templates

Use only the templates relevant to a substantial project. For a short clip, a compact internal checklist is enough.

## 0. Production contract

```markdown
# Production Contract

## Project
- Film/series and episode:
- Edition/runtime:
- Source language and audio track:
- Target language and variant:

## Scope and mode
- Task:
- Standard dialogue / SDH:
- Bilingual or monolingual:
- Machine assistance:

## Locked decisions
- Timing policy:
- Segmentation policy:
- Style guide and reading limits:
- Speaker labels:
- Sound descriptions and music:
- Forced narrative/on-screen text:
- Profanity/rating policy:
- Existing series glossary:
- Prior episodes consulted:

## Deliverables

## Assumptions
```

## 1. Context brief

```markdown
# Context Brief

## Identity
- Working title:
- Original title:
- Year / season / episode:
- Edition and runtime:
- Source language:
- Target language and variant:
- Audience/rating:
- Delivery format:

## Logline

## Dramatic shape
- Opening state:
- Main conflict:
- Midpoint change:
- Climax:
- Ending state:

## Setting
- Period:
- Location:
- Social/political context:
- Fictional rules relevant to dialogue:

## Principal characters
| Character | Role | Relationships | Register | Address rules | Verbal habits | Arc |
|---|---|---|---|---|---|---|

## Scene map
| Scene | Time | Cues | Summary | Characters | New terms |
|---|---:|---:|---|---|---|

## Canonical terminology

## Cultural references

## Songs, poems, and recurring text

## Research questions

## Research sources
| Topic | Source | Finding | Confidence |
|---|---|---|---|
```

## 2. Glossary

Use a tab-separated file:

```tsv
source	preferred_target	part_of_speech	type	first_seen	status	notes
Odysseus	奥德修斯	proper_noun	character	00:05:12	confirmed	Canonical mainland transliteration
Ithaca	伊萨卡	proper_noun	place	00:12:29	confirmed	Do not alternate with 伊塔卡
Zeus' Law	宙斯法则	proper_noun	institution	00:05:16	confirmed	Recurring concept
```

Allowed status:

- `confirmed`
- `provisional`
- `rejected`
- `needs-research`

Do not leave two spellings active for one entity.

## 3. Character voice sheet

```markdown
## Character
- Name:
- Social position:
- Education / profession:
- Regional background:
- Default register:
- Sentence rhythm:
- Politeness:
- Profanity level:
- Humor:
- Typical metaphors:
- Forms of address used:
- Forms of address received:
- Taboo topics:
- Changes under stress:
- Changes after relationship/status shift:
```

Add short target-language examples that represent the voice without copying isolated subtitles out of context.

## 4. Uncertainty log

```markdown
| ID | Cue/time | Issue | Evidence available | Provisional choice | Impact | Resolution needed |
|---|---|---:|---|---|---|---|
| U001 | 01:23:45 | Pronoun from ASR is unclear | Audio muffled; no script | Neutral second-person wording | P2 | Verify against alternate audio |
```

Impact values correspond to the P0-P3 severity scale.

## 5. High-risk cue register

```markdown
| Cue/time | Category | Risk | Current decision | Status | Recheck after |
|---|---|---|---|---|---|
```

Categories include semantic reversals, speaker ambiguity, names and facts, reveals, jokes, lyrics, multilingual dialogue, SDH labels, and on-screen text.

## 6. Series continuity register

```markdown
## Locked terms
| Source term | Locked target | Prior episode | Status | Notes |
|---|---|---|---|---|

## Relationship and address changes

## Callbacks and recurring motifs

## Deliberate changes from prior localization
```

## 7. Correction log for merged versions

```markdown
| Time | Source evidence | Version A | Version B | Chosen meaning | Final text | Reason |
|---|---|---|---|---|---|---|
```

Record only meaningful decisions. Do not create a changelog for every punctuation mark.

## 8. Technical audit summary

```markdown
# Technical Audit

- Input:
- Format:
- Encoding:
- Duration:
- Cues:
- Empty cues:
- Overlaps:
- Zero/negative durations:
- Mean duration:
- Maximum CPS:
- Cues over CPS:
- Lines over length:
- Cues over two lines:
- Unmatched brackets/quotes:
- Duplicate adjacent cues:
- Technical health: PASS / WARN / FAIL
- Target variant consistency:
- Speaker/sound/music conventions:
- Forced-narrative/on-screen-text conventions:

## Critical findings

## Warnings to inspect manually
```

Remember: this is not the semantic translation score.

## 9. QA report

```markdown
# Film Subtitle QA Report

## Scope
- Film/episode:
- Edition:
- Source:
- Target:
- Format:
- Cue count:
- Timing policy:

## Passes completed
- [ ] Context and source audit
- [ ] Full translation pass
- [ ] Blind target-language read
- [ ] Character voice and continuity
- [ ] Adversarial semantic review
- [ ] Production, accessibility, and regression review
- [ ] Technical audit
- [ ] Format/render check
- [ ] Final regression check

## Canonical decisions
- Names:
- Honorifics:
- Recurring terminology:
- Songs:
- Language switching:
- Profanity:
- Machine assistance:
- SDH/accessibility:
- Forced narrative/on-screen text:

## Findings
### P0

### P1

### P2

### P3

## Deliberate tradeoffs

## Unresolved uncertainty

## Technical result

## Score
| Dimension | Weight | Score | Evidence |
|---|---:|---:|---|
| Meaning and fidelity | 30% | | |
| Target-language writing | 20% | | |
| Context and subtext | 15% | | |
| Character voice | 10% | | |
| Timing and readability | 15% | | |
| Terminology and continuity | 5% | | |
| Mechanics | 5% | | |
| **Overall** | **100%** | | |

## Release decision
RELEASE / REVISE / BLOCKED
```

## 10. Final user-facing summary

Keep it concise:

```markdown
Completed: `final.zh-Hans.srt`

- Cue count preserved: 1,905/1,905
- Timing policy: AI timing retained
- QA: two semantic passes, one blind read, technical and ASS render checks
- Key decisions: names standardized; 1,268 cues revised; opening and dedication added by request
- Technical result: no overlaps, empty cues, or invalid timestamps
- Production policy: standard dialogue track; original timing preserved; no machine translation used in final text
- Self-assessed score: 8.8/10
- Remaining limitation: several source lines depend on ASR and were not audio-verified
```

Do not overstate what was checked.

## 11. Naming convention

Recommended output names:

```text
Title.2024.zh-Hans.srt
Title.2024.zh-Hans.en-bilingual.ass
Title.S01E03.zh-Hant.srt
Title.2024.zh-Hans.qa.md
```

Preserve user/project naming when one already exists.

## 12. Final delivery content

Unless the user asks for only a file, report:

- Output path.
- Format and language variant.
- Cue count and whether timing changed.
- QA performed.
- Score and main residual risk.
- Any added/removed non-dialogue cues.

Do not bury a timing change or missing evidence in a long explanation.
