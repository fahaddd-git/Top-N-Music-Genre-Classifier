#!/usr/bin/env zsh

declare -a project_directories=(
  "utilities"
  "etl-service"
  "neural-network"
  "prediction-api"
)

if ! command -v poetry >/dev/null 2>&1; then
  echo "Error: poetry is not installed"
  echo "Please install poetry from https://python-poetry.org/"
  exit 1
fi

declare -a failed=()
for project in $project_directories; do
  pushd $project
  echo "* Running poetry install in $project..."
  poetry install
  [ $? -ne 0 ] && failed+=($project)
  repeat 2 echo
  popd
done

# report failures
[ ${#failed[@]} -ne 0 ] && echo "\n\nError installing dependencies:"
for project in $failed; do
  echo "    poetry install failed for $project"
done

# initialize or upgrade db
echo "* Running alembic migration..."
pushd "utilities"
poetry run alembic upgrade head
if [ $? -ne 0 ]; then
  echo "Alembic failed to upgrade sqlite database"
else
  echo "Alembic upgrade successful"
fi
popd
