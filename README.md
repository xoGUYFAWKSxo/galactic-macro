# Galactic Macro

Records mouse and keyboard input system-wide and plays it back with the original timing.
Windows-only, C# / WinForms, .NET 8, no third-party dependencies.

## Download

1. Grab `GalacticMacro-*-win-x64.zip` from the [latest release](https://github.com/xoGUYFAWKSxo/galactic-macro/releases/latest).
2. Extract it to a folder (keep all the files together) and run `GalacticMacro.exe`.

Requires the [.NET 8 Desktop Runtime](https://dotnet.microsoft.com/download/dotnet/8.0) (x64); Windows offers to
install it if it's missing. The exe isn't code-signed, so SmartScreen may warn — choose **More info → Run anyway**.

To run from source instead, see [Build](#build).

## Use

| Action | Button | Default hotkey |
|---|---|---|
| Start / stop recording (or cancel the countdown) | ● Record | **F9** |
| Play / stop playback | ▶ Play | **F10** |

- **Settings…** – change either hotkey (any key, optionally with Ctrl / Alt / Shift) and the
  countdown before recording (0–60 s, default 3; 0 = start immediately). Saved to
  `%APPDATA%\GalacticMacro\settings.json`.
- **Countdown** – a large click-through number appears on the monitor your mouse is on, so you can
  switch to the target app before recording begins. Press the record hotkey again to cancel.
- **Speed ×** – playback speed multiplier (2 = twice as fast).
- **Repeat** – number of loops; `0` loops until you press the play hotkey.
- **Record mouse movement** – untick to record only clicks, wheel and keys (clicks still remember where they happened, so the cursor jumps there).
- **Minimize while recording/playing** – gets the window out of the way.
- **Open… / Save…** – macros are plain JSON (`*.macro.json`), easy to hand-edit.
- **Delete selected** (or the Delete key) removes events; their delay is folded into the next event so timing after them is preserved.
- Starting a new recording when one exists asks whether to append or replace.

Notes:
- The hotkeys are swallowed globally while the app is running so they never leak into the recording.
  Modifier keys pressed as part of a hotkey (e.g. the Ctrl in Ctrl+F9) are stripped from the recording too.
- Clicks and keystrokes aimed at the Galactic Macro window itself are not recorded.
- If playback is stopped mid-macro, any keys or mouse buttons it was holding down are released.
- Windows blocks input into apps running as Administrator from a non-elevated process. To automate an elevated app, run Galactic Macro as Administrator too.
- Games that read raw mouse deltas may not respond to absolute cursor moves.

## Build

Needs the .NET 8 SDK.

```
dotnet run                               # build and launch
dotnet publish -c Release -o publish     # produces publish\GalacticMacro.exe (git-ignored)
```

## License

[MIT](LICENSE)
