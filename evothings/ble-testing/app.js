// Scan for all services.
evothings.ble.startScan(
    function(device)
    {
        console.log('startScan found device named: ' + device.name);
    },
    function(errorCode)
    {
        console.log('startScan error: ' + errorCode);
    }
);

// Scan for specific service (Eddystone Service UUID).
evothings.ble.startScan(
    function(device)
    {
        console.log('startScan found device named: ' + device.name);
    },
    function(errorCode)
    {
        console.log('startScan error: ' + errorCode);
    },
    { serviceUUIDs: ['0000feaa-0000-1000-8000-00805f9b34fb'] }
);