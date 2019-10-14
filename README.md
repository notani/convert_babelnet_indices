# Convert BabelNet indices into JSON format

## Dependencies

- python 3.x
- tqdm
- [pylucene](https://lucene.apache.org/pylucene/)
    - See "[How to Use PyLucene](https://medium.com/@michaelaalcorn/how-to-use-pylucene-e2e2f540024c)" for the details on installation.

## Run

Download and extract [BabelNet](https://babelnet.org/) indices into `./BabelNet-CCBYSA-4.0.1`. The 3rd party CC-BY-SA resources can be downloaded from [the official website.](https://babelnet.org/download)

```shell
mkdir out
python extract_entries.py BabelNet-CCBYSA-4.0.1/dict_CC_BY_SA_30/ -o out/dict_CC_BY_SA_30.json -v
python extract_entries.py BabelNet-CCBYSA-4.0.1/dict_CC_BY_SA_40/ -o out/dict_CC_BY_SA_40.json -v
python extract_entries.py BabelNet-CCBYSA-4.0.1/dict_CC_BY_NC_SA_30/ -o out/dict_CC_BY_NC_SA_30.json -v
```

Note that the output files are huge (40G+).
