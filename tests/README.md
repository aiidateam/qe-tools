# Tests for the qe-tools package

In this folder there are a number of tests to verify that the parser works with a number of different input files.
In particular, we are testing input files for all `ibrav` values, and for at least some common combinations of input flags (like units for coordinates, etc.).

Note: Some of the input file examples are taken from the Quantum ESPRESSO test-suite (Nov 2017).

## How to add a test
1. Put a new QE input file into the `data` subfolder, with `.in` extension (e.g. for this example: `new_test.in`)
2. Add a new method in the test class in `test_parsers.py`, like the following 
   (the method must start with `test_`):
   ```
       def test_new_test(self):
        self.singletest(label='new_test', parser='pw')
   ```
   (the label is used to choose the input filename by appending `.in` and looking into the `data` subfolder).
   
   **Note**: the `parser` option (optional, default=`pw`) decides which parser to use. The two options
   supported currently are `pw` and `cp`.
3. At this point the test will fail because there's no reference file to compare the results. 
   Run the following command to create a reference file:
   ```
       ./test_parsers.py --write-ref new_test pw
   ```
   replacing `new_test` with the correct label.
   
   **Note**: the last `pw` option is to run the `pw` parser: 
   replace it with `cp` to run the `cp` parser instead. [`pw` is the default value if not specified].
   This will create a new file in `data/ref/<LABEL>.json` (in our case: `data/ref/new_test.json`)
4. **IMPORTANT**: at this point the tests will run (you can run `python test_parsers.py` in an virtualenv in which you installed the `qe_tools` package). **However**, you have to make sure that the reference content in the JSON is correct!!

   So, **please inspect the content of the JSON file** and, if there is a bug, fix it in the code and then re-run the creation of the json.
5. If you have something in the JSON that you do *not* want to test, just remove it from the JSON: only things in the JSON will be compared with the output of the code (do not remove single elements of a list: either you remove the full list or a full key from a dictionary, or you keep it all). 

   Tests are done recursively in dictionaries and lists, using python's `TestCase.assertAlmostEqual` for numbers, and `TestCase.assertEqual` for the rest.
   
