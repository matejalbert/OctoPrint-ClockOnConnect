$(function() {
    function ClockOnConnectSettingsViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];
        self.settings = self.settingsViewModel.settings;

        self.defaults = {
            enabled: true,
            delay: 0,
            updateDuringPrint: true,
            displayWidth: 20,
            updateInterval: 1,
            command: "M117",
            displayTime: 2,
            timeFormat: "%H:%M:%S",
            showDate: false,
            dateFormat: "%d.%m.%Y",
            separator: " ",
            prefix: "",
            suffix: "",
            alignment: "center",
            uppercase: false
        };

        self.resetAll = function() {
            var settings = self.settingsViewModel.settings.plugins.ClockOnConnect;

            $.each(self.defaults, function(key, value) {
                if (ko.isObservable(settings[key])) {
                    settings[key](value);
                }
            });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: ClockOnConnectSettingsViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_ClockOnConnect_form"]
    });
});
