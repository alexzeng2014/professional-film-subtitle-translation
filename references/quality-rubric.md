# Subtitle Quality Rubric and Release Gate

Use this rubric for internal revision and user-facing scoring. A score is an informed professional judgment, not a mathematical proof of quality.

## 1. Weighted score

| Dimension | Weight | What it measures |
|---|---:|---|
| Meaning and fidelity | 30 | Accuracy, completeness, logical relations, names and facts |
| Target-language writing | 20 | Naturalness, idiomaticity, rhythm, concision |
| Context and subtext | 15 | Scene comprehension, implication, cultural function |
| Character voice | 10 | Register, relationships, consistency of speech identity |
| Timing and readability | 15 | CPS, line shape, cue duration, presentation |
| Terminology and continuity | 5 | Stable names, terms, motifs, orthography |
| Mechanics | 5 | Encoding, format, punctuation, tags, cue integrity |

Compute:

```text
overall = sum(dimension score * weight) / 10
```

Use one decimal place for the final score. Do not average away a P0 blocker.

## 2. Dimension anchors

### 9.5-10: Exceptional

- No material semantic loss.
- Dialogue could pass as an original target-language screenplay.
- Subtext, voice, rhythm, and cultural function are consistently controlled.
- Technical delivery is clean.

### 9.0-9.4: Premium professional

- Only minor subjective choices or extremely small losses.
- No P0 or P1 issues.
- No meaningful continuity breaks.
- Technically release-ready.

### 8.5-8.9: Strong professional delivery

- Accurate and natural overall.
- Isolated P2 issues remain.
- Some deliberate tradeoffs are documented.
- Does not contain a systemic misunderstanding.

### 8.0-8.4: Good but needs revision

- One or more significant weaknesses: literal passages, inconsistent names, uneven voice, or technical failures.
- May be usable with review, but does not meet the 8.5 release gate.

### 7.0-7.9: Understandable but not release quality

- Frequent awkwardness, uncompressed text, recurring mistranslations, or major continuity issues.
- General plot may survive, but film experience is damaged.

### Below 7.0: Major rework

- Fundamental source, speaker, logic, naming, or readability failures.

## 3. Severity levels

### P0: Blocker

Examples:

- Fabricated plot-critical dialogue.
- Missing an entire major scene or large cue range.
- Wrong film/episode or language.
- Unreadable encoding or corrupted subtitle structure.
- Subtitle file contains no valid cues.

Action: do not release.

### P1: Major

Examples:

- Reversed negation.
- Wrong speaker or addressee in a consequential exchange.
- Agent/patient reversal.
- Mistranslated reveal, threat, confession, or causal relation.
- Names changed inconsistently enough to confuse characters.
- Persistent CPS or clipping problem across material portions.
- Mixed target variants or orthography that makes the deliverable unusable as a locked release.
- A required SDH speaker label, sound description, or forced-narrative cue that materially misleads the viewer.

Action: fix before scoring above 8.5.

### P2: Moderate

Examples:

- Localized passage that sounds translated but remains understandable.
- A lost joke, cultural nuance, or secondary implication.
- Unnecessary explicitation.
- Inconsistent formality in a minor character.
- One or two overlong cues.
- A terminology variant without plot confusion.

Action: correct where feasible; document if a deliberate loss.

### P3: Polish

Examples:

- A line could be sharper but is accurate.
- Minor punctuation or spacing.
- A slightly less natural rhetorical rhythm.
- Optional style improvement.

Action: fix without destabilizing correct material.

## 4. Scoring by dimension

### Meaning and fidelity

Deduct heavily for:

- Wrong speaker/addressee.
- Reversed agency or time.
- Lost negation or modality.
- Invented content.
- Misleading names or cultural facts.
- Dropped reveal.

Do not reward literal wording when meaning is wrong.

### Target-language writing

Assess:

- Would an actor naturally say the line?
- Does it read as Chinese, English, Japanese, etc., rather than as translationese?
- Is compression elegant or merely terse?
- Does it sound like a screenplay rather than a synopsis?

### Context and subtext

Assess:

- Is the speech act correct?
- Is the line too explicit or too vague?
- Does a joke or cultural reference preserve function?
- Does a clever line accidentally introduce a later contradiction?

### Character voice

Assess:

- Can recurring characters be distinguished without their names?
- Does register change when relationships or situations change?
- Are honorifics and address forms coherent?
- Is profanity used as characterization rather than decoration?

### Timing and readability

Automated metrics are supporting evidence, not the entire judgment. Consider:

- CPS and distribution of long cues.
- Minimum and maximum duration.
- Semantic line breaks.
- Visual fit.
- Reading order.
- Whether important information is held on screen long enough.

### Terminology and continuity

Check:

- One spelling per entity.
- Consistent honorifics and titles.
- Species, technology, ranks, institutions, and recurring motifs.
- Simplified/traditional consistency.
- Series or sequel continuity.

### Mechanics

Check:

- Encoding.
- Cue numbering and ordering.
- Timing syntax.
- Overlaps.
- Empty text.
- Tags and styles.
- Format conversion integrity.
- Speaker, sound, music, and forced-narrative conventions required by the selected deliverable.

## 5. Release gates

### 8.5+: professional release

- No P0.
- No P1.
- P2 rate normally at or below 2 per 100 cues.
- All automated critical checks pass.
- All high-risk semantic cues reviewed.
- Production, accessibility, and regression checks completed where relevant.
- Uncertainty disclosed.

### 9.0+: premium release

- No P0, P1, or known P2.
- Strong character voice throughout.
- Low-loss handling of songs, humor, and cultural references.
- Technical and visual QA complete.
- Research uncertainties do not affect plot comprehension.

### 9.5+: exceptional

Reserve for:

- Subtitles that read as authored dialogue.
- Exceptional handling of language play and cultural transfer.
- Complete continuity across a long or serialized work.
- No known material defect.

Do not hand out 9.5 because the file is technically clean or because the translation is merely competent.

## 6. Evidence of effort is not quality

Do not raise a score because:

- Research was extensive.
- Many revisions were made.
- The file is long.
- The translator followed the process.
- The target language is difficult.

Score the delivered subtitle.

## 7. Required reviews before scoring

A score is provisional until:

- A complete target-language read has been performed.
- The semantic-risk cues have been checked.
- Names and terminology have been searched globally.
- The technical script has been run.
- Any format conversion has been parsed and visually checked where relevant.

For feature-length work, include at least two complete revision passes. A short clip may use a lighter process, but the same defect hierarchy applies.

## 8. Score report format

```markdown
# Subtitle Quality Report

## Scope
- Film/episode:
- Source:
- Target:
- Cue count:
- Timing policy:

## Score
| Dimension | Weight | Score | Evidence |
|---|---:|---:|---|
| Meaning and fidelity | 30% | 8.7 | ... |
| Target-language writing | 20% | 9.0 | ... |
| Context and subtext | 15% | 8.6 | ... |
| Character voice | 10% | 8.5 | ... |
| Timing and readability | 15% | 9.0 | ... |
| Terminology and continuity | 5% | 9.2 | ... |
| Mechanics | 5% | 9.5 | ... |
| **Overall** | **100%** | **8.8** | |

## Major findings
- P0:
- P1:
- P2:
- P3:

## Deliberate tradeoffs

## Unresolved uncertainties

## Release decision
```

## 9. Difference between technical score and overall score

`scripts/subtitle_qa.py` reports a technical-health score only. It cannot judge:

- Whether a translation means the right thing.
- Whether a character sounds authentic.
- Whether a joke works.
- Whether an omission is justified.
- Whether a name is canonical.

Never present the technical-health score as the overall translation score.

## 10. Honest scoring

If the evidence is insufficient:

- Score the version you can evaluate.
- State the uncertainty range or cap.
- Do not fill gaps with confidence language.

Example:

> Provisional 8.2/10. The dialogue is generally natural, but the only available source is an ASR transcript. Speaker attribution and several culturally specific lines cannot be verified without audio; the score is capped until those cues are checked.
