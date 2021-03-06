import csv
from .._csv import UnicodeCsvReader
from .. import utils
from . import base


class Client(base.Client):
    name = 'Delimited'

    description = '''
        Generator for delimited text files such as CSV.
    '''

    options = {
        'properties': {
            'uri': {
                'description': 'A URL or local filesystem path to a file.',
                'type': 'string',
            },
            'domain': {
                'description': 'The domain for new facts',
                'type': 'string',
                'default': None,
            },
            'time': {
                'description': 'The valid time for new facts',
                'type': 'string',
                'default': None,
            },
            'delimiter': {
                'description': 'The delimiter of the file.',
                'type': 'string',
                'default': ',',
            },
            'columns': {
                'description': 'An array of header column names.',
                'type': 'array',
                'default': None,
            },
            'header': {
                'description': 'A boolean denoting if the first line of the file is the header.',  # noqa
                'type': 'boolean',
                'default': None,
            },
            'encoding': {
                'description': 'The character encoding of the file.',
                'type': 'string',
                'default': 'utf-8',
            },
        }
    }

    def setup(self):
        f = utils.get_file(self.options.uri,
                           encoding=self.options.encoding)

        sniff = 1024
        dialect = None

        # Infer various properties about the file
        # Sample the file to determine the dialect
        sample = '\n'.join([l for l in f.readlines(sniff)])
        f.seek(0)

        # Determine dialect
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)

        r = UnicodeCsvReader(f,
                             dialect=dialect,
                             delimiter=self.options.delimiter,
                             encoding=self.options.encoding)

        # Get the first row as the header. Ignore overflow
        _header = [v for v in next(r) if v]

        # If no header is present and none is detected, use an enumeration
        if self.options.header is not True and \
                not sniffer.has_header(sample):
            f.seek(0)
            _header = range(len(_header))

        # If no columns are explicitly supplied, use the derived ones
        if not self.options.columns:
            self.options.columns = _header

    def parse_columns(self):
        columns = []
        for i, name in enumerate(self.options.columns):
            columns.append(name)
        return columns

    def parse(self):
        FIELDS = self.parse_columns()
        with open(self.options.uri, 'rU', newline='') as f:
            yield [
                'operation',
                'domain',
                'entity',
                'attribute',
                'value',
                'valid_time'
            ]

            reader = csv.DictReader(f, fieldnames=FIELDS,
                                    delimiter=self.options.delimiter)
            next(reader)
            for line in reader:
                for key, value in line.items():
                    if key != FIELDS[0]:
                        yield [
                            'assert',
                            self.options.domain,
                            line[FIELDS[0]],
                            key,
                            value,
                            self.options.time
                        ]
