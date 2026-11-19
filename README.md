# Professional Film Subtitle Translation

一个面向 Codex 的专业电影字幕翻译 Skill，用于字幕翻译、校订、评分、双版本合并、背景核查和技术验收。

目标不是逐句直译，而是在可用证据范围内还原电影的对白含义、潜台词、人物语气、文化功能和观看节奏，并通过多轮检查避免“听起来漂亮但意思错了”的译文。

## 核心能力

- 场景级翻译，而不是孤立行翻译。
- 影片版本、人物、专名、历史与文化背景研究。
- 人物声音、称呼、语域、脏话强度和关系变化控制。
- 歌词、双关、俚语、多语言对白、旁白与银幕文字处理。
- 中文电影语言专项规范，重点清除翻译腔。
- 长片分批翻译和全片连续性管理。
- 制作契约、机器辅助译后编辑、剧集连续性、SDH、强制字幕和敏感内容处理。
- 多轮修订的回归控制、高风险字幕登记和最终交接证据。
- AI 字幕与官方字幕时间轴对齐、差异审查与择优合并。
- P0-P3 错误分级、十分制评分和 8.5 分发布门槛。
- SRT、ASS、WebVTT 技术审校与 ASS 宋体样式转换。

## 文件结构

```text
professional-film-subtitle-translation/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- operational-playbook.md
|   |-- research-and-context.md
|   |-- translation-craft.md
|   |-- chinese-film-language.md
|   |-- production-and-continuity.md
|   |-- timing-format-and-style.md
|   |-- quality-rubric.md
|   `-- deliverable-templates.md
|-- scripts/
    |-- subtitle_qa.py
    |-- srt_to_ass.py
    `-- align_subtitle_versions.py
`-- tests/
    |-- test_srt_to_ass.py
    `-- test_subtitle_qa.py
```

## 安装

将仓库克隆到 Codex 的 skills 目录：

```powershell
git clone https://github.com/alexzeng2014/professional-film-subtitle-translation.git `
  "$env:USERPROFILE\.codex\skills\professional-film-subtitle-translation"
```

安装后重新打开 Codex 会话，使技能被重新发现。

调用名称：

```text
$professional-film-subtitle-translation
```

示例：

```text
Use $professional-film-subtitle-translation to translate this subtitle into
Simplified Chinese, research unclear names and cultural references, and run
multi-pass QA before delivery.
```

## 工作流程

1. 检查字幕、视频、音轨、已有译文和交付格式。
2. 确认影片版本、目标语言、受众和平台规范。
3. 研究人物、专名、历史背景和文化引用。
4. 建立术语库、人物语气表、场景地图和不确定性记录。
5. 按场景翻译，再进行电影化压缩。
6. 执行语义、盲读、人物连续性、对抗性和技术检查。
7. 按评分表决定发布、返修或因证据不足而阻塞。

完整规则见 [SKILL.md](SKILL.md)。

## 工具

### 技术审校

```powershell
python scripts/subtitle_qa.py input.srt --language zh --format md
```

检查：

- 空字幕、重叠、负时长、乱序。
- CPS、行宽、行数和过短/过长字幕。
- 重复空格、未闭合引号、异常控制字符。
- ASS 标签混入普通文本。
- 自动识别 CJK 阅读速度档案。
- 简繁混用和中文普通对白句末句号警告。

该工具输出技术健康分，不代表翻译语义分。

### 双版本对齐

```powershell
python scripts/align_subtitle_versions.py version_a.srt version_b.srt `
  --json-out alignment.json --tsv-out alignment.tsv
```

输出匹配、歧义、未匹配时间轴和逐条对照表，便于人工审查 AI、官方或其他字幕版本。

### SRT 转 ASS

```powershell
python scripts/srt_to_ass.py input.srt output.ass `
  --font "SimSun" --font-size 56
```

默认样式为 1920×1080、宋体、白色文字、黑色描边、底部居中，可调整字体、字号、边距、分辨率和颜色。输出固定为 UTF-8 无 BOM、CRLF 换行，并自动校验文件必须以 `[Script Info]` 开头。

ASS/SSA 不应写入 UTF-8 BOM。带 BOM 的文件可能被 Kodi 识别为可选字幕轨，却渲染出零条事件；`subtitle_qa.py` 会把这种文件判为 P1 故障。

## 质量原则

- 保留用户未授权修改的时间轴、分段和原文件。
- 先理解整场戏，再决定字幕。
- 不靠猜测填补无法恢复的 ASR、人物或文化信息。
- 全片专名和术语只能有一个有效版本。
- 优先保护语义、潜台词和人物关系，再处理字面对应。
- 没有完成多轮检查时，不声称达到 8.5 分或“完美”。

## 测试

本项目已用 1905 条中文字幕完成以下验证：

- SRT、ASS、WebVTT 解析与事件计数。
- CPS、行宽、重叠、负时长和引号错误检测。
- 两份包含 1903/1916 条字幕的不同分段版本自动对齐。
- SRT 到 ASS 转换及 FFprobe 字幕流解析。
- ASS 无 BOM、CRLF 和输出文件头回归验证。
- 简繁混用、中文句末句号与自动语言档案检测。
- Skill 结构校验和 Python 语法编译。

## 限制

翻译质量取决于可获得的原字幕、音频、视频和背景资料。对于严重错误的 ASR、缺失剧情上下文、歌词或双关等不可恢复内容，本 Skill 会记录限制，而不是假装客观达到固定分数。
