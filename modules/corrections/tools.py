# -*- coding: iso-8859-15 -*-
from IPython.display import HTML
import traceback
import copy

def truncate (data, max_size=10):
    message = "{}".format(data)
    return message if len(message) <= max_size \
        else message [:max_size-3]+'...'

def truncate_list (data_list, max_size=10):
    message = ", ".join(["{}".format(x) for x in data_list])
    return message if len(message) <= max_size \
        else message [:max_size-3]+'...'

# safer to copy inputs most of the time (always?)
def clone_dataset (dataset, copy_mode):
    if copy_mode == 'shallow':
        return copy.copy(dataset)
    elif copy_mode == 'deep':
        return copy.deepcopy(dataset)
    else:
        return dataset

font_style='font-family:monospace;'

ok_style='background-color:#66CC66;'
ko_style='background-color:#CC3300;color:#e8e8e8;'
default_table_columns = (20, 20, 30)

def correction_table (student_function,
                         correct_function,
                         datasets,
                         columns = default_table_columns,
                         copy_mode = 'deep'):
    """
    colums should be a 3-tuple for the 3 columns widths
    copy_mode can be either None, 'shallow', or 'deep' (default)
    """
    c1,c2,c3 = columns
    html = ""
    html += u"<table style='{}'>".format(font_style)
    html += u"<tr><th>Entr�e</th><th>Attendu</th><th>Obtenu</th><th></th></tr>"

    for dataset in datasets:
        student_dataset = clone_dataset (dataset, copy_mode)
        correct_dataset = clone_dataset (dataset, copy_mode)
        # compute rendering of dataset *before* running in case there are side-effects
        rendered_input = truncate_list(student_dataset,c1)
        expected = apply (correct_function, correct_dataset)
        rendered_expected = truncate (expected, c2)
        # run both codes
        try:
            student_result = apply (student_function, student_dataset)
        except Exception as e:
            student_result = e
#        print 'expected',expected
#        print 'student_result',student_result
        # compare 
        ok = expected == student_result
        # render that run
        result_cell = '<td style="background-color:green;">'
        message = 'OK' if ok else 'KO'
        style = ok_style if ok else ko_style
        html += "<tr style='{}'>".format(style)
        html += "<td>{}</td><td>{}</td><td>{}</td><td>{}</td>".\
                format(rendered_input,rendered_expected,
                       truncate(student_result,c3),message)
    html += "</table>"
    return HTML(html)

# see how to use in exo_rendering.py
def exemple_table (function_name,
                      correct_function,
                      datasets,
                      columns = default_table_columns,
                      copy_mode = 'deep',
                      how_many=1):

    # can provide 3 args (convenient when it's the same as correction) or just 2
    columns = columns[:2]
    c1,c2 = columns
    html = ""
    html += u"<table style='{}'>".format(font_style)
    html += u"<tr><th>Appel</th><th>R�sultat attendu</th></tr>"
    
    for dataset in datasets [:how_many]:
        sample_dataset = clone_dataset (dataset, copy_mode)
        rendered_input = "{}({})".format(function_name,truncate_list(sample_dataset,c1))
        expected = apply (correct_function, sample_dataset)
        rendered_expected = truncate (expected, c2)
        html += "<tr><td>{}</td><td>{}</td></tr>".format(rendered_input,rendered_expected)

    html += "</table>"
    return HTML(html)
