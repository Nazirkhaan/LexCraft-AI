# Render's Docker runtime requires a root file named exactly `Dockerfile`.
# This keeps the local workflow 100% Podman-based: the real build instructions
# live in the OCI-standard `Containerfile`, which Podman reads natively and
# this file simply forwards to.
#
#   Local (Podman, unchanged):  podman build -t lexcraft -f Containerfile .
#   Render:                     builds via this Dockerfile -> Containerfile

FROM Containerfile
