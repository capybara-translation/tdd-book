# Running tests


```
# Run functional tests and unit tests
python manage.py test

# Run functional tests
python manage.py test functional_tests

# Run a specific functional test
python manage.py test functional_tests.test_list_item_validation

# Run unit tests
python manage.py test lists

# Run a specific unit test module
python manage.py test lists.tests.test_models
python manage.py test lists.tests.test_views

# Run a specific unit test method
python manage.py test functional_tests.test_list_item_validation.ItemValidationTest.test_cannot_add_duplicate_items
```


# Running devserver


```
python manage.py runserver
```