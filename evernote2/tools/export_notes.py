import os
import shutil
import csv
import math
import time

from optparse import OptionParser

from evernote2.api.client import EvernoteClient
from evernote2.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote2.edam.type.ttypes import NoteSortOrder
from evernote2.edam.error.ttypes import EDAMSystemException, EDAMErrorCode

import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")

enex_file_basename = 'index.enex'


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

    enex_root = os.path.join(
        output_dir, 'note-enex',
    )
    if not os.path.exists(enex_root):
        os.makedirs(enex_root)

    download_all_note_enex(note_store, enex_root, note_metas)
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


def download_all_note_enex(note_store, enex_root, note_metas):
    total_cnt = len(note_metas)

    for idx, meta in enumerate(note_metas):
        title = meta['title']
        guid = meta['guid']
        note_dir = os.path.join(
            enex_root, 'note-%s' % guid)

        text_file = os.path.join(note_dir, enex_file_basename)

        if os.path.exists(text_file):
            logging.info('(%s/%s) skip download since exists: %s, %s' % (
                idx + 1, total_cnt, text_file, title))
            continue

        # download if not exists
        downloaded = False
        while not downloaded:
            try:
                download_one_note_enex(note_store, note_dir, guid)
            except EDAMSystemException as e:
                if e.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
                    duration = e.rateLimitDuration
                    logging.info('Rate limit reacheded, sleep %s seconds and retry' % duration)
                    time.sleep(duration)
            else:
                downloaded = True
                logging.info('(%s/%s) saved: %s, %s' % (idx + 1, total_cnt, note_dir, title))


def download_one_note_enex(note_store, note_dir, note_guid):
    """

    notes:

        save `enex_file_basename` at the end of all,
        so that we can check this file to know if the cache is good when resume running
    """
    # content_XHTML = note_store.getNote(
    #     note_guid,
    #     withContent=True,
    #     withResourcesData=True,
    # )


if __name__ == '__main__':
    main()
