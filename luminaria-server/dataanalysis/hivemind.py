from common.timeless import prev_day
from database.stream.comment_frequency_model import CommentFrequencyModel
from constants import DB_CONFIG


def top(from_date):


    cursor = DB_CONFIG.execute_sql('''select date, sum(times_mentioned)
                                    from COMMENT_FREQUENCY 
                                    where date >= ?
                                    GROUP BY date;''',
                                   (from_date,))



    #for row in cursor.fetchall():
    #    print(row)
    print(prev_day(from_date))

def top_of_day(day, limit=20):

    i = 1
    for row in CommentFrequencyModel.get_top_on_day(day, limit):
        print(i, row.symbol, row.total)
        i += 1


top('2020-01-01')