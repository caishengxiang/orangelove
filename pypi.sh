rm -rf build/*
rm -rf dist/*
pip install twine
#python3 -m pip install --upgrade pip
#python3 -m pip install --upgrade build
python3 -m build
twine upload -r pypi dist/*
rm -rf build/*
rm -rf dist/*