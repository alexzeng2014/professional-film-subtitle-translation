# Timing, Format, and Style

Translation quality is constrained by reading time. A semantically accurate line can still fail if it appears too briefly or covers the image.

## 1. Hierarchy of timing constraints

Use:

1. User or platform specification.
2. Final delivery format constraints.
3. Original timing when locked.
4. Conservative cinematic defaults below.

Do not change timing solely because a draft translation is too long. Condense first.

## 2. Reading speed

Reading speed is language- and audience-dependent. When no platform guide exists:

| Target | Suggested maximum | Notes |
|---|---:|---|
| Chinese adults | 9-12 Hanzi/second | Prefer lower for dense exposition |
| Chinese children | 7-9 Hanzi/second | Shorter lines and simpler syntax |
| Latin-script adults | 15-20 characters/second | Platform guidance may be stricter |
| Fast action/comedic banter | Lower than normal | Performance and cuts reduce reading time |

Do not treat a single CPS number as proof of quality. Check:

- Distribution of long lines, not only the average.
- Whether key phrases sit at the start or end of a rapidly replaced cue.
- Whether the viewer is also reading signs or subtitles in multiple positions.
- Whether the line contains unfamiliar names or numbers.

## 3. Line length and number of lines

Without a platform specification:

- Use at most two lines per cue.
- For Chinese, target 16-18 Hanzi per line.
- For long lines, aim to keep both lines roughly balanced.
- Break after a clause, before a conjunction, or between independent thoughts.
- Do not break:
  - A number and its unit.
  - A person's name and title.
  - A modifier from the word it directly modifies if the result is confusing.
  - A pair of quotation marks across lines without reason.
  - A two-character word.
- Avoid a single-word last line when a balanced break is possible.

For 1920x1080 ASS, a 27-Hanzi line may fit horizontally but still be too fast or visually heavy. Fit is not the same as readability.

## 4. Cue duration and gaps

Conservative defaults:

- Minimum duration: about 0.8 seconds for a short but complete cue.
- Maximum duration: about 7 seconds unless the platform permits more.
- Minimum gap: about 2 frames or 80 ms where supported.
- Do not leave a cue visible long after the speech ends unless it is an intentional narrative card.

Short cues under 0.5 seconds may be acceptable for a one-word shout within a rapid exchange, but must be checked in context.

## 5. Synchronization

- Start close to the audible or visual cue, not distractingly early.
- End after the line is understood, not necessarily at the last consonant.
- Preserve overlap where two conversations matter.
- Do not shift a cue into the next speaker's turn.
- With on-screen text, preserve the text's appearance and disappearance.
- With songs, align by phrase rather than lagging behind the vocal.

## 6. Speaker changes

In a single cue containing two speakers:

- Use a dash at the beginning of each speaker line.
- Keep speakers in reading order.
- Do not merge lines when it prevents the viewer from identifying the turn.

Example:

```text
- 让他试。
- 来吧。
```

If a cue already has one line per speaker, do not add names unless names are necessary for comprehension.

## 7. Italics, sound effects, and labels

Use conventions consistently:

- Italics for off-screen narration or a second language only if the platform uses that convention.
- Square-bracket or descriptive sound cues only for SDH/accessibility tracks, not ordinary dialogue.
- Do not italicize every emotional line.
- Do not add labels such as `[愤怒地]`; performance is visible or audible.
- Preserve a repeated sound-effect convention across the film.

## 8. SRT

SRT characteristics:

- Millisecond timestamps.
- Simple sequence number, timing, text.
- No reliable native style specification.
- Usually limited to plain text and basic HTML-like tags.

SRT validation should check:

- Sequential cue numbering or identify intentional non-sequential IDs.
- Valid timing syntax.
- No overlaps unless explicitly intended.
- No empty cues.
- Text encoding.
- No accidental HTML or ASS tags.

## 9. ASS/SSA

ASS supports styles, positioning, fonts, and effects. Do not use complex effects merely because they are available.

### Conservative 1080p cinema style

```text
[Script Info]
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

Default style:
Font: SimSun (宋体) or platform-approved serif
Size: 54-58
Primary: white
Outline: black, approximately 2-2.5
Shadow: subtle, no glow
Alignment: bottom center
Margins: 70-90 left/right, 50-70 bottom
```

ASS font requirements:

- Use an installed font or embed/provide the font when the platform supports it.
- Confirm the actual family name, not only a marketing name.
- Avoid a font that looks correct in an editor but falls back in the final player.
- Do not use all-caps, negative letter spacing, or heavy outlines for Chinese cinema subtitles.
- For 720p, scale size and margins proportionally or let the player scale.

### Typesetting

Translate signs and titles only when:

- They carry meaning.
- They are legible enough to read.
- The user requests typesetting or the platform requires it.

Preserve position, reading direction, and content hierarchy. Do not invent text from a blurry sign.

## 10. WebVTT and other formats

For VTT:

- Verify whether cue identifiers and settings are required.
- Preserve speaker tags and styling only if the delivery expects them.
- Convert timing precision accurately.
- Do not leave SRT sequence numbers in VTT.

For embedded MP4/Matroska subtitles:

- Confirm codec and language tags.
- Verify default/forced flags.
- Verify character encoding.
- Render the actual stream, not only the standalone subtitle.

## 11. Bilingual layout

When two languages are required:

1. Choose source/target order.
2. Use a consistent style for each language.
3. Keep total display height within the safe area.
4. Do not allow source text to force awkward target breaks.
5. Reduce both languages before shrinking font.
6. Keep the primary language visually dominant.

Common options:

- Target above source.
- Source above target.
- Target primary white, source smaller and secondary.

Follow the user's platform convention.

## 12. Safe area

Avoid:

- Faces and important props.
- Lower-third broadcast graphics.
- Burned-in titles.
- The extreme bottom edge of the frame.
- Multiple subtitle blocks competing for attention.

For theatrical films, leave visual breathing room. The audience should read without hunting.

## 13. Retiming policy

If retiming is authorized:

- Preserve the source cue as a reference.
- Use a mapping table between old and new cues.
- Split overlong cues only at semantic boundaries.
- Merge only when the speaker and meaning remain unambiguous.
- Check total film duration and audio alignment afterward.
- Re-run overlap, CPS, and duration checks.
- Spot-check audio at all changed boundaries.

If retiming is not authorized, do not silently fix timing. Report the problem and offer a separate retimed version.

## 14. Format QA commands

Technical audit:

```bash
python scripts/subtitle_qa.py final.srt --language zh --format md
```

ASS conversion:

```bash
python scripts/srt_to_ass.py final.srt final.ass \
  --font "SimSun" --font-size 56 --margin-v 58
```

When FFmpeg and libass are available, render representative frames:

```bash
ffmpeg -v error -f lavfi -i "color=c=black:s=1920x1080:r=25:d=2" \
  -vf "setpts=PTS+125/TB,ass=final.ass" \
  -frames:v 1 preview.png
```

Inspect:

- Font fallback.
- Line clipping.
- Vertical position.
- Outline legibility over light and dark backgrounds.
- Longest line and two-speaker cue.

## 15. Final technical gate

- Cue count is as expected.
- No zero/negative durations.
- No unintended overlaps.
- No empty text.
- No invalid encoding or control characters.
- No stale ASS tags in SRT.
- CPS and line lengths are within the chosen guide.
- Speaker labels are consistent.
- ASS styles parse and render.
- Final file opens in at least one independent parser/player.
