try:
    import json
except ImportError:
    import simplejson as json

import sys
import optparse
from copy import deepcopy

class InvalidFormat(ValueError): pass

# http://www.xormedia.com/recursively-merge-dictionaries-in-python/
def dict_recursive_merge(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_recursive_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

def get_cli():
    cli = optparse.OptionParser()
    cli.add_option('-p', '--pretty-print', action='store_true')
    return cli

class Parser(object):
    def parse(self, parts):
        document = {}
        for part in parts:
            document = dict_recursive_merge(document, self.parse_part(part))
        return document

    def split(self, part):
        return part.split('=', 1)

    def create_nested_hash(self, key, value):
        parts = key.split('.')
        document = {}
        current_level = document
        levels = len(parts)
        for index, part in enumerate(parts):
            if part not in current_level:
                if index != ( levels - 1 ):
                    current_level[part] = {}
                else:
                    current_level[part] = value
            current_level = current_level[part]
        return document

    def coerce(self, value):
        result = value
        for coercer_func in self._coercer_funcs:
            coerced = coercer_func(value)
            if coerced is not value:
                result = coerced
                break
        return result

    @property
    def _coercer_funcs(self):
        return [self._coerce_null, self._coerce_bool, self._coerce_int, self._coerce_float]

    def _coerce_null(self, value, nulls=['null']):
        result = value
        if value in nulls:
            result = None
        return result

    def _coerce_bool(self, value, trues=["true"], falses=["false"]):
        result = value 
        if result in trues:
            result = True
        elif result in falses:
            result = False
        return result

    def _coerce_int(self, value):
        result = value
        try:
            coerced = int(value)
            if str(coerced) == value:
                result = coerced
        except ValueError:
            pass
        return result

    def _coerce_float(self, value):
        result = value
        try:
            # strip insignificant 0's prior to casting
            real_value = value.rstrip("0")
            coerced = float(real_value)
            if str(coerced) == real_value:
                result = coerced
        except ValueError:
            pass
        return result

    def convert_value_part(self, part, coerce_types=True):
        # TODO allow escaped commas
        if "," in part:
            result = part.split(",")
            if coerce_types:
                result = map(self.coerce, result)
        else:
            result = part
            if coerce_types:
                result = self.coerce(result)
        return result

    def parse_part(self, part):
        try:
            key, val = self.split(part)
        except ValueError:
            raise InvalidFormat("'%s' must be in the format KEY=VALUE" % part)
        converted_val = self.convert_value_part(val) 
        return self.create_nested_hash(key, converted_val)

def serialize(obj, pretty=False):
    if pretty:
        kwargs = {"indent":2}
    else:
        kwargs = {}
    return json.dumps(obj, **kwargs)

def main(argv=None):
    cli = get_cli()
    opts, args = cli.parse_args(argv)

    parser = Parser()
    try:
        result = parser.parse(args) 
    except InvalidFormat, e:
        cli.error(e.args[0])
    sys.stdout.write(serialize(result, pretty=opts.pretty_print) + "\n")

if __name__ == '__main__':
    main()
