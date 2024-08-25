# ./scripts/run-tests.sh
# Start the app-test service in the docker-compose.yml
# and run the pytest command

pytest_args=$*
docker compose -f docker-compose.yml run --rm app-test $pytest_args
docker compose -f docker-compose.yml --profile test down --volumes
