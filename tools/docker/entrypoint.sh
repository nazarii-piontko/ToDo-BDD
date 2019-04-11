#!/usr/bin/env sh

set -e

export APP_BASE_URI=http://app.test/
export SELENIUM_REMOTE=True
export ARTIFACTS_DIR=/artifacts

dockerd > /dev/null 2>&1 &

python3 -m behave
