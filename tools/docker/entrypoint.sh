#!/usr/bin/env sh

set -e

export APP_BASE_URI=http://app.test/
export SELENIUM_REMOTE=True
export ARTIFACTS_DIR=/artifacts

if pgrep -x dockerd > /dev/null
then
    echo 'Docker daemon is running'
else
    echo 'Starting Docker daemon'
    dockerd > /dev/null 2>&1 &
fi

python3 -m behave
