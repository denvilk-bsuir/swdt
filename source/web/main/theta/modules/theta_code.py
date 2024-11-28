import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from django.conf import settings
from main.models import Answer, Task
from main.theta.theta_abc import ThetaAbstract


RUNEXE = Path(settings.RUNEXE)


class ThetaCode(ThetaAbstract):
    name = 'theta_code'
    test_result = None
    count = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        answer:Answer = kwargs.get("answer")
        self.task: Task = kwargs.get('task')

        self.compiler = answer.answer_code.compiler.extension
        self.code = answer.answer_code.code
        # TODO: set delete to True
        self.dir = tempfile.TemporaryDirectory(delete=False)
        self.solution = Path(self.dir.name, f'code{self.compiler}')

        # saving solution to file for compilation
        with open(self.solution, 'w') as f:
            print(self.code, file=f)

        self.__compile_code()

    def __del__(self):
        ''' Cleaning all files after testing tasks '''
        self.dir.cleanup()

    @ThetaAbstract._logging("COMPILE")
    def __compile_code(self):
        ''' Method for compilation code '''

        match self.compiler:
            case '.cpp20':
                res = os.system(f"g++ -x c++ -std=c++20 -DCONTEST {self.solution} -o {self.dir.name}/main -v")
                if res != 0:
                    self.test_result = "CE"
            case '.py':
                return

    def __parse_verdict_from_xml(self, verdict_xml) -> str:
        tree = ET.parse(verdict_xml)
        for result in tree.findall("invocationResult"):
            if result.get('id') == 'program':
                res = result.find("invocationVerdict").text
                print(res)
                match res:
                    case "SUCCEEDED":
                        return "OK"
                    case "TIME LIMIT EXCEEDED":
                        return "TL"
                    case "MEMORY LIMIT EXCEEDED":
                        return "ML"
                    case _:
                        return "ERR"

    @ThetaAbstract._logging("RUN")
    def run(self) -> str:
        ''' Method for running code on test '''
        cmd = ''

        match self.compiler:
            case '.cpp20':
                cmd = str(Path(self.dir.name, 'main'))
            case ".py":
                return

        file_in = Path(self.test_dir.name, 'input.txt')
        file_out = Path(self.test_dir.name, 'output.txt')
        verdict = Path(self.test_dir.name, 'verdict.xml')

        run = f'{RUNEXE} -xml -i {str(file_in)} -o {str(file_out)} {cmd} > {str(verdict)}'
        res = os.system(run)

        r = self.__parse_verdict_from_xml(verdict)
        if res != 0:
            return 'RE'
        return r


    def is_valid(self, expected_output) -> bool:
        file_in = Path(self.test_dir.name, 'input.txt')
        file_out = Path(self.test_dir.name, 'output.txt')
        file_answer = Path(self.test_dir.name, 'expected.txt')
        real_output = None

        with open(file_out, 'r') as f:
            real_output = f.read()

        return expected_output.strip() == real_output.strip()

    @ThetaAbstract._logging("TEST")
    def test(self, input, expected_output):
        self.count += 1
        if self.test_result is not None or self.test_result == 'CE':
            return self.test_result

        self.test_dir = tempfile.TemporaryDirectory(delete=False)
        with open(Path(self.test_dir.name, 'input.txt'), 'w') as f:
            print(input, file=f)

        run_result = self.run()

        if run_result != "OK":
            self.test_result = run_result
            return

        if not self.is_valid(expected_output):
            self.test_result = 'WA'

        if self.task.test_set.all().count() == self.count:
            self.test_result = 'OK' if self.test_result is None else self.test_result

        self.test_dir.cleanup()
