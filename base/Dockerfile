# Inherit from an upstream image
FROM pangeo/pangeo-notebook:2026.06.04

# We copy the `environment.yml` file in this repo, only adding in extra
# packages that aren't in our base image.
COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml