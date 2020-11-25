import os
import shutil
import csv
import math

from optparse import OptionParser

from evernote2.api.client import EvernoteClient
from evernote2.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote2.edam.type.ttypes import NoteSortOrder

import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")


def main():
    parser = OptionParser()

    parser.add_option('-t', '--token', dest='token', help='evernote_api_token')
    parser.add_option('-o', '--output_dir', dest='output_dir', help='dir to save notes', default='./notes-exported')
    parser.add_option('-s', '--sandbox', dest='is_sandbox', help='use sandbox', action='store_true', default=False)
    parser.add_option('-c', '--china', dest='is_china', help='use yinxiang.com instead of evernote.com', action='store_true', default=False)
    parser.add_option('-f', '--force-delete', dest='is_force_delete', help='delete output_dir if exists', action='store_true', default=False)
    parser.add_option('-m', '--max-notes-count', dest='max_notes_count', help='max notes count to download', default='10000')

    (options, args) = parser.parse_args()

    token = options.token
    output_dir = options.output_dir
    is_sandbox = options.is_sandbox
    is_china = options.is_china
    is_force_delete = options.is_force_delete
    max_notes_count = int(options.max_notes_count)

    if token is None:
        logging.error('error! token is None')
        parser.print_help()
        exit(1)

    logging.info('sandbox: %s, china: %s, output_dir: %s' % (
        is_sandbox, is_china, output_dir
    ))

    init_output_dir(output_dir, is_force_delete)
    download_notes(token=token, sandbox=is_sandbox, china=is_china, output_dir=output_dir, max_notes_count=max_notes_count)


def init_output_dir(output_dir, is_force_delete):
    if os.path.exists(output_dir):
        if not is_force_delete and len(os.listdir(output_dir)) > 0:
            raise Exception('%s exists and not exmpty' % output_dir)

    if is_force_delete and os.path.exists(output_dir):
        logging.warning('drop dir: %s' % output_dir)
        shutil.rmtree(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def download_notes(token, sandbox, china, output_dir, max_notes_count):
    client = EvernoteClient(token=token, sandbox=sandbox, china=china)
    note_store = client.get_note_store()

    note_books = note_store.listNotebooks()
    save_notebooks(note_books, output_dir)

    note_books_map = {n.guid: n.name for n in note_books}

    note_metas = download_metadata(note_store, max_notes_count, note_books_map)
    save_notemetas(note_metas, output_dir)

    # download_note_content(note_store, note_metas)
    # total_cnt_notebooks = len(note_books)
    # for nb_idx, notebook in enumerate(note_books):
    #     nb_seq = nb_idx + 1

    #     logging.info('download notebook: (%s/%s) %s' % (nb_seq, total_cnt_notebooks, notebook.name))


def save_notebooks(note_books, output_dir):
    fn = os.path.join(output_dir, 'note_book_meta.csv')

    header = [
        'guid',
        'name',
        'stack',
        'contact',
    ]

    with open(fn, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(header)
        for notebook in note_books:
            record = [getattr(notebook, i) for i in header]
            csvwriter.writerow(record)

    logging.info('%s notebook meta saved in %s' % (len(note_books), fn))


def download_metadata(note_store, max_count, note_books_map):
    batch_cnt = 100
    max_count = max_count or 10000  # ensure valuable default

    loops = math.ceil(max_count / batch_cnt)
    metas = []

    for i in range(loops):
        offset = i * batch_cnt
        result_list = download_metadata_batch(note_store, offset, batch_cnt)

        for idx, note in enumerate(result_list.notes):
            note_meta = {
                # 'idx': offset + idx + 1,
                'guid': note.guid,
                'title': note.title,
                'contentLength': note.contentLength,
                'created': note.created,
                'updated': note.updated,
                'updateSequenceNum': note.updateSequenceNum,
                'tagGuids': note.tagGuids,
                'notebookGuid': note.notebookGuid,
                'notebookName': note_books_map[note.notebookGuid],
                'attr_author': note.attributes.author,
                'attr_source': note.attributes.source,
                'attr_sourceURL': note.attributes.sourceURL,
                'attr_sourceApplication': note.attributes.sourceApplication,
                'attr_shareDate': note.attributes.shareDate,
                # 'attributes': note.attributes,
                # 'largestResourceMime': note.largestResourceMime,
                # 'largestResourceSize': note.largestResourceSize,
            }
            metas.append(note_meta)

        if len(result_list.notes) < 100:
            break

    return metas[:max_count]


def download_metadata_batch(note_store, offset=0, batch_cnt=100):
    # note is an instance of NoteMetadata
    # result_list is an instance of NotesMetadataList

    updated_filter = NoteFilter(order=NoteSortOrder.UPDATED)
    result_spec = NotesMetadataResultSpec(
        includeTitle=True,
        includeContentLength=True,
        includeCreated=True,
        includeUpdated=True,
        includeUpdateSequenceNum=True,
        includeNotebookGuid=True,
        includeTagGuids=True,
        includeAttributes=True,
        # includeLargestResourceMime=True,
        # includeLargestResourceSize=True,
    )

    result_list = note_store.findNotesMetadata(updated_filter, offset, batch_cnt, result_spec)

    return result_list


def save_notemetas(note_metas, output_dir):
    fn = os.path.join(output_dir, 'note_meta.csv')

    fieldnames = [
        'guid',
        'title',
        'contentLength',
        'created',
        'updated',
        'updateSequenceNum',
        'tagGuids',
        'notebookGuid',
        'notebookName',
        'attr_author',
        'attr_source',
        'attr_sourceURL',
        'attr_sourceApplication',
        'attr_shareDate',
    ]

    with open(fn, 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for record in note_metas:
            csvwriter.writerow(record)

    logging.info('%s note metas saved in %s' % (len(note_metas), fn))


if __name__ == '__main__':
    main()
