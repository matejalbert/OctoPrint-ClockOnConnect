# OctoPrint-ClockOnConnect

ClockOnConnect is an OctoPrint plugin that keeps the printer LCD updated with a customizable clock message.

It can show the current time, optionally add the date, format the text for your display width, and choose whether the clock should continue updating while a print is running.

![ClockOnConnect settings screenshot](screenshot.jpg)

## Features

- Sends the current time to the printer display through `M117` or `M70`.
- Optional date display.
- Configurable time and date formats using Python `strftime` syntax.
- Custom prefix, suffix, and time/date separator.
- Left, center, or right alignment with configurable display width.
- Optional uppercase output.
- Configurable start delay and refresh interval.
- Option to pause LCD clock updates during active prints.
- Reset all settings button in the OctoPrint settings dialog.

## Fork Notice

ClockOnConnect is a fork of [OctoPrint-ipOnConnect](https://github.com/jneilliii/OctoPrint-ipOnConnect).
The original plugin showed OctoPrint's IP address on the printer display. This fork changes the behavior to show a customizable clock instead.

## Setup

Install through OctoPrint's Plugin Manager with this URL:

```text
https://github.com/matejalbert/OctoPrint-ClockOnConnect/archive/master.zip
```

After installation, restart OctoPrint and open:

```text
Settings > Plugins > ClockOnConnect
```

## Settings

`Enable LCD clock updates` turns the plugin output on or off.

`Keep updating while printing` controls whether the clock keeps sending LCD messages during a print. Disable it if your firmware, slicer start G-code, filament change flow, or other plugins use LCD messages while printing.

`Start delay` waits before the first display update after OctoPrint starts, reconnects, or a print state changes.

`Update interval` controls how often the clock is refreshed. Use `1` second for live seconds, or a longer interval if you only show hours and minutes.

`Command` selects the LCD message command:

- `M117` is the common Marlin-style LCD message command.
- `M70` is supported by some firmwares and can use a display timeout.

`M70 display time` sets the timeout used in the generated `M70 P... (...)` command.

`Time format` and `Date format` use Python `strftime` formatting. Examples:

```text
%H:%M:%S      23:59:08
%H:%M         23:59
%d.%m.%Y      11.06.2026
%Y-%m-%d      2026-06-11
```

`Prefix`, `Suffix`, and `Time/date separator` let you build messages like:

```text
Time 23:59
23:59 | 11.06.2026
[23:59:08]
```

`Display width` and `Alignment` control padding for displays such as 16x2 or 20x4 LCDs.

`Reset all` restores the settings fields to plugin defaults. Click OctoPrint's normal save button afterward to store the reset values.

## Default Output

By default the plugin sends an `M117` message every second:

```gcode
M117       23:59:08
```

The text is centered for a 20-character display.

## Changelog

## 0.2.0 - 2026-06-11

### Added

- Added an option to keep clock updates enabled or disabled during active prints.
- Added a master enable switch for LCD clock updates.
- Added configurable command selection for `M117` and `M70`.
- Added custom time format, date format, separator, prefix, suffix, alignment, display width, and uppercase options.
- Added a Reset all button in plugin settings.
- Added automatic rescheduling after settings are saved.

### Changed

- Expanded the settings UI and README documentation.

## 0.1.0 - 2026-06-09

### Added

- Initial ClockOnConnect release forked from ipOnConnect.
- Sends centered clock text to the printer display.
- Optional date display.

## Get Help

Please use the GitHub issue tracker if you run into problems or want to suggest improvements. 
