# ExpenseTrackerIoT
IoT feature for Expense Tracker App

## MQTT Endpoint(Deployed to IBM K8s)
- HOST = '184.173.52.86'
- PORT = 30002

## Run with Docker
```
cd ExpenseTrackerIoT
docker build -t expense-tracker-subscriber . 
docker run --rm -it --name subscriber -p 1883:1883 expense-tracker-subscriber
```

## Home Device Message Format
Currently we only support a ON/OFF event from smart home device. The message format is as follows:
```
{
    "action_timestamp": <current timestamp>,
    "action": <"ON"|"OFF">,
    "device_id": "0"
}
```

## A simple console mqtt publish to interactive with the IoT message collector
```
mosquitto_pub -h <MQTT_HOST> \
-p <MQTT_PORT> -q 1 -d \
-t <TOPIC>  -i clientid1 \
-m "<json_message>"
```
An example:
```
mosquitto_pub -h localhost \
-p 1883 -q 1 -d \
-t home_device -i clientid1 \
-m "{\"action_timestamp\": 1588052501.667447, \"action\":\"OFF\", \"device_id\":\"0\"}"
```

## More examples
See scripts under **fake-devices** foler
