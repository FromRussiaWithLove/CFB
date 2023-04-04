from prettytable import PrettyTable
import datetime_methods


class DefaultTabulator:

    @staticmethod
    def get_pretty_table(raw_data, child_name):
        table = PrettyTable()
        table.field_names = ['Time', 'Info']
        response = f'{child_name}\n'
        prev_date = ''
        for record in raw_data:
            feed_date, feed_time = datetime_methods.date_time_from_timestamp(record[1])
            if feed_date != prev_date:
                table.add_row([feed_date, ''])
                prev_date = feed_date
            table.add_row([feed_time[:5], record[2]])
        response += table.get_string()
        return f'<pre> {response} </pre>'
