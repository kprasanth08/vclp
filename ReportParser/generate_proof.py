import os
import subprocess
import re
from Connector.sqldb import SqlDB
from Logger.logger import log


class ProofGen:
    def __init__(self, tag, tag_type, report_config, dict_data_array):

        self.tag = tag
        self.tag_type = tag_type
        self.report_config = report_config
        self.dict_data_array = dict_data_array
        self.drivernode_list = []
        self.db = SqlDB(self.tag)
        self.db_connect = True
        self.trace_paths = []
        self.parser_data = {}
        self.proof_function_list = {'ISO_STRATCONTROL_GLITCH': self.proof_strat_control_glitch,
                                    'RET_CONTROL_GLITCH': self.proof_ret_control_glitch,
                                    'ISO_STRATEGY_REDUND': self.proof_iso_strategy_redund,

                                    }

    def generate_proof_tcl(self):
        tcl_cmd = '## Commands to generate Proofs\n'

        for data in self.dict_data_array:
            if data['DriverNode'] in self.drivernode_list:
                continue
            else:
                self.drivernode_list.append(data['DriverNode'])
                tcl_cmd += 'echo \"Start-of {0}\" >> {1}_PROOFS.rpt\n'.format(data['DriverNode'], self.tag)
                tcl_cmd += 'report_trace_paths  [get_trace_paths -from {0} -back] >>{1}_PROOFS.rpt\n'.format(
                    data['DriverNode'], self.tag)
                tcl_cmd += 'echo \"End-of {0}\" >> {1}_PROOFS.rpt\n'.format(data['DriverNode'], self.tag)
        with open('Auto_Proof_{}.tcl'.format(self.tag), 'w+') as fp:
            fp.write(tcl_cmd)

    def execute_tcl(self):
        process = subprocess.Popen("source proof_gen_{}.tcl".format(self.tag), stdout=subprocess.PIPE, shell=True)
        print(str(process.communicate()[0]))

    def analyze_proof(self):

        with open(self.report_config[self.tag][self.tag_type]['PROOF'], 'r') as fp:
            proof_data = fp.readlines()
            log(self.report_config[self.tag][self.tag_type]['PROOF'])
            self.proof_function_list[self.tag](proof_data)

    def proof_strat_control_glitch(self, proof_data):
        for driver in self.drivernode_list:
            cmd = "CREATE TABLE IF NOT EXISTS '{}' (Sequence  INT PRIMARY KEY," \
                  " FlowPath VARCHAR(500),TransitPoint VARCHAR(500));".format(driver)
            self.db.execute(cmd)
            self.db.execute("DELETE FROM '{}';".format(driver))
            self.db.commit()
            trace_paths = []
            driver_nodes = []
            for line in range(0, len(proof_data) - 1):
                if re.match(r'\s*Start-of.*{}.*'.format(driver), proof_data[line]):
                    count = 0
                    while not re.match(r'\s*End-of.*{}.*'.format(driver), proof_data[line]):
                        line += 1
                        pattern = re.compile(r"\s*((\w*[/](\w*|\[|\]|\w|\d)+|[.*^\s])+)\s+((\w+|_|\s)+)")

                        match = pattern.match(proof_data[line])
                        if match:
                            count += 1
                            # print(count, match.group(1), match.group(4))
                            cmd = "INSERT INTO '{0}' (Sequence,FlowPath,TransitPoint) VALUES ('{1}','{2}','{3}');".format(
                                str(driver),
                                str(count),
                                str(match.group(1)),
                                str(match.group(4)))
                            trace_paths.append([count, str(match.group(1).strip()), str(match.group(4)).strip()])

                            try:
                                self.db.execute(cmd)
                            except:
                                print("upload failed :")
                    self.db.commit()
            for data_dict in self.dict_data_array:
                if data_dict['DriverNode'] == driver:
                    driver_nodes.append([data_dict['Strategy'], data_dict['UPFNetName']])

            self.parser_data[driver] = {'DriverNode': driver_nodes, 'TracePaths': trace_paths}
        # print(self.parser_data.keys())

    def proof_ret_control_glitch(self, proof_data):
        self.proof_strat_control_glitch(proof_data)

    def proof_iso_strategy_redund(self, proof_data):
        pass

    def run(self):
        self.generate_proof_tcl()
        # self.execute_tcl()
        self.analyze_proof()
        return self.parser_data
