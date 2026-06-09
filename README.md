# OctoPrint-ClockOnConnect

A simple OctoPrint plugin that keeps the printer LCD updated with the current time, including seconds.

By default it sends an `M117` message every second:

    HH:MM:SS

The settings also allow showing the date:

    HH:MM:SS DD.MM.YYYY

The message is centered by padding it to the configured display width. Use `20` for common 20x4 LCDs or `16` for 16x2 LCDs.

![screenshot](screenshot.jpg)

# Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/matejalbert/OctoPrint-ClockOnConnect/archive/master.zip

# Settings

- `Start delay`: waits before the first LCD update after startup or reconnect.
- `Update interval`: how often the clock is refreshed. Use `1` to show live seconds.
- `Display width`: character width used for centering.
- `Show date`: adds the current date after the time.
- `Show message using M70`: uses `M70` instead of `M117` for firmware that supports it.

# Changelog

## [0.1.0] - 2026-06-09
### Added
- Initial ClockOnConnect release forked from ipOnConnect.
- Sends centered clock text to the printer display.
- Optional date display.

## Get Help

If you experience issues with this plugin or need assistance please use the issue tracker by clicking issues above.
