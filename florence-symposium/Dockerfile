FROM base_image

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml