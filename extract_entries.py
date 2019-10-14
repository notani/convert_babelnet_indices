#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lucene

from java.io import File
from java.nio.file import Paths
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory

from tqdm import trange
import argparse
import json
import logging

verbose = False
logger = None


def init_logger(name='logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)
    return logger


def main(args):
    global verbose
    verbose = args.verbose

    if verbose:
        logger.info(f'Read {args.dir_index}')
    directory = SimpleFSDirectory.open(Paths.get(args.dir_index))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    reader = searcher.getIndexReader()

    if verbose:
        logger.info(f'Write to {args.path_output}')
    with open(args.path_output, 'w') as f:
        for idx in trange(reader.maxDoc()):
            doc = reader.document(idx)
            babelnet_id = doc.get('ID')
            synset_id = doc.get('SYNSET_ID')
            pos = doc.get('POS')
            synset_type = doc.get('TYPE')
            main_sense = doc.get('MAIN_SENSE')
            categories = list(doc.getValues('CATEGORY'))
            translation_mappings = list(doc.getValues('TRANSLATION_MAPPING'))
            images = list(doc.getValues('IMAGE'))
            lemmas = doc.getValues('LEMMA')
            forms = []
            for i in range(len(lemmas)):
                forms.append({
                    'lemma': lemmas[i],
                    'source': doc.getValues('LEMMA_SOURCE')[i],
                    'lang': doc.getValues('LEMMA_LANGUAGE')[i],
                    'weight': doc.getValues('LEMMA_WEIGHT')[i],
                    'sense_key': doc.getValues('LEMMA_SENSEKEY')[i],
                })
            entry = {
                'id': babelnet_id,
                'synset': synset_id,
                'pos': pos,
                'type': synset_type,
                'main_sense': main_sense,
                'categories': categories,
                'translation_mappings': translation_mappings,
                'images': images,
                'forms': forms
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    return 0


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    logger = init_logger('Extract')
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_index', help='path to index directory')
    parser.add_argument('-o', '--output', dest='path_output',
                        required=True,
                        help='path to output file')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose output')
    args = parser.parse_args()
    main(args)
