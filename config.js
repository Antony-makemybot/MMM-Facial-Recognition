let config = {
	address: "localhost",
	port: 8080,
	ipWhitelist: ["127.0.0.1", "::ffff:127.0.0.1", "::1"],

	language: "en",
	locale: "en-US",
	timeFormat: 24,
	units: "metric",

	modules: [
        {
			module: 'MMM-Face-Reco-DNN',
			config: {
				logoutDelay: 15000,  // Logout 15 seconds after user is not detected anymore
				checkInterval: 2000,  // Face detection every 2 seconds
				noFaceClass: 'noface',  // Class to apply when no face is detected
				unknownClass: 'unknown',  // Class to apply when an unknown face is detected
				knownClass: 'known',  // Class to apply when a known face is detected
				defaultClass: 'default',  // Default class for modules
				everyoneClass: 'everyone',  // Show for everyone (any face detected)
				alwaysClass: 'always',  // Always show these modules
				cascade: 'modules/MMM-Face-Reco-DNN/model/haarcascade_frontalface_default.xml',
				encodings: 'modules/MMM-Face-Reco-DNN/model/encodings.pickle',
				brightness: 0,
				contrast: 0,
				rotateCamera: -1,
				method: 'dnn',
				detectionMethod: 'hog',
				animationSpeed: 0,
				pythonPath: null,
				welcomeMessage: true,
				extendDataset: false,
				dataset: 'modules/MMM-Face-Reco-DNN/dataset/',
				tolerance: 0.6,
				multiUser: 0,
				resolution: [640, 480],
				processWidth: 300,
				outputmm: 0,
				debug: 0,  // Disable debugging
			}
		},
		{
			module: 'MMM-SimpleLogo',
			position: 'top_left',
			classes: "always",  // Visible for everyone
			config: {}
		},
		{
			module: "alert",
			classes: "always",  // Always visible
		},
		{
			module: "updatenotification",
			position: "top_bar",
			classes: "known",  // Visible for everyone
		},
		{
			module: "clock",
			position: "top_left",
			classes: "always",  // Show for known and unknown faces
		},
		{
			module: "calendar",
			header: "Indian Holidays",
			position: "top_left",
			classes: "known",  // Show for known and unknown faces
			config: {
				calendars: [
					{
						fetchInterval: 7 * 24 * 60 * 60 * 1000,
						symbol: "calendar-check",
						url: "https://ics.calendarlabs.com/33/3549fd93/India_Holidays.ics"
					}
				]
			}
		},
				{
			module: "compliments",
			position: "lower_third",
			classes: "Akshay",  // Only show for known faces
			config: {
				compliments: {
					anytime: [
						"Hey there Handsome!",
					],
					morning: [
						"Good morning!",
						"Enjoy your day!",
					],
					afternoon: [
						"You're a star, Akshay!",
						"You're looking great!",
					],
					evening: [
						"Fantastic job today, Akshay!",
						"Enjoy your evening!",
					]
				},
				updateInterval: 30000,
				fadeSpeed: 4000,
			}
		},
				{
			module: "compliments",
			position: "lower_third",
			classes: "Sona",  // Only show for known faces
			config: {
				compliments: {
					anytime: [
						"Hey there, gorgeous!",
					],
					morning: [
						"Good morning!",
						"Enjoy your day!",
					],
					afternoon: [
						"You're amazing, Sona!",
						"You're looking great!",
					],
					evening: [
						"Keep up the great work, Sona!",
						"Enjoy your evening!",
					]
				},
				updateInterval: 30000,
				fadeSpeed: 4000,
			}
		},
		{
			module: "compliments",
			position: "lower_third",
			classes: "Antony",  // Only show for known faces
			config: {
				compliments: {
					anytime: [
						"Hey there Antony!",
					],
					morning: [
						"Good morning!Antony",
						"Enjoy your day!Antony",
					],
					afternoon: [
						"Hello, Antony!",
						"Antony,You're looking great!",
					],
					evening: [
						"Wow, you look fantastic!",
						"Enjoy your evening!",
					]
				},
				updateInterval: 30000,
				fadeSpeed: 4000,
			}
		},
				{
			module: "compliments",
			position: "lower_third",
			classes: "unknown",  // Only show for known faces
			config: {
				compliments: {
					anytime: [
						"Hey there Stranger!",
					],
					morning: [
						"Good morning!Stranger",
						"Enjoy your day!Stranger",
					],
					afternoon: [
						"Hello, Stranger!",
						"Stranger,You're looking great!",
					],
					evening: [
						"Wow, you look fantastic!",
						"Enjoy your evening!",
					]
				},
				updateInterval: 30000,
				fadeSpeed: 4000,
			}
		},
		{
			module: "weather",
			position: "top_right",
			classes: "known",  // Show for known and unknown faces
			config: {
				weatherProvider: "openmeteo",
				type: "current",
				lat: 10.00758306891496,
				lon: 76.35566169991439
			}
		},
		{
			module: "weather",
			position: "top_right",
			header: "Weather Forecast",
			classes: "known",  // Show for known and unknown faces
			config: {
				weatherProvider: "openmeteo",
				type: "forecast",
				lat: 10.00758306891496,
				lon: 76.35566169991439
			}
		},
		{
			module: "newsfeed",
			position: "bottom_bar",
			classes: "known",  // Show for known and unknown faces
			config: {
				feeds: [
					{
						title: "BBC",
						url: "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
					}
				],
				showSourceTitle: true,
				showPublishDate: true,
				broadcastNewsFeeds: true,
				broadcastNewsUpdates: true
			}
		}
	]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") { module.exports = config; }
