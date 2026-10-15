FROM base_image

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml

# workshop_agent and sci_units live inside the VISS repo. nbgitpuller pulls it to
# ~/viss-agentic-ai-workshop-tsos-2026 (the link generator must set that targetPath).
# They are imported from the checkout, not installed, so participants' edits take effect.
ENV PYTHONPATH=/home/jovyan/viss-agentic-ai-workshop-tsos-2026/workshop_agent/src:/home/jovyan/viss-agentic-ai-workshop-tsos-2026/blocks/01-landscape/demo/starter/src

# Fail the build if the combined hackathon + VISS environment is broken.
RUN ${NB_PYTHON_PREFIX}/bin/python -c "import psrchive, sncosmo, boto3, s3fs, redback, argus_sim, convening2026, pint.toa, litellm, dotenv, statsmodels, scipy, numpy, pandas; assert int(pandas.__version__.split('.')[0]) >= 3, pandas.__version__; print('pandas', pandas.__version__, 'numpy', numpy.__version__)"
RUN ${NB_PYTHON_PREFIX}/bin/python -c "import numba, slicersim, wcc_etc, esc_etc, wcc_phot, wcc_sim, lazuli_exo, jaxoplanet; print('numba', numba.__version__)" \
 && command -v tempo2

# pip (litellm, lazuli, ...) can drift away from what conda installed, e.g. a newer botocore than
# aiobotocore/s3fs allow, which breaks S3 access at runtime while imports still succeed. Fail on
# `uv pip check` problems outside the 4 already present in the stock pangeo-notebook image.
# Fail closed: require proof that uv ran ("Checked N packages"), and only ignore a problem whose
# subject (the first package named on the line) is a baseline package.
RUN out=$(${NB_PYTHON_PREFIX}/bin/uv pip check --python ${NB_PYTHON_PREFIX}/bin/python 2>&1 || true) \
 && printf '%s\n' "$out" | grep -qE '^Checked [0-9]+ packages' \
 && ! printf '%s\n' "$out" | grep '^The package' | grep -vE '^The package `(xmip|lonboard|pygobject|pycairo)`'