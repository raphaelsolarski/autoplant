#!/bin/bash

docker run -d --rm -p 15672:15672 -p 5672:5672 rabbitmq:3.7.8-management