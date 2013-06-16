import unittest
from jgen import Parser, InvalidFormat
import shlex

VALID = (
  # Standard
  ('test_string_string', 'a=b', {"a":"b"}),
  ('test_string_int', 'a=1', {"a":1}),
  ('test_string_bool', 'a=true', {"a":True}),
  ('test_string_float', 'a=2.30', {"a":2.3}),
  ('test_string_null', 'a=null', {"a":None}),
  ('test_string_list', "a=1,2,3", {"a":[1,2,3]}),
  ('test_string_multi_string', 'a=b c=d', {"a":"b", "c":"d"}),
  # Overrides
  ('test_override', 'a.a=b a=c', {"a":"c"}),
  # Nested
  ('test_nested_string', "a.a=b a.b=b", {"a": {"a":"b", "b":"c"}}),
  ('test_nested_multi_type', "a.a=true a.b=1.0 a.c=null", {"a": {"a":True, "b":1.0, "c":None}}),
  ('test_nested_list', "a.a=1,2,3", {"a":{"a":[1,2,3]}}),
  # Weird Ones
  ('test_typey_key', "true=a", {"true": "a"}), # JSON spec does not allow non-string keys  
  ('test_blank_key', "=a", {"": "a"}), # not sure why you would do this..
  ('test_blank_value', "a=", {"a": ""}),
  ('test_ridiculous_key_empty', "==", {"=": ""}),   # stop it.
  ('test_ridiculous_key_value', "===", {"=": "="}), # ..sigh.. if you must.
  ('test_stupidity', '\\=\\', {'\\': '\\'}), # oh come on!
)

class TestAllTheThings(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_invalid_key_val(self):
        try:
            self.parser.parse(["a"])
        except InvalidFormat, e:
            assert "must be in the format KEY=VALUE" in e.args[0]
            return
        raise

for testname, querystring, document in VALID:
    def test(cls):
        cls.assertTrue(cls.parser.parse(querystring.split()) == document)
    setattr(test, '__name__', testname)
    setattr(TestAllTheThings, testname, test)

if __name__ == '__main__':
    unittest.main()
