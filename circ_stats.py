import csv
import re

call_number_regex = re.compile(r'^(?:\+ )?(\D+)(\d+)')

output_fields = ('Date/Time', 'Borrower Category', 'Day of Week', 'Loan Policy',
                 'Barcode', 'Title', 'Format', 'Shelving Location',
                 'Call Number', 'Call Number Class', 'Class and First Segment')


def break_up_call_number(call_number):
    try:
        cn = call_number_regex.search(call_number)
        return cn.groups()[0], ''.join(cn.groups())
    except AttributeError:
        return 'N/A', 'N/A'


def oclc_to_libinsight(item):
    oclc_indices = (4, 5, 6, 8, 9, 11, 13, 15, 12)
    base = [item[i] for i in oclc_indices]
    base.extend(break_up_call_number(base[-1]))
    return base

if __name__ == '__main__':
    with open('data/Circulation_Events_Detail_Report.csv', 'rt', encoding='utf-8') as r, open('data/to_libinsight.csv', 'wt', newline='', encoding='utf-8') as w:
        from_oclc, to_libinsight = csv.reader(r), csv.writer(w)

        next(from_oclc)  # skip header row
        to_libinsight.writerow(output_fields)  # write new header

        for item in from_oclc:
            to_libinsight.writerow(oclc_to_libinsight(item))

