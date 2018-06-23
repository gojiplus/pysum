from pysum.summary_tool import SummaryTool

def summarizeDF(dataframe,
                    round_digits=2,
                    var_numbers=True,
                    missing_col=True,
                    max_distinct_values=10,
                    max_string_width=25,
                    output_type='html',
                    output_file='summary.html',
                    append=True):
    pysum = SummaryTool()
    pysum.summarizeDF(dataframe, round_digits, var_numbers, missing_col, max_distinct_values, max_string_width, output_type, output_file, append)
