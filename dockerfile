FROM python:3.8
# WORKDIR /Docker2/emddocker
RUN apt-get update
ADD emsdocker/ems_v3.py ems_v3.py

# install dependencies that are required.

RUN pip install paho-mqtt
RUN pip install influxdb_client
RUN pip install pandas
CMD ["python3","./ems_v3.py"]
