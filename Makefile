make clean:
	rm -rf build
	rm -rf dist
	rm -rf PyDex.spec
make release:
	pyinstaller PyDex.py
