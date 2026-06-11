# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import threading
import time

class ClockOnConnectPlugin(octoprint.plugin.SettingsPlugin,
						octoprint.plugin.AssetPlugin,
						octoprint.plugin.StartupPlugin,
						octoprint.plugin.ShutdownPlugin,
						octoprint.plugin.EventHandlerPlugin,
						octoprint.plugin.TemplatePlugin):

	def __init__(self):
		self._timer = None
		self._timer_lock = threading.Lock()
		self._shutting_down = False
						
	##~~ SettingsPlugin mixin
	
	def get_settings_defaults(self):
		return dict(
			enabled=True,
			delay=0,
			updateDuringPrint=True,
			displayWidth=20,
			updateInterval=1,
			command="M117",
			displayTime=2,
			timeFormat="%H:%M:%S",
			showDate=False,
			dateFormat="%d.%m.%Y",
			separator=" ",
			prefix="",
			suffix="",
			alignment="center",
			uppercase=False
		)

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self._schedule_clock_update(self._get_int_setting("delay", 0), allow_zero=True)

	##~~ AssetPlugin mixin

	def get_assets(self):
		return dict(
			js=["js/ClockOnConnect.js"]
		)
						
	##~~ StartupPlugin mixin
	
	def on_after_startup(self):	
		self._shutting_down = False
		self._schedule_clock_update(self._get_int_setting("delay", 0), allow_zero=True)

	##~~ ShutdownPlugin mixin

	def on_shutdown(self):
		self._shutting_down = True
		self._cancel_clock_update()
		
	##-- EventHandler mixin 
	
	def on_event(self, event, payload):
		if event in ("Connected", "ConnectivityChanged", "PrintStarted", "PrintDone", "PrintFailed", "PrintCancelled"):
			self._schedule_clock_update(self._get_int_setting("delay", 0), allow_zero=True)
			
	##~~ TemplatePlugin mixin

	def get_template_configs(self):
		return [dict(type='settings', custom_bindings=True, template='ClockOnConnect_settings.jinja2')]

	##~~ Utility functions

	def _schedule_clock_update(self, delay=None, allow_zero=False):
		if self._shutting_down:
			return

		if delay is None:
			delay = self._get_int_setting("updateInterval", 1)
		delay = max(0 if allow_zero else 1, int(delay))

		with self._timer_lock:
			if self._timer is not None:
				self._timer.cancel()
			self._timer = threading.Timer(delay, self._send_clock_and_reschedule)
			self._timer.daemon = True
			self._timer.start()

	def _cancel_clock_update(self):
		with self._timer_lock:
			if self._timer is not None:
				self._timer.cancel()
				self._timer = None

	def _send_clock_and_reschedule(self):
		try:
			self.send_clock()
		finally:
			self._schedule_clock_update()

	def send_clock(self):
		if not self._printer or not self._printer.is_operational():
			return
		if not self._settings.get_boolean(["enabled"]):
			return
		if not self._settings.get_boolean(["updateDuringPrint"]) and self._printer.is_printing():
			return

		message_text = self._format_clock_message()
		if self._settings.get(["command"]) == "M70":
			message = "M70 P{0} ({1})".format(self._settings.get(["displayTime"]), message_text)
		else:
			message = "M117 {0}".format(message_text)

		self._printer.commands(message)
		self._logger.info("ClockOnConnectPlugin: " + message)

	def _format_clock_message(self):
		parts = [self._strftime_setting("timeFormat", "%H:%M:%S")]
		if self._settings.get(["showDate"]):
			parts.append(self._strftime_setting("dateFormat", "%d.%m.%Y"))

		separator = self._settings.get(["separator"])
		if separator is None:
			separator = " "
		message = separator.join(parts)
		message = "{0}{1}{2}".format(
			self._settings.get(["prefix"]) or "",
			message,
			self._settings.get(["suffix"]) or ""
		)
		if self._settings.get_boolean(["uppercase"]):
			message = message.upper()

		display_width = self._get_int_setting("displayWidth", 20)
		alignment = self._settings.get(["alignment"])
		if display_width > len(message) and alignment == "center":
			message = message.center(display_width)
		elif display_width > len(message) and alignment == "right":
			message = message.rjust(display_width)
		elif display_width > len(message):
			message = message.ljust(display_width)
		return message

	def _strftime_setting(self, key, fallback):
		value = self._settings.get([key]) or fallback
		try:
			return time.strftime(value)
		except (TypeError, ValueError):
			return time.strftime(fallback)

	def _get_int_setting(self, key, fallback):
		try:
			return int(self._settings.get([key]))
		except (TypeError, ValueError):
			return fallback

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			ClockOnConnect=dict(
				displayName="ClockOnConnect",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="matejalbert",
				repo="OctoPrint-ClockOnConnect",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/matejalbert/OctoPrint-ClockOnConnect/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "ClockOnConnect"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ClockOnConnectPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

