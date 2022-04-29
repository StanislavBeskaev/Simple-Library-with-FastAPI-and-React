#!/bin/bash
echo "Спим 5 секунд, ждём базу"
sleep 5
uvicorn backend.main:app --host 0.0.0.0 --port 8000