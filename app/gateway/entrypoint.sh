#!/bin/bash

gunicorn -w 4 'app:app'
