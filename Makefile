# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build2
BUILDDIR      = build

# Internal variables.
ALLSPHINXOPTS   = -d .doctrees $(SPHINXOPTS) .

.PHONY: clean html deploy

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/
	touch $(BUILDDIR)/.nojekyll
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/"

clean:
	-rm -rf $(BUILDDIR)/*
	rm -rf .doctrees

deploy: clean html
	cd $(BUILDDIR) && git add . && git add -u && \
		git commit -m "Updated at `LANG=C date`" && git push origin master
	git add . && git add -u && \
	git commit -m "Updated at `LANG=C date`" && git push origin source
