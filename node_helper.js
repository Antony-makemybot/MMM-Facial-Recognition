const NodeHelper = require("node_helper");
const { spawn } = require("child_process");

module.exports = NodeHelper.create({
    start: function() {
        console.log("Starting module helper: " + this.name);
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "START_RECOGNITION") {
            this.startFaceRecognition();
        }
    },

    startFaceRecognition: function() {
        const pythonProcess = spawn("python3", ["modules/MMM-Facial-Recognition/face_recognition.py"]);
        
        pythonProcess.stdout.on("data", (data) => {
            const result = data.toString().trim();
            if (result.startsWith("USER:")) {
                const user = result.split(":")[1];
                this.sendSocketNotification("USER_LOGGED_IN", { user });
            } else if (result === "LOGOUT") {
                this.sendSocketNotification("USER_LOGGED_OUT");
            }
        });

        pythonProcess.stderr.on("data", (data) => {
            console.error(`stderr: ${data}`);
        });

        pythonProcess.on("close", (code) => {
            console.log(`child process exited with code ${code}`);
        });
    }
});
