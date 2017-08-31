import circ_stats
import csv
CN_CLASS_INDEX = 12
COLS_OUTPUT = [x for x in range(24) if x not in range(18, 23)]

if __name__ == '__main__':

    with open('data/Circulation_Events_Detail_Report.csv', 'rt', encoding='utf-8') as r, open('data/with_cn_class.csv', 'wt', newline='', encoding='utf-8') as w:
        from_oclc, new_one = csv.reader(r), csv.writer(w)
        header = next(from_oclc)
        header = [header[x] for x in COLS_OUTPUT]
        header.extend(("Call # Class", "Class w/ First Subdivision", "Use counter"))
        new_one.writerow(header)

        for item in from_oclc:
            try:
                item = [item[x] for x in COLS_OUTPUT]
                cn_class = circ_stats.break_up_call_number(item[CN_CLASS_INDEX])
                item.extend([cn_class[0], cn_class[1], 1])
                new_one.writerow(item)
            except IndexError:
                pass
