cd ..
cd stoqdrivers
rm -r build/
rm -r dist/
rm -r locale/es_ES
rm -r locale/pt_BR
rm -r stoqdrivers.egg-info/
python setup.py build
python setup.py install
