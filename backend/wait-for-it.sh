#!/usr/bin/env bash

# wait-for-it.sh
# Автор: Maria

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port to be available..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "$host:$port is available. Executing command..."

exec $cmd

