FROM base_image

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml

# workshop_agent and sci_units live inside the VISS repo. nbgitpuller pulls it to
# ~/viss-agentic-ai-workshop-tsos-2026 (the link generator must set that targetPath).
# They are imported from the checkout, not installed, so participants' edits take effect.
ENV PYTHONPATH=/home/jovyan/viss-agentic-ai-workshop-tsos-2026/workshop_agent/src:/home/jovyan/viss-agentic-ai-workshop-tsos-2026/blocks/01-landscape/demo/starter/src

# Fail the build if the combined hackathon + VISS environment is broken.
RUN ${NB_PYTHON_PREFIX}/bin/python -c "import psrchive, sncosmo, boto3, s3fs, redback, argus_sim, convening2026, pint.toa, litellm, dotenv, statsmodels, scipy, numpy, pandas; assert int(pandas.__version__.split('.')[0]) >= 3, pandas.__version__; print('pandas', pandas.__version__, 'numpy', numpy.__version__)"
RUN ${NB_PYTHON_PREFIX}/bin/python -c "import importlib.metadata as m; print({d: m.version(d) for d in ('slicersim', 'wcc-etc', 'esc-etc', 'wcc-sim', 'lazuli-exo', 'argus-sim', 'convening2026-release')})" \
 && command -v tempo2

# pip (litellm, lazuli, ...) can drift away from what conda installed, e.g. a newer botocore than
# aiobotocore/s3fs allow, which breaks S3 access at runtime while imports still succeed. Fail on
# `uv pip check` problems outside the 4 already present in the stock pangeo-notebook image.
RUN ! ${NB_PYTHON_PREFIX}/bin/uv pip check --python ${NB_PYTHON_PREFIX}/bin/python 2>&1 \
      | grep '^The package' \
      | grep -vE '`(xmip|lonboard|pygobject|pycairo)`'