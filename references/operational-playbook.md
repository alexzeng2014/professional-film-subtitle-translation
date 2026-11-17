# Operational Playbook

Use this reference for feature-length films, episodic television, multi-version merges, or any job large enough that continuity can be lost during translation.

## 1. Workspace and version control

Use a task-specific workspace:

```text
work/
|-- source/
|   |-- source.srt
|   `-- reference.srt
|-- analysis/
|   |-- context-brief.md
|   |-- glossary.tsv
|   |-- character-voices.md
|   `-- uncertainty-log.md
|-- drafts/
|   |-- pass1.srt
|   |-- pass2.srt
|   `-- pass3.srt
|-- qa/
|   |-- technical-report.md
|   |-- semantic-audit.md
|   `-- qa-report.md
`-- final/
    `-- title.target-language.srt
```

Never make the first draft the only artifact. Preserve at least:

- The original source.
- The first complete translation draft.
- The post-review draft.
- The final delivered file.

When editing a source-like deliverable, produce a new file unless overwrite was explicitly requested.

## 2. Job classification

Classify the request before translating:

| Mode | Typical instruction | Primary risk |
|---|---|---|
| Translate | "Translate this subtitle" | Misreading source or context |
| Polish | "Make this Chinese more natural" | Improving style while introducing semantic drift |
| Proofread | "Check this subtitle" | Catching only surface errors |
| Merge | "Combine these versions" | Segmentation mismatch and accidental duplication |
| Audit/score | "Rate this subtitle" | Confusing technical cleanliness with translation quality |
| Convert/style | "Make this ASS" | Accidentally changing text or timing |
| Raw captioning | "Transcribe and translate this film" | ASR error, speaker attribution, overlap |

Do not silently convert one mode into another. For a proofreading request, report unusually large structural problems before resegmentation. For a format-conversion request, do not rewrite dialogue unless asked.

## 3. Evidence inventory

Record every available artifact:

- Video and audio quality.
- Subtitle files in all languages.
- Forced-narrative or SDH tracks.
- Transcript, screenplay, shooting script, or published screenplay.
- Cast list, episode synopsis, press kit, and official glossary.
- User's preferred terminology or previous translations.
- Platform style guide.

When versions disagree, establish a truth hierarchy:

1. User-supplied authoritative script or glossary.
2. Audio or verified transcript for the exact edition.
3. Official or professionally localized subtitle for the same edition.
4. Official distributor materials and authoritative language references.
5. High-quality reviews, interviews, and production notes.
6. Fan wikis and community subtitles as leads only.

The hierarchy is not absolute. A polished subtitle can still contain an error, and a fan glossary can preserve an official name that a database lacks.

## 4. Exact-version lock

Before research or translation, lock the identity:

- Film or series title in original language.
- Year, season, episode, and episode title.
- Theatrical, extended, director's-cut, remastered, broadcast, streaming, or localized release.
- Runtime and key scene differences.
- Remake versus original.
- Dubbing track versus original-language performance.

If the exact edition cannot be established, avoid changing names or interpreting scenes that differ between editions. Record the limitation.

## 5. Scene map

Create a scene map instead of dividing only by cue number.

```markdown
| Scene | Time range | Cue range | Summary | Characters | Terms introduced | Notes |
|---|---:|---:|---|---|---|---|
| S01 | 00:00:00-00:02:15 | 1-22 | Prologue and song | Narrator | Troy, Ithaca | Lyric register |
| S02 | 00:02:15-00:06:40 | 23-96 | Suitors in the hall | Penelope, Telemachus | Zeus' Law | Status insults |
```

A scene boundary is a change in time, place, speaker group, dramatic objective, or topic. Keep adjacent scenes visible while translating a scene because setup and payoff often cross the boundary.

## 6. Batch translation

For large subtitle files:

1. Translate one scene or 100-250 cues at a time.
2. Read a small overlap before and after the batch.
3. Keep the same glossary and character voice files open.
4. Log every new recurring term immediately.
5. Resolve conflicts before moving to the next batch.
6. After every 10-15 minutes of film, skim all previous recurring names and phrases.
7. At the end of each act, perform a continuity read.

Do not translate each batch as if it were a separate film. A character who uses formal address in act one must not become casual in act two without an in-story reason.

## 7. First complete pass

Optimize this pass for semantic completeness:

- Decode every line before compressing it.
- Identify speaker and addressee.
- Mark uncertain pronouns, referents, and ASR words.
- Translate idiom and speech act rather than surface wording.
- Capture repeated language and deliberate motifs.

Do not spend the first pass endlessly polishing isolated lines. Get a complete, coherent draft, then revise globally.

## 8. Second pass: blind target-language read

Read the draft without the source file visible.

Mark:

- Paragraph-style subtitles that no actor could naturally speak.
- Explanatory information that belongs in the image, not dialogue.
- Lines that all use the same rhythm and vocabulary.
- Abrupt register changes.
- Unnecessary subject pronouns.
- Repeated sentence openings.
- Jokes that have to be decoded.
- Lines that sound morally or emotionally stronger/weaker than the scene.

Then compare each changed line to the source and surrounding cues. A natural line that changes the story is not an improvement.

## 9. Third pass: adversarial source audit

Look for high-severity semantic errors:

- Missing or doubled negation.
- Wrong speaker or addressee.
- Agent/patient reversal.
- Before/after reversal.
- Singular/plural confusion that changes a reveal.
- Literal translation of an idiom.
- Missing sarcasm, threat, taboo, or romantic implication.
- A subtitle that resolves an intentional ambiguity.

Prioritize cues with:

- Very short source lines but long target lines.
- Negation, modals, conditionals, and tense.
- Pronouns without explicit nouns.
- Names and titles.
- Numbers and military/political terminology.
- Song lyrics, jokes, and cultural references.

## 10. Resegmentation and retiming

Only change cue boundaries or timestamps when allowed.

Before changing:

- Check whether a downstream player or platform uses the original timing.
- Preserve cue IDs or time ranges in a mapping file.
- Avoid creating flashes shorter than the platform minimum.
- Do not split a line merely because the translator wrote too much; condense first.
- Do not merge two speakers unless the format explicitly supports multiple speakers within one cue.

After changing:

- Confirm no overlaps.
- Confirm total content is neither duplicated nor lost.
- Re-run technical QA.
- Spot-render changed regions.

## 11. Multi-version merge

### Preparation

Label versions by trust and purpose, for example:

- Version A: machine translation with stronger timing.
- Version B: official translation with weaker segmentation.

### Alignment

Run:

```bash
python scripts/align_subtitle_versions.py version_a.srt version_b.srt \
  --json-out alignment.json --tsv-out alignment.tsv
```

Inspect unmatched and ambiguous groups, especially where one version combines two source sentences into one cue.

### Adjudication

For each group:

1. Read surrounding scene.
2. Reconstruct the source meaning from the best available evidence.
3. Compare each version clause by clause.
4. Choose the stronger semantic content.
5. Re-express it in natural target-language rhythm.
6. Keep the user-preferred timing.
7. Record a major change in the correction log.

Do not concatenate both translations. That commonly produces duplication, overexplanation, and impossible reading speed.

### Quality control of a merge

- Check every unmatched cue individually.
- Search for doubled words caused by overlap.
- Check whether one version omitted a whole clause.
- Check names and forms of address against the glossary.
- Run a blind read of the merged result.
- Run the full technical audit.

## 12. Format conversion

Translation and presentation are separate operations.

When converting:

- Parse, do not regex-edit blindly, when practical.
- Preserve event count unless retiming/resegmentation is authorized.
- Preserve line breaks and intentional italics.
- Convert timestamps according to the target format's precision.
- Verify font availability or provide a fallback.
- Re-open the output in a parser and count events.
- Render representative frames when styling matters.

Use `scripts/srt_to_ass.py` for a conservative ASS starting style, then adjust to the user's platform.

## 13. Stop and escalation conditions

Pause or qualify delivery when:

- The wrong film or episode may have been supplied.
- The subtitle is severely incomplete.
- The audio cannot be heard well enough to resolve plot-critical lines.
- Multiple versions conflict on facts that cannot be researched.
- The user asks for a translation claim that contradicts the source.
- Required platform specifications are unknown and materially alter the deliverable.
- Continuing would require overwriting or destroying a user file.

When stopping, state exactly what evidence would resolve the issue.

## 14. Final release checklist

- Source and target files are clearly named.
- Target variant and orthography are consistent.
- All cues are present and ordered.
- No accidental duplication or omission.
- Timing policy is documented.
- Glossary and names are locked.
- Character voice changes are intentional.
- P0/P1 issues are zero.
- Technical script passes.
- Representative cues render correctly.
- Final score is evidence-based.
- Uncertainty log is summarized honestly.
