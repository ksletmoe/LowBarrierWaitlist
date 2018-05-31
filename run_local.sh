#!/usr/bin/env bash
set -e

export FLASK_APP='low_barrier_waitlist'
export FLASK_ENV='development'

flask run "$@"
