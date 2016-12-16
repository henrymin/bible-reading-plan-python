from datetime import timedelta, date


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def create_cal(gen):
    with open('Bible.txt') as bible_data, open('bible_cal.csv', 'w') as output:
        print('Subject,Start Date,Start Time,End Date, End Time, All Day Event', file=output)
        for line in bible_data:
            (book_name, number_of_chapter) = line.rstrip().split(',')
            print("The book of %s has %s chapters" % (book_name, number_of_chapter))

            for x in range(int(number_of_chapter)):
                the_date = process_weekends(gen, output)

                write_event_to_file(the_date, '%s chapter %s' % (book_name, x+1), output)
            print()


# the func always returns the next date which needs to add a regular reading event
def process_weekends(date_gen, output):
    the_date = next(date_gen)
    if the_date.weekday() != 5:  # Saturday
        return the_date

    # write Saturday's event
    write_event_to_file(the_date, 'Bible study reflection', output)

    # write Sunday's event
    write_event_to_file(next(date_gen), 'Bible study reflection', output)
    return next(date_gen)  # return next Monday's date


def write_event_to_file(the_date, subject, output):
    print('%s,%s,9:30 PM,%s,10:15 PM,False' %
          (subject, the_date.strftime('%m/%d/%Y'), the_date.strftime('%m/%d/%Y')), file=output)

if __name__ == '__main__':
    start_date = date(2017, 1, 2)
    end_date = date(2017, 12, 31)
    date_generator = daterange(start_date, end_date)
    create_cal(date_generator)
