# Scanarium Handbook

This repository holds the sources of the content of the "[Scanarium Handbook](https://handbook.scanarium.com)".

In order to build it:

1. Get [`scanarium-document-generator`](https://github.com/scanarium/scanarium-document-generator)
1. Run the following command in the root of your [`scanarium-handbook`](https://github.com/scanarium/scanarium-handbook) clone:

    `/path/to/scanarium-document-generator/generator.py --config config.json`

    (where `/path/to/scanarium-document-generator` should be replaced with the path where you cloned the [`scanarium-document-generator`](https://github.com/scanarium/scanarium-document-generator).)

1. Then you can find the generated HTML and MarkDown files in the `output` directory.