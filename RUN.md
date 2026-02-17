# How to Run Manim

## Basic Commands

Run the example scene:
```sh
manimgl example_scenes.py OpeningManimExample
```

Run your custom scenes:
```sh
manimgl my_scene.py <SceneName>
```

Or run the video generator:
```sh
python generate_video.py
```

## Useful Flags

- `-w` - Write the scene to a file
- `-o` - Write and open the result
- `-s` - Skip to the end and show final frame
- `-so` - Save final frame as image
- `-n <number>` - Skip to the nth animation
- `-f` - Fullscreen playback

## Examples

```sh
# Write to file and open
manimgl my_scene.py MyScene -o

# Show final frame only
manimgl my_scene.py MyScene -s

# Save final frame as image
manimgl my_scene.py MyScene -so
```
