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
  ('test_nested_string', "a.a=b a.b=b", {"a": {"a":"b", "b":"b"}}),
  ('test_nested_multi_type', "a.a=true a.b=1.2 a.c=null", {"a": {"a":True, "b":1.2, "c":None}}),
  ('test_nested_list', "a.a=1,2,3", {"a":{"a":[1,2,3]}}),
  # Weird Ones
  ('test_inty_float', 'foo=1.0', {"foo": 1.0}),
  ('test_typey_key', "true=a", {"true": "a"}), # JSON spec does not allow non-string keys  
  ('test_blank_value', "a=", {"a": ""}),
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

    def test_invalid_key(self):
        try:
            self.parser.parse(["=="])
        except InvalidFormat, e:
            assert "key value cannot be '='" in e.args[0]
            return
        raise

    def test_no_type_coercion(self):
        self.parser.coerce_types = False
	assert self.parser.parse(["foo=true"]) == {"foo":"true"}

def generate_test(testname, querystring, document):
    def test(cls):
        parsed = cls.parser.parse(querystring.split())
        assert parsed == document, "'%s' is '%s', not '%s'" % (querystring, parsed, document)
    test.__name__ = testname
    return test

for testname, querystring, document in VALID:
    test = generate_test(testname, querystring, document)
    setattr(TestAllTheThings, testname, test)

if __name__ == '__main__':
    unittest.main()
