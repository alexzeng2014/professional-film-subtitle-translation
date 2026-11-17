---
name: professional-film-subtitle-translation
description: Translate, adapt, merge, proofread, score, and technically validate film or television subtitles using context research, scene-level localization, character voice control, consistent terminology, cinematic condensation, and multi-pass QA. Use for subtitle translation or review in SRT, ASS, VTT, or similar timed-text formats, including bilingual comparison and format conversion.
---

# Professional Film Subtitle Translation

## Mission

Produce the best defensible subtitle translation possible for the available evidence. Optimize for the audience's experience of the film, not for word-for-word correspondence.

The target is professional release quality, normally 8.5/10 or higher under [quality-rubric.md](references/quality-rubric.md). Never promise that an arbitrary subtitle can objectively reach a score when audio, video, source scripts, or reliable context are missing. When the evidence is insufficient, flag uncertainty rather than inventing certainty.

## Scope

Use this skill for:

- Translating subtitles or timed transcripts.
- Polishing or proofreading an existing translation.
- Merging machine-generated and human/official subtitles.
- Comparing two subtitle versions.
- Translating songs, narration, titles, and on-screen text in a film context.
- Converting or styling subtitle formats after translation.

Do not use it for unrelated document translation, live captioning with no post-editing, or dubbing scripts unless the user explicitly asks to adapt those tasks to subtitle conventions.

## Non-Negotiable Rules

1. **Preserve what was not authorized to change.** Keep cue timing, cue count, ordering, and source files unless the user permits retiming or resegmentation.
2. **Translate scenes, not isolated rows.** Understand the dramatic beat, speaker intention, power relationship, and surrounding dialogue before deciding a line.
3. **Do not silently guess.** Mark unresolved ASR, speaker, cultural-reference, or wording ambiguities in an uncertainty log.
4. **Use one canonical terminology system.** Character names, places, factions, institutions, honorifics, and recurring phrases must not drift.
5. **Write natural target-language dialogue.** Prefer idiomatic speech over calques. Preserve the effect and subtext, not the original syntax.
6. **Respect the medium.** A subtitle must be readable, timed, and emotionally actable, not merely semantically correct.
7. **Do not fabricate background facts.** Research may inform interpretation, but it must not create content absent from the film or line.
8. **Finish with evidence.** A translation is not ready because the first pass "sounds good." It must survive semantic, voice, continuity, and technical review.
9. **Never overwrite supplied source files.** Write a new output file unless the user explicitly requests in-place editing.
10. **Do not claim absolute perfection.** State the score, residual risks, and unresolved evidence gaps.

## Step 1: Intake and File Audit

Identify and record:

- Source and target languages and target regional variant.
- Film, series, episode, season, year, runtime, and exact edition.
- Delivery format: SRT, ASS, VTT, embedded captions, or another timed-text format.
- Whether timing is locked and whether resegmentation is allowed.
- Audience, rating, platform, and any style guide.
- Required output: monolingual, bilingual, translated only, or review report.
- Available evidence: video, audio, transcript, existing subtitles, glossary, script, cast list, or production notes.
- Rights and usage constraints supplied by the user.

Use these defaults only when the user has not specified otherwise:

- For a Chinese-speaking user requesting Chinese subtitles, use Simplified Chinese.
- Preserve all timestamps and cue boundaries.
- Produce a new file beside the source with a clear language or version suffix.
- Keep the source-language subtitle in a separate review artifact, not mixed into a monolingual deliverable.
- Do not add translator credits or promotional text.

Ask a question only when the missing information is both material and unavailable through reasonable inference. Otherwise make a conservative assumption and disclose it.

Audit source quality:

| Grade | Evidence | Required response |
|---|---|---|
| A | Verified transcript or authoritative source subtitle plus media/context | Translate normally with full QA |
| B | Clean subtitle or transcript with reliable text but incomplete context | Research and verify uncertain readings |
| C | ASR or machine translation with known errors | Check audio/media wherever possible; log residual uncertainty |
| D | Severely corrupted, incomplete, or context-free text | Do not present as release-ready without qualification |

If media is available, inspect at least the opening, difficult scenes, songs, overlapping dialogue, endings, and any scene implicated by a translation uncertainty. Do not rely on a subtitle file alone when audio or video can resolve a plot-critical ambiguity.

## Step 2: Build Film Context

Read [research-and-context.md](references/research-and-context.md). Then build a compact working bible:

- Logline and major dramatic arc.
- Scene or sequence map.
- Character list with relationships, power dynamics, register, verbal habits, and forms of address.
- Canonical names and terms.
- Historical, geographic, religious, institutional, and cultural references that affect meaning.
- Recurring jokes, catchphrases, songs, poems, and motifs.
- Known ambiguities and research questions.

For a long film, series episode, or large batch, use scene-indexed batches rather than translating the entire file as unrelated rows. Keep the glossary, voice bible, and uncertainty log open across batches.

### Research rules

Research when any of the following can change meaning:

- Exact production, edition, remake, director's cut, localization, or episode.
- Real people, historical events, military ranks, institutions, laws, or religions.
- Regional slang, dialect, insults, honorifics, or forms of address.
- A character's official localized name or a term used across sequels/series.
- Songs, poems, nursery rhymes, quotations, or literary allusions.
- A scene whose subtitle text appears internally inconsistent.
- Multilingual dialogue, language barriers, or deliberate mistranslation in the story.

Prefer user-provided materials, then primary/authoritative sources, then high-quality reference works. Treat fan wikis, forums, and unofficial subtitles as leads, not proof. Cross-check consequential facts. Record source links or short source notes in the internal context brief.

Do not insert research into dialogue as exposition. Research should help infer the correct intent and terminology.

## Step 3: Prepare Translation Assets

Before drafting, create the following in a temporary work area when the task is substantial:

1. `context-brief.md` using [deliverable-templates.md](references/deliverable-templates.md).
2. `glossary.tsv` for names, places, titles, institutions, and recurring terms.
3. `character-voices.md` for register and address rules.
4. `uncertainty-log.md` for unresolved source or research issues.
5. `qa-report.md` for pass-by-pass findings and final score.

For short clips, this can remain a compact internal checklist. For a feature-length subtitle, maintain it as persistent state so later cues do not contradict earlier choices.

## Step 4: Translate by Scene

Read [translation-craft.md](references/translation-craft.md) and, for Chinese targets, [chinese-film-language.md](references/chinese-film-language.md).

Use this sequence:

1. **Understand the scene.** Read all cues in the scene, including adjacent cues needed for context. Identify who speaks, to whom, why, what changes, and what remains unsaid.
2. **Draft the full meaning.** Resolve pronouns, ellipsis, shared knowledge, tense, aspect, negation, scope, and implied objects before compressing.
3. **Localize the speech act.** Preserve the effect: command, plea, joke, threat, evasion, flirtation, ritual formula, deliberate awkwardness, etc.
4. **Apply character voice.** Keep each character's vocabulary, rhythm, politeness, profanity, and address forms distinguishable.
5. **Compress for subtitles.** Remove redundancy while preserving plot information, implication, and tone.
6. **Fit timing and line shape.** Condense wording first, then use permitted resegmentation. Never shrink text or increase reading speed to conceal a translation problem.
7. **Update the glossary and uncertainty log immediately.** Resolve conflicts at the whole-film level.

For each cue, protect in this order:

1. Plot-critical meaning and logical relations, especially negation, modality, agency, and temporal order.
2. Intent, implication, emotional force, and relationship dynamics.
3. Character voice and register.
4. Cultural or stylistic effect.
5. Surface syntax and word-level correspondence.

The hierarchy does not permit inventing a new meaning. If a joke or reference cannot survive literally, preserve its dramatic function and note any unavoidable loss.

## Step 5: Timing, Segmentation, and Presentation

Read [timing-format-and-style.md](references/timing-format-and-style.md).

Default constraints:

- Keep original timing unless the user authorizes changes.
- Prefer one or two lines per cue.
- Break lines at clause or semantic boundaries, never between a numeral and its unit or between a name and its title.
- For Chinese, target roughly 9-12 characters per second and 16-18 Hanzi per line unless the platform guide or established style requires otherwise.
- Keep a subtitle on screen long enough to read without lingering unnaturally.
- Use speaker dashes only when needed to disambiguate turn-taking.
- Use italics and sound effects sparingly and consistently.
- Preserve intentional repetition, stuttering, unfinished sentences, and overlapping speech when they carry performance.

If a platform style guide exists, it overrides these defaults. If the supplied subtitle systematically violates readability limits, report the issue and ask or make a clearly disclosed conservative adjustment depending on the user's instruction.

## Step 6: Multi-Pass QA

Read [quality-rubric.md](references/quality-rubric.md). For every substantial project, run all applicable passes; do not stop after a single proofread.

### Pass A: Source and semantic audit

- Compare high-risk cues against source text, audio, and context.
- Check names, numbers, dates, ranks, locations, negation, pronoun reference, and causal logic.
- Back-translate a sample of difficult cues and all cues where compression or ambiguity is high.
- Add or repair information omitted by segmentation.

### Pass B: Blind target-language read

- Read the target subtitle without looking at the source.
- Mark places that sound written, explanatory, repetitive, over-complete, anonymous, or unlike spoken film dialogue.
- Check that scenes are emotionally coherent and that each speaker remains recognizable.

### Pass C: Character voice and continuity

- Compare each recurring character's lines across the whole work.
- Verify address forms, honorifics, catchphrases, profanity level, education/class markers, and relationship changes.
- Check timeline, reveal order, and terms established across sequels or episodes.

### Pass D: Subtitle mechanics

Run:

```bash
python scripts/subtitle_qa.py input.srt --format md
```

Review every critical issue. Use `--language zh` for Chinese-target defaults, or specify custom limits where a platform guide applies.

### Pass E: Format and render verification

- Parse the final file with the actual target format.
- Check ASS style names, fonts, margins, alignment, encoding, and event count.
- Render representative normal, short, long, song, and two-speaker cues over video when possible.
- Verify that text does not clip, overlap other subtitles, or sit unreadably low/high.

### Pass F: Adversarial review

Search specifically for:

- Reversed pronouns or speaker attribution.
- Missing or doubled negation.
- Wrong subject/object of an action.
- Literal idioms that do not work in the target language.
- Overcompression that removes a reveal or motive.
- Explanatory additions that are not in the film.
- Name variants, inconsistent accents, and mixed orthography.
- Cues where a translation sounds polished but changes the speech act.

For a feature-length project, run at least two complete translation-review passes and one complete technical pass. Between passes, preserve the previous artifact so improvements can be diffed and regressions detected.

## Step 7: Score and Release Gate

Use the rubric in [quality-rubric.md](references/quality-rubric.md). Score semantics, naturalness, context/subtext, voice, timing/readability, terminology, and mechanics.

Do not report 8.5+ unless:

- There are no open P0 or P1 issues.
- P2 issues are rare and documented.
- All technical checks pass.
- Uncertain source passages are either resolved or clearly disclosed.
- The final target text has been read as a complete work, not only cue by cue.

If the score is below 8.5 for reasons that can be fixed, revise and repeat the relevant passes. If it is below 8.5 because evidence is missing, state that limitation instead of inflating the score.

## Step 8: Merge or Compare Versions

When the user supplies multiple subtitle versions:

1. Inspect each version's timing, segmentation, source completeness, fluency, and known errors.
2. Align versions with:

   ```bash
   python scripts/align_subtitle_versions.py version_a.srt version_b.srt --json-out alignment.json --tsv-out alignment.tsv
   ```

3. Treat alignment as evidence, not an automatic winner. Different cue boundaries can make text appear mismatched.
4. For each divergence, classify the difference as:
   - one version correct;
   - both incomplete;
   - segmentation mismatch;
   - dictionary/name variant;
   - stylistic alternative;
   - unresolved source ambiguity.
5. Prefer timing from the version the user specifies.
6. Rebuild meaning at scene level when one version combines or splits cues.
7. Keep a correction log for consequential choices.
8. Run the full QA suite on the merged result, not merely a comparison of both inputs.

## Format Conversion

When output needs ASS styling, use:

```bash
python scripts/srt_to_ass.py input.srt output.ass --font "SimSun" --font-size 56
```

The default style is a conservative 1920x1080 cinema subtitle: white Song-style text, black outline, bottom-center placement. Override font, size, margins, resolution, outline, and shadow for the target platform. Do not change translation text during format conversion unless explicitly asked.

## Deliverables

Provide the final subtitle first. For complex work, also provide a concise QA report containing:

- Input and output file paths.
- Kept/changed cue counts and timing policy.
- Key terminology and voice decisions.
- QA passes performed.
- Automated technical results.
- Final self-assessed score by dimension.
- Remaining uncertainties or evidence gaps.
- Any formatting/style assumptions.

Keep the report factual. Do not turn it into marketing copy.

## Working Defaults

- Target audience: general adult film audience unless specified.
- Register: natural contemporary film language unless the setting requires period/formal speech.
- Names: follow an established official localization; otherwise use the most widely recognized standard and lock it globally.
- Punctuation: follow target-language subtitle convention; omit final full stops for ordinary Chinese declarative subtitles.
- Numbers: preserve exact meaning; write in the form easiest to read at speed.
- Profanity: match intensity, taboo level, and character voice rather than translating word by word.
- Songs: mark as lyrics only when they function as songs; translate for singability only when singability is required.
- Ambiguity: preserve ambiguity when it is intentional; resolve it only when grammar or context makes the meaning clear.

## Reference Routing

- Complex end-to-end workflow or long feature: [operational-playbook.md](references/operational-playbook.md).
- Background research, edition identification, names, and cultural facts: [research-and-context.md](references/research-and-context.md).
- Semantic translation, voice, humor, lyrics, and difficult dialogue: [translation-craft.md](references/translation-craft.md).
- Chinese target-language style and common translationese: [chinese-film-language.md](references/chinese-film-language.md).
- CPS, line breaks, subtitle timing, ASS and platform mechanics: [timing-format-and-style.md](references/timing-format-and-style.md).
- Scoring, severity levels, and release gates: [quality-rubric.md](references/quality-rubric.md).
- Working documents and QA report templates: [deliverable-templates.md](references/deliverable-templates.md).

## Script Routing

- Technical audits and readability checks: `scripts/subtitle_qa.py`.
- SRT-to-ASS conversion and style setup: `scripts/srt_to_ass.py`.
- Two-version time alignment for comparison or merge: `scripts/align_subtitle_versions.py`.
