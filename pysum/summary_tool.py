import pandas as pd
import pytablewriter
from tabulate import tabulate
import os


class SummaryTool:
    def __init__(self):
        self.summary_cols = ['No', 'Variable', 'Stats / Values', 'Freqs (% of Valid)', 'Valid', 'Missing']

    def GetSummaryForColumn(self, no, col_name):
        col_set = self.df[col_name]
        col_summary = []

        # set No
        if self.var_numbers is True:
            col_summary.append(no)

        # get Variable
        variable = ''
        variable += col_name
        if self.data_type[col_name] == 'float64':
            variable += '\n' + ('[%s]' % ('float'))
        elif self.data_type[col_name] == 'int64':
            variable += '\n' + ('[%s]' % ('integer'))
        elif self.data_type[col_name] == 'object':
            variable += '\n' + ('[%s]' % ('character'))

        col_summary.append(variable)

        # get Stats / Values
        col_summary.append(self.GetStatsAndValues(col_name))

        # get Freqs (% of Valid)
        if self.data_type[col_name] == 'object':
            col_summary.append(self.GetFreqsForCharacter(col_name))
        else:
            col_summary.append('%d distinct val.' % (len(col_set.value_counts())))

        # get Valid
        valid = ''
        missing_count = col_set.isnull().sum()
        valid_count = self.row_count - missing_count
        valid += str(valid_count)
        if valid_count == 0:
            valid += '\n' + '(0%)'
        else:
            valid += '\n' + ('(%0.' + str(self.round_digits) + 'f%%)') % (100 * (valid_count / self.row_count))

        col_summary.append(valid)

        # get Missing
        if self.missing_col is True:
            missing = ''
            missing += str(missing_count)
            if missing_count == 0:
                missing += '\n' + '(0%)'
            else:
                missing += '\n' + ('(%0.' + str(self.round_digits) + 'f%%)') % (100*(missing_count/self.row_count))

            col_summary.append(missing)

        return col_summary

    def GetIQR(self, col_name):
        col_set = self.df[col_name]
        q1 = col_set.quantile(0.25)
        q3 = col_set.quantile(0.75)
        return q3 - q1

    # take second element for sort
    def takeSecond(self, elem):
        return elem[1]

    # take first element for sort
    def takeFirst(self, elem):
        return elem[0]

    def GetStatsAndValues(self, col_name):
        col_set = self.df[col_name]
        ret_val = ''

        if self.data_type[col_name] == 'float64':
            ret_val += '\n' + (('mean (sd) : %0.' + str(self.round_digits) + 'f (%0.' + str(self.round_digits) + 'f)') % (col_set.mean(), col_set.std()))
            ret_val += '\n' + ('min < med < max :')
            ret_val += '\n' + (('%0.' + str(self.round_digits) + 'f < %0.' + str(self.round_digits) + 'f < %0.' + str(self.round_digits) + 'f') % (col_set.min(), col_set.median(), col_set.max()))
            ret_val += '\n' + (('IQR (CV) : %0.' + str(self.round_digits) + 'f (%0.' + str(self.round_digits) + 'f)') % (self.GetIQR(col_name), col_set.std()/col_set.mean()))
        elif self.data_type[col_name] == 'int64':
            ret_val += '\n' + (('mean (sd) : %0.' + str(self.round_digits) + 'f (%0.' + str(self.round_digits) + 'f)') % (col_set.mean(), col_set.std()))
            ret_val += '\n' + ('min < med < max :')
            ret_val += '\n' + ('%d < %d < %d' % (col_set.min(), col_set.median(), col_set.max()))
            ret_val += '\n' + (('IQR (CV) : %d (%0.' + str(self.round_digits) + 'f)') % (self.GetIQR(col_name), col_set.std() / col_set.mean()))
        elif self.data_type[col_name] == 'object':
            # get col_count_list and sort it
            col_count_list = list(self.df.groupby(col_name)[col_name].count().items())
            if len(col_count_list) > self.max_distinct_values:
                col_count_list.sort(key=self.takeSecond, reverse=True)
            else:
                col_count_list.sort(key=self.takeFirst)

            idx = 1
            for group_name, count in col_count_list:
                if len(group_name) > self.max_string_width:
                    group_name = group_name[:self.max_string_width] + '...'
                ret_val += '\n' + ('%d. %s' % (idx, group_name))
                if idx == self.max_distinct_values:
                    ret_val += '\n' + (('[ %d others ]') % (len(col_count_list) - self.max_distinct_values))
                    break
                idx += 1

        return ret_val

    def GetFreqsForCharacter(self, col_name):
        ret_val = ''

        # get col_count_list and sort it
        col_count_list = list(self.df.groupby(col_name)[col_name].count().items())
        if len(col_count_list) > self.max_distinct_values:
            col_count_list.sort(key=self.takeSecond, reverse=True)
        else:
            col_count_list.sort(key=self.takeFirst)

        idx = 1
        other_count = 0
        for group_name, count in col_count_list:
            if idx <= self.max_distinct_values:
                ret_val += '\n' + (('%d ( %0.' + str(self.round_digits) + 'f%%)') % (count, 100 * (count / self.row_count)))
            else:
                other_count += count
            idx += 1

        if other_count > 0:
            ret_val += '\n' + (('%d ( %0.' + str(self.round_digits) + 'f%%)') % (other_count, 100 * (other_count / self.row_count)))

        return ret_val

    def WriteToExcelFile(self):
        writer = pytablewriter.ExcelXlsxTableWriter()
        writer.open(self.output_file)

        writer.make_worksheet(self.df.name)
        writer.header_list = self.summary_cols
        writer.value_matrix = self.df_summary
        writer.write_table()

        writer.close()

    def OutputMarkdown(self):
        writer = pytablewriter.MarkdownTableWriter()

        writer.table_name = self.df.name
        writer.header_list = self.summary_cols
        writer.value_matrix = self.df_summary

        writer.write_table()

    def WriteMarkdownFile(self):
        if self.append is True:
            f = open(self.output_file, 'a')
        else:
            f = open(self.output_file, 'w')
        f.write('\n')
        f.write('Data Frame Summary')
        f.write('\n')
        f.write(self.df.name)
        f.write('\n')
        f.write('N: ' + str(self.row_count))
        f.write('\n')
        f.write((tabulate(self.df_summary, tablefmt='simple', headers=self.summary_cols)))
        f.write('\n')
        f.close()

    def WriteHtmlFile(self):
        temp_file_name = str(self.output_file).split('.')[0] + '.md'
        if self.append is True:
            f = open(temp_file_name, 'a')
        else:
            f = open(temp_file_name, 'w')
        f.write('\n')
        f.write('<center>Data Frame Summary</center>')
        f.write('\n')
        f.write('<center>' + self.df.name + '</center>')
        f.write('\n')
        f.write('<center>' + 'N: ' + str(self.row_count) + '</center>')
        f.write('\n')
        f.write((tabulate(self.df_summary, tablefmt='simple', headers=self.summary_cols)))
        f.write('\n')
        f.close()

        os.system('pandoc -s -c custom.css -o ' + self.output_file + ' ' + temp_file_name)
        # os.unlink(temp_file_name)

    def summarizeDF(self, dataframe,
                    round_digits=2,
                    var_numbers=True,
                    missing_col=True,
                    max_distinct_values=10,
                    max_string_width=25,
                    output_type='html',
                    output_file='summary.html',
                    append=True):
        self.df = dataframe
        self.round_digits = round_digits
        self.var_numbers = var_numbers
        self.missing_col = missing_col
        self.max_distinct_values = max_distinct_values
        self.max_string_width = max_string_width
        self.output_type = output_type
        self.output_file = output_file
        if self.output_type == 'html':
            self.output_file = str(self.output_file).split('.')[0] + '.html'
        elif self.output_type == 'markdown':
            self.output_file = str(self.output_file).split('.')[0] + '.md'
        elif self.output_type == 'xlsx':
            self.output_file = str(self.output_file).split('.')[0] + '.xlsx'
        self.append = append

        self.summary_cols = []

        if self.var_numbers is True:
            self.summary_cols.append('No')

        self.summary_cols.append('Variable')
        self.summary_cols.append('Stats / Values')
        self.summary_cols.append('Freqs (% of Valid)')
        self.summary_cols.append('Valid')

        if self.missing_col is True:
            self.summary_cols.append('Missing')

        self.data_type = self.df.dtypes

        self.row_count = len(self.df)

        self.cols = list(self.df.columns.values)
        self.col_count = len(self.cols)

        self.df_summary = []

        for col_idx in range(0, self.col_count):
            col_summary = self.GetSummaryForColumn(col_idx + 1, self.cols[col_idx])
            self.df_summary.append(col_summary)

        if self.output_type == 'xlsx':
            self.WriteToExcelFile()
        elif self.output_type == 'markdown':
            self.OutputMarkdown()
            self.WriteMarkdownFile()
        elif self.output_type == 'html':
            self.OutputMarkdown()
            self.WriteHtmlFile()
