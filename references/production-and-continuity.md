# Production, Accessibility, and Continuity

Use this reference for episodic work, feature films with recurring terminology, machine-assisted translation, SDH/accessibility deliverables, sensitive content, or any job with more than one revision pass. It protects decisions that are easy to lose while working cue by cue.

## 1. Production contract

Before drafting, lock the production decisions in a short contract:

- Project identity: film/series, season/episode, edition, runtime, and language track.
- Task mode: translate, polish, proofread, merge, audit, caption, or format/style only.
- Target language, regional variant, orthography, and punctuation convention.
- Timing policy: preserve timing, authorize retiming, or authorize resegmentation.
- Standard dialogue versus SDH/accessibility subtitle.
- Forced-narrative and on-screen text policy.
- Reading-speed and line-length limits, including any platform override.
- Speaker-label, music, and sound-description conventions.
- Rating, censorship, and profanity policy.
- Existing official localization, series glossary, or prior translated episodes.
- Required deliverables and whether internal QA artifacts are user-facing.

Record the contract even for a small job. If a decision must be inferred, state it as an assumption rather than discovering it late in the file.

## 2. Machine-assisted translation

Machine translation and ASR are evidence or drafts, not finished translation.

When machine assistance is used:

1. Pre-fill a locked glossary and do-not-translate list.
2. Generate or import the machine draft without changing source timing unless authorized.
3. Post-edit scene by scene, not row by row.
4. Audit every high-risk cue for hallucination, omission, speaker misattribution, negation reversal, and invented cultural detail.
5. Compare cue counts and event spans before and after post-editing.
6. Run the complete semantic, voice, and technical QA suite on the final post-edited file.
7. Describe the workflow honestly in the QA report.

Do not describe a machine-post-edited deliverable as an unaided human translation. If user material is confidential, do not send it to an external service unless the user has authorized that use.

## 3. Series and franchise continuity

For sequels, series, franchises, or repeated clients:

- Establish episode order and translate in order whenever possible.
- Import the prior glossary, character voice sheets, and recurring terms before drafting.
- Keep a name authority: character names, titles, honorifics, factions, technology, locations, and nicknames.
- Track relationship changes and forms of address across episodes.
- Preserve callbacks, catchphrases, jokes, songs, and motifs even when they are not plot-critical.
- Record deliberate changes from an earlier localization and explain them in the handoff.
- Do not silently rename an established term to improve one line.

For serialized work, a subtitle is also a continuity artifact. A locally elegant line that breaks a series-level callback is a defect.

## 4. High-risk cue register

Maintain a cue register for passages where an error is expensive:

```markdown
| Cue/time | Category | Risk | Current decision | Status | Recheck after |
|---|---|---|---|---|---|
```

Typical categories:

- Negation, modality, conditionals, and temporal order.
- Speaker attribution and ambiguous pronouns.
- Names, ranks, institutions, measurements, dates, and numbers.
- Reveal, confession, threat, lie, or motive.
- Jokes, wordplay, lyrics, and cultural references.
- Multilingual or deliberately mistranslated dialogue.
- Overlapping speech and rapid action.
- SDH sound descriptions and speaker labels.
- On-screen text that must agree with a spoken line.

Update the register during every pass. Before release, confirm that no unresolved high-risk cue remains unreported.

## 5. SDH and accessibility

SDH subtitles are a different deliverable, not ordinary dialogue with extra labels.

Before drafting, lock:

- Speaker identification convention.
- Sound-description grammar, length, and placement.
- Music and lyric conventions.
- Whether off-screen and on-screen speakers are marked differently.
- Treatment of foreign-language dialogue and interpreters.
- Accessibility style guide, such as a broadcaster or platform guide.

Sound descriptions should:

- Report what is audible and relevant to the story.
- Stay concise and concrete.
- Avoid interpreting emotion as fact when the audio does not support it.
- Use the same syntax and label style throughout.
- Distinguish diegetic music, song lyrics, and instrumental score.
- Not describe sounds that cannot be heard or verified in the supplied media.

Never silently convert an ordinary subtitle into SDH. If accessibility cues are requested, disclose added labels and descriptions in the QA report.

## 6. Forced narratives and on-screen text

Classify each non-dialogue text cue:

- Plot-critical sign.
- Location or time card.
- Phone, computer, document, or broadcast text.
- Title, credit, warning, or archival caption.
- Decorative text.
- Text that duplicates dialogue.

For each class, decide whether it belongs in:

- The normal dialogue track.
- A separate forced-narrative track.
- A typeset overlay.
- No subtitle at all.

Preserve on-screen timing, reading direction, and content hierarchy. Do not invent readable text from an illegible prop. If a translated sign must replace the original graphic, keep the replacement visually plausible and aligned with the production's art direction.

## 7. Sensitive content and cultural safety

Professional subtitle work must preserve the film's dramatic force without amplifying harm.

Check:

- Slurs, hate speech, and demeaning terms.
- Sexual violence, coercion, and consent language.
- Self-harm, suicide, addiction, and medical terminology.
- Legal, military, religious, and ritual language.
- Child endangerment and age-inappropriate content.
- Regional, ethnic, gender, disability, and class references.

Rules:

- Preserve source intensity and in-world meaning; do not sanitize a threat into politeness.
- Do not introduce a modern slur, identity label, or cultural insult absent from the source.
- Use current respectful terminology for real-world communities when the source permits a neutral equivalent.
- Do not add content warnings, hotline information, or censorship unless requested or required by the delivery guide.
- If platform censorship materially changes meaning, disclose it.
- For terms with contested translations, record the chosen equivalent and the rejected alternative.

## 8. Revision and regression control

Do not let a polish pass destroy a correct earlier decision.

For every substantial revision:

1. Preserve the source, first complete draft, post-review draft, and final file.
2. Compare passes with a cue-level diff when available.
3. Review every semantic change, not only newly polished lines.
4. Review unchanged cues that contain a changed name, term, form of address, or callback.
5. Re-run global terminology and orthography checks after any bulk replacement.
6. Re-run technical QA on the final artifact, not on an earlier intermediate.
7. Spot-render changed regions when presentation is part of the deliverable.
8. Keep a meaningful correction log; do not document every punctuation-only edit.

A release candidate is not ready until regressions have been checked and the final file has been parsed independently.

## 9. Final handoff

For a production job, deliver:

- Final subtitle file or files.
- QA report with score and release decision.
- Technical audit.
- Glossary and, when relevant, character voice sheet.
- High-risk cue register and uncertainty log.
- Correction log for merges or series continuity changes.
- Timing and resegmentation policy.
- Accessibility and on-screen-text policy.
- Known limitations and unverified evidence.

Keep internal research notes separate from user-facing deliverables unless the user asks for the full audit trail. Do not bury a timing change, censored passage, machine-assisted workflow, or unresolved ambiguity in generic release language.
