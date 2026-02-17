# OUTPUT FORMAT

Your response MUST use these exact delimiters:

```
=== PLAN ===
TITLE: <title>

ACT 1: <name> (~Xs)
- Mobjects: <what's created>
- Animations: <step-by-step>
- Voice-over cue: <what a narrator would say>

ACT 2: ...

CLOSING (~Xs)
- <how it ends>

TOTAL: ~Xs
=== CODE ===
from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        ...
```

The CODE section must contain ONLY runnable Python. No markdown fences, no prose.
