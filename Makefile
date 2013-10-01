# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build2
BUILDDIR      = build

# Internal variables.
ALLSPHINXOPTS   = -d .doctrees $(SPHINXOPTS) source

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/
	touch $(BUILDDIR)/.nojekyll
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/."

clean:
	-rm -rf $(BUILDDIR)/*

deploy: clean html
	cd $(BUILDDIR) && git add -u . && git commit -m "Updated at `date`" && git push origin master

.PHONY: clean html
