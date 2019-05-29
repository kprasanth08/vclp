import datetime
import re
import yaml

from Connector.sqldb import SqlDB
from Logger.logger import log
import fileinput

from sys import getsizeof


class Parser:
    def __init__(self, tag, report_config):
        self.tag = tag
        self.full_tag_report = ''
        self.yaml_report_array = []
        self.dict_report_array = []
        self.updated_dict_report_array = []
        self.generate_db = {'RET_ELEMENT_WILD': self.ret_element_wild_db,
                            'ISO_STRATEGY_REDUND': self.iso_strategy_redund_db,
                            'ISO_STRATEGY_MISSING': self.iso_strategy_missing,
                            'ISO_STRATMISSING_NOBOUNDARY': self.iso_stratmissing_noboundary_db,
                            'ISO_CONTROL_STATE': self.iso_control_state_db,
                            'UPF_BUFINV_ORDER': self.upf_bufinv_order,
                            'LS_SUPPLY_UNAVAIL': self.iso_stratcontrol_glitch_db,
                            'ISO_STRATCONTROL_GLITCH': self.iso_stratcontrol_glitch_db,
                            'UPF_HIERSRSN_CONN': self.iso_stratcontrol_glitch_db,
                            'ISO_STRATCLAMP_MISMATCH': self.iso_stratcontrol_glitch_db,
                            'PST_SUPPLY_MULTIPLE': self.iso_stratcontrol_glitch_db,
                            'RET_CONTROL_GLITCH': self.iso_ret_control_glitch_db,
                            'PST_STATE_MULTIPLE': self.iso_stratcontrol_glitch_db,
                            'UPF_SUPPLY_NOLOAD': self.iso_stratcontrol_glitch_db,
                            'ISO_STRATEGY_IGNORED': self.iso_stratcontrol_glitch_db,
                            }
        self.db = SqlDB(self.tag)
        self.db_connect = True
        self.parser_data = {}
        self.report_config = report_config
        log('Running {} '.format(self.tag))

    def analyze_report(self, report_file):
        log('Analyzing Reports..')
        # report_file = self.report_config['']  # generate the report file name
        _full_tag_report = ''
        try:
            pattern = re.compile(r"(\s+\w+)\n")  # pattern to find the keys with missing :

            f = open('temp.file', 'w+')
            with open(report_file, 'r') as fp:
                for line in fp:
                    match = pattern.match(line)
                    if match:
                        line = (match.group(1) + ':' + '\n')  # add the missing : to the keys to create yaml
                        f.write("%s" % line)
                    else:
                        f.write("%s" % line)
            f.close()
            f = open('temp.file', 'a')
            f.write('-----------------------------------')
            f.close()
            #   _full_tag_report += line
            # self.full_tag_report = _full_tag_report.splitlines()  # full report for the tag with yaml format
            # log(_full_tag_report)
        except Exception as e:
            log("Error opening file  {}".format(e))

    def data_splitter(self):
        log('Splitting data..')
        yaml_report = ''
        with open('temp.file', 'r') as fp:
            append = False

            while True:
                line = fp.readline()
                if line:
                    if re.match(r'\s*Tag.*:.*{}.*'.format(self.tag), line):
                        append = True
                    elif re.match(r'\s*-+', line):
                        append = False

                    if append:
                        yaml_report += line
                    else:
                        if not yaml_report == '':
                            data = yaml.load(yaml_report, Loader=yaml.FullLoader)
                            self.dict_report_array.append(data)
                            self.generate_db[self.tag](data)
                            log('Total violation found {}'.format(len(self.dict_report_array)))
                        yaml_report = ''

                else:
                    break
    #
    # def big_data_splitter(self):
    #     log('Splitting data..')
    #     yaml_report = ''
    #     for line in range(0, len(self.full_tag_report) - 1):
    #         if re.match(r'\s*Tag.*:.*{}.*'.format(self.tag), self.full_tag_report[line]):
    #             new_full_tag_report = self.full_tag_report[line:]
    #             break
    #     print(new_full_tag_report)
    #     with open('new_full_tag_report.txt'.format(self.tag), 'w+') as fp:
    #         for line in new_full_tag_report:
    #             fp.write("%s\n" % line)

    def yaml2db(self):
        log("creating local DB")
        self.generate_db[self.tag]()

    def iso_stratcontrol_glitch_db(self, data):
        while self.db_connect:
            self.db.execute(
                "CREATE TABLE IF NOT EXISTS {} (DriverNode VARCHAR(500),Strategy VARCHAR(500),UPFNetName VARCHAR(500));".format(
                    self.tag))
            self.db.execute("DELETE FROM {};".format(self.tag))
            self.db.commit()
            self.db_connect = False

        cmd = "INSERT INTO {0} (DriverNode,Strategy,UPFNetName) VALUES ('{1}','{2}','{3}');".format(
            str(self.tag),
            str(data['DriverNode']),
            str(data['Strategy']),
            str(data['UPFNet']['NetName']), )
        data['UPFNetName'] = data['UPFNet']['NetName']

        try:
            self.db.execute(cmd)
            self.db.commit()
            return data
        except:
            log("upload failed :")

    def iso_ret_control_glitch_db(self, data):
        while self.db_connect:
            self.db.execute(
                "CREATE TABLE IF NOT EXISTS {} (DriverNode VARCHAR(500),Strategy VARCHAR(500),UPFNetName VARCHAR(500));".format(
                    self.tag))
            self.db.execute("DELETE FROM {};".format(self.tag))
            self.db.commit()
            self.db_connect = False

        cmd = "INSERT INTO {0} (DriverNode,Strategy,UPFNetName) VALUES ('{1}','{2}','{3}');".format(
            str(self.tag),
            str(data['DesignDriver']['DrivingNode']),
            str(data['Strategy']),
            str(data['UPFNet']['NetName']), )
        data['UPFNetName'] = data['UPFNet']['NetName']
        data['DriverNode'] = data['DesignDriver']['DrivingNode']

        try:
            self.db.execute(cmd)
            self.db.commit()
            return data
        except:
            log("upload failed :")

    def ret_element_wild_db(self):
        # ToDo
        pass

    def iso_strategy_redund_db(self, data):
        while self.db_connect:
            self.db.execute(
                "CREATE TABLE IF NOT EXISTS {} (Strategy VARCHAR(500),LogicSource VARCHAR(500),LogicSink VARCHAR(500));".format(
                    self.tag))
            self.db.execute("DELETE FROM {};".format(self.tag))
            self.db.commit()
            self.db_connect = False

        for data in self.dict_report_array:
            self.updated_dict_report_array.append(data)
            cmd = "INSERT INTO {0} (Strategy,SourceSupply,SinkSupply,LogicSource,LogicSink) VALUES ('{1}','{2}','{3}','{4}','{5}');".format(
                str(self.tag),
                str(data['Strategy']),
                str(data['SourceInfo']['PowerNet']['NetName']),
                str(data['SinkInfo']['PowerNet']['NetName']),
                str(data['LogicSource']['PinName']),
                str(data['LogicSink']), )
            data['SourceSupply'] = data['SourceInfo']['PowerNet']['NetName']
            data['SinkSupply'] = data['SinkInfo']['PowerNet']['NetName']
        try:
            self.db.execute(cmd)
            self.db.commit()
            return data
        except:
            log("upload failed : check database schema/ db connectivity")

    def iso_strategy_missing(self):
        # ToDo
        pass

    def iso_stratmissing_noboundary_db(self):
        # ToDo
        pass

    def iso_control_state_db(self):
        # ToDo
        pass

    def upf_bufinv_order(self):
        # ToDo
        pass
