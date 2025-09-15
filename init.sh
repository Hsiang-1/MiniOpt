pip install llamafactory==0.9.3

git clone https://github.com/NVIDIA/apex.git
cd apex
git checkout e13873debc4699d39c6861074b9a3b2a02327f92
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
pip install --upgrade bitsandbytes

pip install verl[vllm]==0.5.0

pip install pyomo
conda config --set solver classic
conda update conda -y
conda install -c conda-forge glpk coincbc ipopt scip pulp -y
