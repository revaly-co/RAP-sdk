"""SDK version constant.

0.0.0.dev0 is a placeholder: pipeline stage 5 stamps the real semver at release
time from the python/v* tag (pipeline-and-release.md). The dev suffix is one more
guard against an accidental registry upload while publish is embargoed.
"""

SDK_VERSION = "0.0.0.dev0"
