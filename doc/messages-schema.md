### Messages schema

#### Broker to watering unit

    {
      "watering_id": "1",
      "creation_date": "2018-10-23T07:28:18.815035+00:00",
      "amount": "10",
      "ttl": "30"
    }
    
* *watering_id* - id of scheduled watering abstraction in central unit
* *creation_date* - date of message/watering creation in iso format with timezone
* *amount* - amount of water to use - in milliliters; it can be float
* *ttl* - period in seconds relative to *creation_date* in which message is valid
 
#### Broker from sensor unit

    {
      "sensor_unit": "s1",
      "type": "temperature",
      "date": "2018-10-23T07:28:18.815035+00:00",
      "value": "10"
    }
    
* *sensor_unit* - id of sensor unit - sender of message
* *type* - type of measurement (e.g. 'temperature', 'humidity')
* *date* - date when measurement was taken
* *value* - value of measurement in scale typical to measurement - it can be float 