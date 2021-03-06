// JavaScript code for the Arduino BLE example app.

/**
 * The BLE plugin is loaded asynchronously so the ble
 * variable is set in the onDeviceReady handler.
 */
var ble = null;

/**
 * Called when HTML page has been loled when HTML page has been loaded.
 */
$(document).ready(function () {
	// Adjust canvas size when browser resizes
	$(window).resize(respondCanvas);

	// Adjust the canvas size when the document has loaded.
	respondCanvas();
});

/**
 * Adjust the canvas dimensions based on its container's dimensions.
 */
function respondCanvas() {
	var canvas = $('#canvas');
	var container = $(canvas).parent();
	canvas.attr('width', $(container).width()); // Max width
	//canvas.attr('height', $(container).height() ); // Max height
}

/**
 * Application object that holds data and functions used by the app.
 */
var app =
	{
		// Discovered devices.
		knownDevices: {},

		// Reference to the device we are connecting to.
		connectee: null,

		// Handle to the connected device.
		deviceHandle: null,

		// Handles to characteristics and descriptor for reading and
		// writing data from/to the Arduino using the BLE shield.
		characteristicRead: null,
		descriptorNotification: null,

		// Data that is plotted on the canvas.
		dataPoints: [],

		initialize: function () {
			document.addEventListener(
				'deviceready',
				function () { evothings.scriptsLoaded(app.onDeviceReady) },
				false);
		},

		displayStatus: function (status) {
			if (document.getElementById('status').innerHTML == status)
				return;
			console.log('Status: ' + status);
			document.getElementById('status').innerHTML = status
		},

		displayOutput: function (status) {
			if (document.getElementById('blueoutput').innerHTML == status)
				return;
			console.log('BlueOutput: ' + status);
			document.getElementById('blueoutput').innerHTML = status
		},

		// Called when device plugin functions are ready for use.
		onDeviceReady: function () {
			ble = evothings.ble; // Evothings BLE plugin

			app.startScan();
		},

		startScan: function () {
			app.displayStatus('Scanning...');
			evothings.ble.startScan(
				function (deviceInfo) {
					if (app.knownDevices[deviceInfo.address]) {
						return;
					}
					console.log('found device: ' + deviceInfo.name);
					app.knownDevices[deviceInfo.address] = deviceInfo;
					if (deviceInfo.name == 'Bluno' && !app.connectee) {
						console.log('Found Bluno');
						connectee = deviceInfo;
						app.connect(deviceInfo.address);
					}
				},
				function (errorCode) {
					app.displayStatus('startScan error: ' + errorCode);
				});
		},

		connect: function (address) {
			evothings.ble.stopScan();
			app.displayStatus('Connecting...');
			evothings.ble.connect(
				address,
				function (connectInfo) {
					if (connectInfo.state == 2) // Connected
					{
						app.deviceHandle = connectInfo.deviceHandle;
						app.getServices(connectInfo.deviceHandle);
					}
					else {
						app.displayStatus('Disconnected');
					}
				},
				function (errorCode) {
					app.displayStatus('connect error: ' + errorCode);
				});
		},

		startReading: function (deviceHandle) {
			app.displayStatus('Enabling notifications...');

			// Start reading notifications.
			evothings.ble.enableNotification(
				deviceHandle,
				app.characteristicRead,
				app.onSuccess,
				// function(data)
				// {
				// 	app.displayStatus('Active');
				// 	app.drawLines([new DataView(data).getUint16(0, true)]);
				// },
				app.onBlunoNotificationError,
				// function(errorCode)
				// {
				// 	app.displayStatus('enableNotification error: ' + errorCode);
				// }
				{ writeConfigDescriptor: false }
			);
		},

		onSuccess: function (data) {
			app.displayStatus('Active. Connected to Player #1')
			var blu = app.calculateBlu(data)
			document.getElementById('blueoutput').innerHTML = blu
			if (blu > 100) {
				document.getElementById('adjustment').innerHTML = 'bend more'
			}
			if (blu < 80) {
				document.getElementById('adjustment').innerHTML = 'straighten'
			}
			if (blu < 100 && blu > 80 ) {
				document.getElementById('adjustment').innerHTML = 'perfect!'
			}
			app.drawLines([blu]);
		},

		onBlunoNotificationError: function (errorCode) {
			console.log('enableNotification error: ' + errorCode)
		},

		calculateBlu: function (data) {
			console.log('begin...')
			console.log(data.byteLength)
			var bluno_value = new Uint8Array(data)
			console.log(bluno_value)
			return bluno_value
		},

		drawLines: function (dataArray) {
			var canvas = document.getElementById('canvas');
			var context = canvas.getContext('2d');
			var dataPoints = app.dataPoints;

			dataPoints.push(dataArray);
			if (dataPoints.length > canvas.width) {
				dataPoints.splice(0, (dataPoints.length - canvas.width));
			}

			var magnitude = 200;

			function calcY(i) {
				return (i * canvas.height) / magnitude;
			}

			function drawLine(offset, color) {
				context.strokeStyle = color;
				context.beginPath();
				context.moveTo(0, calcY(dataPoints[dataPoints.length - 1][offset]));
				var x = 1;
				for (var i = dataPoints.length - 2; i >= 0; i--) {
					var y = calcY(dataPoints[i][offset]);
					context.lineTo(x, y);
					x++;
				}
				context.stroke();
			}

			context.clearRect(0, 0, canvas.width, canvas.height);
			drawLine(0, '#f00');
		},

		getServices: function (deviceHandle) {
			app.displayStatus('Reading services...');

			evothings.ble.readAllServiceData(deviceHandle, function (services) {
				// Find handles for characteristics and descriptor needed.
				for (var si in services) {
					var service = services[si];

					for (var ci in service.characteristics) {
						var characteristic = service.characteristics[ci];

						if (characteristic.uuid == '0000dfb1-0000-1000-8000-00805f9b34fb') {
							app.characteristicRead = characteristic.handle;
						}

						for (var di in characteristic.descriptors) {
							var descriptor = characteristic.descriptors[di];

							if (characteristic.uuid == '0000dfb1-0000-1000-8000-00805f9b34fb' &&
								descriptor.uuid == '00002901-0000-1000-8000-00805f9b34fb') {
								app.descriptorNotification = descriptor.handle;
							}
						}
					}
				}

				if (app.characteristicRead && app.descriptorNotification) {
					console.log('RX/TX services found.');
					app.startReading(deviceHandle);
				}
				else {
					app.displayStatus('ERROR: RX/TX services not found!');
				}
			},
				function (errorCode) {
					app.displayStatus('readAllServiceData error: ' + errorCode);
				});
		},

		openBrowser: function (url) {
			window.open(url, '_system', 'location=yes')
		}
	};
// End of app object.

// Initialise app.
app.initialize();