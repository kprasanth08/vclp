import re
import os
from html_gen.htmldata import *
from Logger.logger import log


class HtmlGen:
    def __init__(self, tag, parser_data):
        self.parser_data = parser_data
        self.tag = tag
        self.table_data = ''

    def run(self):
        log('Generating Html')
        html_table = ''
        html_head_template.replace('_tag_', self.tag)
        html_head = html_head_template.replace('_tag_', self.tag)
        for driver, data in self.parser_data.items():
            #print(len(data['DriverNode']))
            self.table_data += 'var {0} = {1} ;\n'.format(self.tag + '_' + str(re.sub('\W+', '', driver)),
                                                          data['DriverNode'])
            html_table += html_table_template.replace('_tag_',
                                                      '{}'.format(self.tag + '_' + str(re.sub('\W+', '', driver))))
            self.table_data += 'var {0} = {1} ;\n'.format(
                self.tag + '_' + str(re.sub('\W+', '', driver) + '_TracePath'),
                data['TracePaths'])

            html_table += html_path_table_template.replace('_trace_path_',
                                                           '{}'.format(self.tag + '_' + str(
                                                               re.sub('\W+', '', driver) + '_TracePath')))

            html_table = html_table.replace('_driver_', driver)

        final_html = html_head.replace('_table_', html_table)
        summary_table = []
        driven_by = 'Not Found'
        for driver, data in self.parser_data.items():
            #print(len(data['DriverNode']))
            for _item in data['TracePaths']:
                if _item[0] == 2:
                    driven_by = _item[2]
                    break

            summary_table.append([driver, driven_by, len(data['DriverNode']), driver])

        self.table_data += 'var {0} = {1} ;\n'.format(self.tag + 'summary', summary_table)
        with open(os.path.join(os.getcwd(), 'HtmlReport/js/{}.js'.format(self.tag)), 'w+') as fp:
            fp.write(self.table_data)

        summary_html = html_summary_data.replace('_summ_tag_', self.tag + 'summary')
        final_html = final_html.replace('_summary_', summary_html)

        with open(os.path.join(os.getcwd(), 'HtmlReport/{}.html'.format(self.tag)), 'w+') as fp:
            fp.write(final_html)

    def add_data(self):
        pass
