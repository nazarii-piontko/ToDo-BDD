#!/usr/bin/env sh

set -e

export APP_BASE_URI=http://app.test/
export SELENIUM_REMOTE=True

if ! pgrep -x dockerd > /dev/null
then
    dockerd > /dev/null 2>&1 &
fi

python3 -m behave
