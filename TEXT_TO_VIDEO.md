# Text-to-Video Multi-Pass LLM System

Generate 3Blue1Brown-style educational videos from text descriptions using AI.

## Overview

This system uses a multi-stage LLM pipeline to create Manim animations:

1. **Planner LLM** - Converts your description into a structured scene plan
2. **Coder LLM** - Generates executable Manim code from the plan
3. **Checker LLM** - Validates code quality and spatial layout
4. **Auto-Fix** - Automatically fixes rendering errors (up to 3 attempts)

## Quick Start

```bash
# Basic usage
python generate_video.py "Explain the Pythagorean theorem"

# From a text file
python generate_video.py description.txt

# With verbose output (see plan and code)
python generate_video.py "derivative of x squared" -v

# Multi-pass mode (higher quality, slower)
python generate_video.py "integral calculus" --multi-pass

# Custom output directory
python generate_video.py "linear algebra" -o my-video

# Don't auto-play after rendering
python generate_video.py "probability" --no-play
```

## Pipeline Modes

### Single-Pass Pipeline (Default)
**Flow:** Planner → Coder ↔ Checker → Render

- Faster (~30-60 seconds)
- Generates entire scene at once
- Checker validates before rendering
- Auto-fixes errors if render fails

```bash
python generate_video.py "explain derivatives"
```

### Multi-Pass Pipeline (Premium Quality)
**Flow:** Planner → Per-Act Code Gen with Checker Loop → Collate → Render

- Slower but higher quality
- Generates code act-by-act
- Each act validated before moving to next
- Up to 3 attempts per act
- Better for complex topics

```bash
python generate_video.py "quantum mechanics basics" --multi-pass
```

## Command-Line Options

```
python generate_video.py <description> [options]

Arguments:
  description          Text description or path to .txt file

Options:
  -v, --verbose        Show plan and generated code
  --multi-pass         Use multi-pass pipeline (slower, higher quality)
  -o, --output DIR     Custom output directory name
  --no-play            Skip auto-playing video after render
```

## How It Works

### 1. Planning Stage
The Planner LLM breaks your topic into pedagogical acts:
- Title card
- Teaching acts (each 7-10 seconds)
- Closing summary

Each act specifies:
- Objects to create (axes, shapes, text)
- Animations and timing
- Spatial layout (no overlaps)
- Teaching goal

### 2. Code Generation
The Coder LLM converts the plan to runnable Manim code:
- Uses `manimlib` (3Blue1Brown's version)
- Text only (no LaTeX)
- Precise timing and positioning
- Clean transitions between acts

### 3. Quality Checking
The Checker LLM validates:
- **Spatial:** No overlapping text/shapes
- **Temporal:** Proper updater cleanup
- **API:** Correct method usage
- **Pedagogical:** Clear teaching flow

### 4. Auto-Fix Loop
If rendering fails:
1. Send error to LLM
2. Generate fixed code
3. Retry (up to 3 attempts)

## Example Workflow

```bash
# 1. Generate from description
python generate_video.py "Show how the derivative of x² equals 2x" -v

# Output shows:
# [1/3] Generating scene (Planner → Coder → Checker)...
#   [1/3] Planning scene...
#   [2/3] Generating code from plan...
#   [3/3] Checking code (round 1/2)...
#     ✓ Code approved!
#
# [2/3] Rendering (attempt 1/3)...
#   Render succeeded! Video: output/20260216_143022/video.mp4
#
# [3/3] Opening video...
```

## Output Structure

```
output/
└── 20260216_143022/           # Timestamped directory
    ├── plan.txt               # The generated plan
    ├── scene_001.py           # Generated Manim code
    └── video.mp4              # Final rendered video
```

## Environment Setup

Required environment variable:
```bash
# Add to .env file
XAI_API_KEY=your_xai_api_key_here
```

The system uses Grok (xAI's LLM) via OpenAI-compatible API.

## Tips for Best Results

### Writing Good Descriptions

**Good:**
- "Explain the Pythagorean theorem with a visual proof"
- "Show how the tangent line becomes the derivative"
- "Demonstrate the area under a curve as a Riemann sum"

**Bad:**
- "Make a math video" (too vague)
- "Explain all of calculus" (too broad)
- "Show me integration and differentiation and limits and series" (too many topics)

### When to Use Multi-Pass

Use `--multi-pass` for:
- Complex mathematical concepts
- Topics requiring multiple visual build-ups
- When you need highest quality

Use default single-pass for:
- Quick prototypes
- Simple explanations
- Faster iteration

### Verbose Mode

Always use `-v` when developing:
```bash
python generate_video.py "topic" -v
```

This shows:
- The generated plan
- The complete code
- Checker feedback
- Fix attempts

## Troubleshooting

### "XAI_API_KEY not set"
```bash
# Create .env file with:
echo "XAI_API_KEY=your_key_here" > .env
```

### Render fails after 3 attempts
- Check the error in `scene_00X.py` files
- Try simplifying your description
- Use `-v` to see what code was generated

### Video doesn't open
- Use `--no-play` and open manually from `output/`
- Check that video file was created

### Poor quality output
- Try `--multi-pass` mode
- Be more specific in your description
- Check the plan (with `-v`) and refine your prompt

## Architecture

```
generate_video.py
    ├── text_to_video/cli.py        # Pipeline orchestration
    ├── text_to_video/llm.py         # LLM client (Grok)
    ├── text_to_video/prompt.py      # System prompts
    ├── text_to_video/renderer.py    # Manim execution
    └── text_to_video/player.py      # Video playback
```

## Advanced Usage

### Custom Prompts
Edit `text_to_video/grok_prompt.md` to customize:
- Teaching style
- Visual preferences
- Timing guidelines
- Color schemes

### Pipeline Customization
Edit `text_to_video/cli.py`:
- Change max retry attempts
- Adjust checker rounds
- Modify multi-pass act count

## Target Video Specs

- Duration: 35-45 seconds
- Acts: 4-6 scenes
- Pacing: 80% animation, 20% pauses
- Resolution: 1920x1080 (default Manim)
- Style: 3Blue1Brown aesthetic

## Examples

### Basic Math
```bash
python generate_video.py "visualize sin and cos on unit circle"
```

### Calculus
```bash
python generate_video.py "show limits approaching a point" --multi-pass
```

### Linear Algebra
```bash
python generate_video.py "demonstrate matrix multiplication geometrically" -v
```

### Probability
```bash
python generate_video.py "explain Bayes theorem with a medical test example"
```
