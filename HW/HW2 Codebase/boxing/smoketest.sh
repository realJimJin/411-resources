#!/bin/bash

BASE_URL="http://localhost:5001/api"
ECHO_JSON=false

while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

check_health() {
  echo "Checking health..."
  curl -s "$BASE_URL/health" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."; exit 1
  fi
}

check_db() {
  echo "Checking DB connection..."
  curl -s "$BASE_URL/db-check" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Database is healthy."
  else
    echo "Database check failed."; exit 1
  fi
}

create_boxer() {
  echo "Creating boxer..."
  response=$(curl -s -X POST "$BASE_URL/create-boxer" \
    -H "Content-Type: application/json" \
    -d '{"name": "Ali", "weight": 150, "height": 70, "reach": 75, "age": 30}')
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxer created."
  else
    echo "Failed to create boxer."; exit 1
  fi
}

get_leaderboard() {
  echo "Getting leaderboard..."
  response=$(curl -s "$BASE_URL/leaderboard")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Leaderboard retrieved."
    [ "$ECHO_JSON" = true ] && echo "$response" | jq .
  else
    echo "Failed to get leaderboard."; exit 1
  fi
}

run_fight() {
  echo "Running a fight..."
  response=$(curl -s -X POST "$BASE_URL/fight")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Fight executed."
    [ "$ECHO_JSON" = true ] && echo "$response" | jq .
  else
    echo "Fight failed."; exit 1
  fi
}

check_health
check_db
create_boxer
create_boxer
get_leaderboard
run_fight

echo "All smoketests passed!"