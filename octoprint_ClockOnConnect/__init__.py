# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import threading
import time

class ClockOnConnectPlugin(octoprint.plugin.SettingsPlugin,
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
			delay=0,
			showDate=False,
			displayWidth=20,
			updateInterval=1,
			useM70=False,
			displayTime="2"
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
		if event in ("Connected", "ConnectivityChanged", "PrintDone", "PrintFailed"):
			self._schedule_clock_update(self._get_int_setting("delay", 0), allow_zero=True)
			
	##~~ TemplatePlugin mixin

	def get_template_configs(self):
		return [dict(type='settings', custom_bindings=False, template='ClockOnConnect_settings.jinja2')]

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

		message_text = self._format_clock_message()
		if self._settings.get(["useM70"]):
			message = "M70 P{0} ({1})".format(self._settings.get(["displayTime"]), message_text)
		else:
			message = "M117 {0}".format(message_text)

		self._printer.commands(message)
		self._logger.info("ClockOnConnectPlugin: " + message)

	def _format_clock_message(self):
		parts = [time.strftime("%H:%M:%S")]
		if self._settings.get(["showDate"]):
			parts.append(time.strftime("%d.%m.%Y"))

		message = " ".join(parts)
		display_width = self._get_int_setting("displayWidth", 20)
		if display_width > len(message):
			message = message.center(display_width)
		return message

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

