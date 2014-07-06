@ECHO OFF

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set BUILDDIR=build
set ALLSPHINXOPTS=-d %BUILDDIR%/doctrees %SPHINXOPTS% .

if "%1" == "" goto html

if "%1" == "html" (
	:html
	echo.---------------------
	echo.
	echo. !!! DOESNT WORK !!!
	echo.
	echo.---------------------
	python npc/update-npc.py
	python update-fits.py
	python wallet.py && cp srp.json %BUILDDIR%/
	%SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/
	echo ''>>%BUILDDIR%/.nojekyll
	if errorlevel 1 exit /b 1
	echo.
	echo.---------------------
	echo.
	echo. !!! DOESNT WORK !!!
	echo.
	echo.---------------------
	echo.Build finished. The HTML pages are in %BUILDDIR%/html.
	goto end
)

if "%1" == "clean" (
	for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i
	del /q /s %BUILDDIR%\*
	goto end
)

:end
