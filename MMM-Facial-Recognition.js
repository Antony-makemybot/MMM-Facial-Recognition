Module.register("MMM-Facial-Recognition", {
    defaults: {
        useDNN: true,
        interval: 5,  // How often to run recognition (seconds)
        logoutDelay: 15,
        users: ["John", "Jane"],
        welcomeMessage: true
    },

    start: function() {
        this.loggedInUser = null;
        this.sendSocketNotification("START_RECOGNITION");
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "USER_LOGGED_IN") {
            this.loggedInUser = payload.user;
            this.showUserModules(payload.user);
            if (this.config.welcomeMessage) {
                this.sendNotification("SHOW_ALERT", {message: "Welcome, " + payload.user + "!", timer: 3000});
            }
        }

        if (notification === "USER_LOGGED_OUT") {
            this.loggedInUser = null;
            this.hideAllModules();
        }
    },

    showUserModules: function(user) {
        MM.getModules().enumerate((module) => {
            if (module.data.classes.includes(user) || module.data.classes.includes("everyone")) {
                module.show(1000);
            } else {
                module.hide(1000);
            }
        });
    },

    hideAllModules: function() {
        MM.getModules().enumerate((module) => {
            if (!module.data.classes.includes("default")) {
                module.hide(1000);
            }
        });
    }
});
