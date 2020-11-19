import os
import shutil
import csv

from optparse import OptionParser

from evernote2.api.client import EvernoteClient

import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")


def main():
    parser = OptionParser()

    parser.add_option('-t', '--token', dest='token', help='evernote_api_token')
    parser.add_option('-o', '--output_dir', dest='output_dir', help='dir to save notes', default='./notes-exported')
    parser.add_option('-s', '--sandbox', dest='is_sandbox', help='use sandbox', action='store_true', default=False)
    parser.add_option('-c', '--china', dest='is_china', help='use yinxiang.com instead of evernote.com', action='store_true', default=False)
    parser.add_option('-f', '--force-delete', dest='is_force_delete', help='delete output_dir if exists', action='store_true', default=False)

    (options, args) = parser.parse_args()

    token = options.token
    output_dir = options.output_dir
    is_sandbox = options.is_sandbox
    is_china = options.is_china
    is_force_delete = options.is_force_delete

    if token is None:
        logging.error('error! token is None')
        parser.print_help()
        exit(1)

    logging.info('sandbox: %s, china: %s, output_dir: %s' % (
        is_sandbox, is_china, output_dir
    ))

    init_output_dir(output_dir, is_force_delete)
    download_notes(token=token, sandbox=is_sandbox, china=is_china, output_dir=output_dir)


def init_output_dir(output_dir, is_force_delete):
    if os.path.exists(output_dir):
        if not is_force_delete and len(os.listdir(output_dir)) > 0:
            raise Exception('%s exists and not exmpty' % output_dir)

    if is_force_delete:
        logging.warning('drop dir: %s' % output_dir)
        shutil.rmtree(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def download_notes(token, sandbox, china, output_dir):
    client = EvernoteClient(token=token, sandbox=sandbox, china=china)
    note_store = client.get_note_store()

    notebooks = note_store.listNotebooks()
    save_notebooks(notebooks, output_dir)

    total_cnt_notebooks = len(notebooks)
    for nb_idx, notebook in enumerate(notebooks):
        nb_seq = nb_idx + 1

        logging.info('download notebook: (%s/%s) %s' % (nb_seq, total_cnt_notebooks, notebook.name))


def save_notebooks(notebooks, output_dir):
    fn = os.path.join(output_dir, 'notebook_meta.csv')

    header = [
        'guid',
        'name',
        'stack',
        'contact',
    ]

    with open(fn, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(header)
        for notebook in notebooks:
            record = [getattr(notebook, i) for i in header]
            csvwriter.writerow(record)

    logging.info('%s notebook meta saved in %s' % (len(notebooks), fn))


if __name__ == '__main__':
    main()
