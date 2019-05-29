# -*- coding: utf-8 -*-
from ReportParser.Parser import Parser
from ReportParser.generate_proof import ProofGen
from html_gen.html_gen import HtmlGen
import yaml
import time
start_time = time.time()


if __name__ == '__main__':
    with open(r'./ReportParser/reportconfig.yaml', 'r') as fp:
        report_config = yaml.load(fp.read(), Loader=yaml.FullLoader)

    for tag, tag_dict in report_config.items():
        parser = Parser(tag, report_config)
        parser_data = {} #ToDo parser_data[type]
        for tag_type, tag_files in tag_dict.items():
            # print(tag_files['REPORT'], tag_files['PROOF'])
            print(tag_type,report_config[tag][tag_type]['REPORT'])
            parser.analyze_report(report_config[tag][tag_type]['REPORT'])
            parser.data_splitter()
            #parser.yaml2db()
            proof = ProofGen(tag, tag_type, report_config, parser.dict_report_array)
            parser_data[type] = proof.run()
            html_gen = HtmlGen(parser.tag, parser_data[type])
            html_gen.run()

print("--- %s seconds ---" % (time.time() - start_time))