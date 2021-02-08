py5_java_src = $(shell find py5_jar/src/ -name "*.java")
py5_jar_file = py5_jar/dist/py5.jar

py5_py_src = $(shell find py5_resources/ -name "*.py*") $(shell find py5_resources/ -name "*.csv") $(shell find py5_docs/Reference/ -name "*.txt")
py5_txt_docs = $(shell find py5_docs/Reference/api_en/ -name "*.txt")

py5_generator = generate_py5.py
py5_doc_generator = generate_py5_docs.py
generator_src = $(shell find generator/ -name "*.py*")
py5_installed = $(py5_build_dir)/.install_py5.nogit
extra_args := 

ifeq ($(skip_autopep8), true)
	extra_args += --skip_autopep8
endif

all: install_py5

py5_jar: $(py5_jar_file)
$(py5_jar_file): $(py5_java_src)
	ant -f py5_jar/build.xml -Dprocessing_dir=$(realpath $(processing_dir))

generate_py5: $(py5_build_dir)
$(py5_build_dir): $(py5_jar_file) $(py5_py_src) $(py5_generator) $(generator_src) $(py5_txt_docs)
	python $(py5_generator) $(processing_dir) $(py5_build_dir) $(extra_args)

install_py5: $(py5_installed)
$(py5_installed): $(py5_build_dir)
	cd $(py5_build_dir) && python setup.py build && pip install .
	touch $(py5_installed)

distributions:
	cd $(py5_build_dir) && python setup.py sdist && python setup.py bdist_wheel

generate_py5_docs:
	python $(py5_doc_generator) $(py5_website_dir) py5_docs/Reference/$(py5_api_lang)

sphinx_docs:
	sphinx-build -M html py5_docs/sphinx $(py5_sphinx_dir)

.PHONY: clean
clean:
	rm -f $(py5_installed)
	ant -f py5_jar/build.xml clean
