# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = build
PYTHON        = python2

# Internal variables.
ALLSPHINXOPTS   = -d .doctrees $(SPHINXOPTS) .

.PHONY: clean html deploy

html:
	$(PYTHON) update-fits.py
	$(PYTHON) wallet.py
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/
	touch $(BUILDDIR)/.nojekyll
	echo "raisa.su" > $(BUILDDIR)/CNAME
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/"

submodule:
	[ -e $(BUILDDIR)/.git ] || git submodule init && git submodule update

clean:
	cd $(BUILDDIR) && git fetch && git reset --hard origin/master
	-rm -rf $(BUILDDIR)/*
	-rm -rf .doctrees

deploy: clean html
	cd $(BUILDDIR) && \
		git add -A && \
		git commit -m "Updated at `LANG=C date`" && \
		git push origin master
	git add -A && \
		git commit -m "Updated at `LANG=C date`" && \
		git rebase origin/source && \
		git push origin source
