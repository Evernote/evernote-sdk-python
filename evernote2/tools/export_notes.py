from optparse import OptionParser


def main():
    parser = OptionParser()

    parser.add_option('-t', '--token', dest='token', help='evernote_api_token')
    parser.add_option('-o', '--output_dir', dest='output_dir', help='dir to save notes', default='./notes-exported')
    parser.add_option('-s', '--sandbox', dest='is_sandbox', help='use sandbox', action='store_true', default=False)
    parser.add_option('-c', '--china', dest='is_china', help='use yinxiang.com instead of evernote.com', action='store_true', default=False)

    (options, args) = parser.parse_args()

    token = options.token
    output_dir = options.output_dir
    is_sandbox = options.is_sandbox
    is_china = options.is_china

    if token is None:
        print('error! token is None')
        parser.print_help()
        exit(1)

    print('sandbox: %s, china: %s, output_dir: %s' % (
        is_sandbox, is_china, output_dir
    ))


if __name__ == '__main__':
    main()
