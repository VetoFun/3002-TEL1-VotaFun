#!/bin/sh
# This hook runs before every commit.

cd web

# Run linting
pnpm lint-staged

# Run tests
pnpm jest --runInBand --detectOpenHandles --forceExit

# Return non-zero exit code if any of the above commands fail
