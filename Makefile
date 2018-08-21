make dependencies:
	pip install -Ur requirements.

make clean_database:
	rm db/datashop.db || true
	python create_database.py
