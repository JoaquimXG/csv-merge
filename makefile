dist/:
	python3 -m build
	
.PHONY: publish
publish: dist/
	python3 -m twine upload dist/*
	
.PHONY: publish-test
publish-test: dist/
	python3 -m twine upload --repository testpypi dist/*

.PHONY: clean
clean:
	rm -rf dist

.PHONY: clean-build
clean-build:
	$(MAKE) clean
	$(MAKE) build

.PHONY: clean-publish
clean-publish:
	$(MAKE) clean
	$(MAKE) publish