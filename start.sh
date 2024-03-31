#!/bin/bash

# Script para recarregar o daemon, reiniciar o Gunicorn e reiniciar o Nginx
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
