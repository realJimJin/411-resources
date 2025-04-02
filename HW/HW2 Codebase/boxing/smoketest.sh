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
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

check_db() {
  echo "Checking DB connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Database is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

create_boxer() {
  echo "Creating boxer..."
  response=$(curl -s -X POST "$BASE_URL/add-boxer" \
    -H "Content-Type: application/json" \
    -d '{"name": "Ali", "weight": 150, "height": 70, "reach": 75, "age": 30}')

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer created successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to create boxer."
    echo "$response"
    exit 1
  fi
}

get_boxer_by_name() {
  echo "Retrieving boxer by name..."
  response=$(curl -s -X GET "$BASE_URL/get-boxer-by-name/Ali")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve boxer."
    echo "$response"
    exit 1
  fi
}

# Run tests
check_health
check_db
create_boxer
get_boxer_by_name

echo "All smoketests passed successfully! "