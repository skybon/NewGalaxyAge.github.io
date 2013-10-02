# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = build

# Internal variables.
ALLSPHINXOPTS   = -d .doctrees $(SPHINXOPTS) .

.PHONY: clean html deploy

html:
	python update-fits.py
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/
	touch $(BUILDDIR)/.nojekyll
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/"

submodule:
	[ -e $(BUILDDIR)/.git ] || git submodule init && git submodule update

clean:
	-rm -rf $(BUILDDIR)/*
	-rm -rf .doctrees

deploy: clean html
	cd $(BUILDDIR) && \
		git add -A && \
		git commit -m "Updated at `LANG=C date`" && \
		git fetch && git rebase origin/master && \
		git push origin master
	git add -A && \
		git commit -m "Updated at `LANG=C date`" && \
		git rebase origin/source && \
		git push origin source
