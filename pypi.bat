del /q .\dist
del /q .\build
pip install twine
python3 -m build
twine upload -r pypi dist/*
del /q .\dist
del /q .\build