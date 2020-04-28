FROM python:3.7-alpine

# Uncommit and modify the followings when you build and deploy locally
# If you're using kubectl, you can define these ENV variables in your YAML file

# ENV HOST "184.173.52.86"
# ENV PORT 30002
# ENV TOPIC "home_device"
# ENV DEVICE_ID "0"
# ENV INTERVAL "10"

# Create working folder and install dependencies
WORKDIR /fake-devices
COPY . /fake-devices
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "fake-device.py"]
