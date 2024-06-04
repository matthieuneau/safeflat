mkdir -p layer_wheels

rm -rf layer

pip download -r ../requirements.txt --dest layer_wheels --platform manylinux2014_aarch64 --python-version 3.11 --implementation cp --abi cp311 --only-binary=:all:

mkdir -p layer/python/lib/python3.11/site-packages

for whl in layer_wheels/*.whl; do
    unzip -o $whl -d layer/python/lib/python3.11/site-packages
done

rm -rf layer_wheels