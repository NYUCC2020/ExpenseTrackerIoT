# Simulated Devices

Scripts simulating real devices to send generated data to our MQTT server.

## Deployment

- The docker image for the fake device is manually built and pushed to IBM private registry.
```
docker build -t us.icr.io/nyu-cc/expense-tracker-iot-fake-device:latest .
docker push us.icr.io/nyu-cc/expense-tracker-iot-fake-device:latest
```

- The docker image is deployed to the IBM K8s manually. Now it is sending message to our MQTT server every 1 hour.
```
kubectl apply -f deploy.yml
```

