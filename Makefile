release: 
	pyinstaller PyDex.py
	./dist/PyDex/PyDex
clean:
	rm -rf build
	rm -rf dist
	rm -rf PyDex.spec
