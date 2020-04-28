FROM python:3.7-alpine

# Install packages
RUN apk update && apk add bash
RUN apk --no-cache add mosquitto mosquitto-clients

WORKDIR /aws_mqtt_conf
COPY aws_mqtt_conf/. /aws_mqtt_conf/

ENV BRIDGE_CAFILE /aws_mqtt_conf/rootCA.crt
ENV BRIDGE_CERTFILE /aws_mqtt_conf/cert.crt
ENV BRIDGE_KEYFILE /aws_mqtt_conf/private.key

RUN sed -i 's:$BRIDGE_CAFILE:'"$BRIDGE_CAFILE"':g' bridge.conf
RUN sed -i 's:$BRIDGE_CERTFILE:'"$BRIDGE_CERTFILE"':g' bridge.conf
RUN sed -i 's:$BRIDGE_KEYFILE:'"$BRIDGE_KEYFILE"':g' bridge.conf

# Expose MQTT port
EXPOSE 1883

ENV PATH /usr/sbin:$PATH

# Create working folder and install dependencies
WORKDIR /subscriber
COPY subscriber/. /subscriber/
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /scripts
COPY start.sh /scripts

CMD ["bash", "start.sh"]
