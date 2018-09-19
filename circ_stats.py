import argparse
import csv
import re

# Some call numbers might have a plus sign in them for some reason,
call_number_regex = re.compile(r'^(?:\+ )?(\D+)(\d+)')

# The fields as they exist in LibInsight
output_fields = ('Date/Time', 'Borrower Category', 'Day of Week', 'Loan Policy',
                 'Barcode', 'Title', 'Format', 'Shelving Location',
                 'Call Number', 'Call Number Class', 'Class and First Segment')

oclc_indices = (4, 5, 6, 8, 9, 11, 13, 15, 12)


def break_up_call_number(call_number):
    """
    Get call number class and call number class with first subdivision from
    call number.

    Regex captures just class in the first group, just subdivision in second,
    so .groups() is both in a list. Return a pair either way.

    :param call_number: LoC call number of an item
    :return: A pair with call # class and class+first subdivision
    """
    try:
        cn = call_number_regex.search(call_number)
        return cn.groups()[0], ''.join(cn.groups())
    except AttributeError:
        return 'N/A', 'N/A'


def oclc_to_libinsight(item):
    """
    Pull out the pieces of the OCLC report in the order we want them.

    Treat call numbers differently because we want to process them a bit first.
    Call #s are last item on OCLC's report, thus the -1 index.

    :param item: A circulation event item from OCLC
    :return: A list mapping to the columns in LibInsight circ report
    """
    base = [item[i] for i in oclc_indices]
    base.extend(break_up_call_number(base[-1]))
    base[0] = base[0].replace('/', '-')
    return base


if __name__ == '__main__':
    # To override args, just pass them on command line
    parser = argparse.ArgumentParser(description='Get input and output files')
    parser.add_argument('--from_oclc', help='Path to the OCLC csv file.',
                        default='data/Circulation_Events_Detail_Report.csv')
    parser.add_argument('--to_libinsight', help='Path to output the LibInsight file',
                        default='data/to_libinsight.csv')
    args = parser.parse_args()

    with open(args.from_oclc, 'rt', encoding='utf-8') as r, open(args.to_libinsight, 'wt', newline='', encoding='utf-8') as w:
        from_oclc, to_libinsight = csv.reader(r), csv.writer(w)

        next(from_oclc)  # skip header row
        to_libinsight.writerow(output_fields)  # write new header

        for circ_event in from_oclc:
            try:
                to_libinsight.writerow(oclc_to_libinsight(circ_event))
            except IndexError:
                # last couple of lines of report are short totals lines
                pass

