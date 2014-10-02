.PHONY: noop rpm clean

noop:
	#noop

rpm:
	python setup.py sdist
	rpmbuild -ba ext/jgen.spec --define "_sourcedir ${PWD}/dist"

clean:
	rm -rf dist build *egg-info*
