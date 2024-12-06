import os
import shutil
import tempfile
import xml.etree.ElementTree as ET
from enum import Enum
from pathlib import Path
from django.conf import settings
from main.models import Answer, Task
from main.theta.theta_abc import ThetaAbstract


RUNEXE = Path(settings.RUNEXE)
TESTLIB = Path(settings.TESTLIB)


class ThetaCode(ThetaAbstract):
    name = 'theta_code'
    test_result = None
    count = 0
    EXECUTABLE_CODE_NAME = 'main'
    EXECUTABLE_CHECKER_NAME = 'checker'

    DEFAULT_TIME_LIMIT = 1000
    DEFAULT_MEM_LIMIT = 128 * 1024

    class __CheckerResult(Enum):
        OK = 0
        WA = 1
        PE = 2
        FAIL = 3
        DIRT = 4
        POINTS = 5
        UNEXPECTED_EOF = 8
        PARTIALLY = 16

    class TaskResultVerdict(Enum):
        OK = 'ok'
        WA = 'wa'
        CE = 'ce'
        RE = 're'
        PE = 'pe'
        FAIL = 'fail'
        ML = 'ml'
        TL = 'tl'
        ERR = 'err'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        answer:Answer = kwargs.get("answer")
        self.task: Task = kwargs.get('task')

        self.compiler = answer.answer_code.compiler.extension
        self.code = answer.answer_code.code
        # TODO: set delete to True
        self.dir = tempfile.TemporaryDirectory(delete=settings.TEMP_DIR_DELETE)
        self.solution = Path(self.dir.name, f'code{self.compiler}')

        # saving solution to file for compilation
        with open(self.solution, 'w') as f:
            print(self.code, file=f)

        self.__compile_code(self.EXECUTABLE_CODE_NAME, self.solution)

        # compiling checker if exists
        if self.task.checker is not None:
            shutil.copy(TESTLIB, Path(self.dir.name, 'testlib.h'))
            self.checker = Path(self.dir.name, f'checker{self.task.checker.compiler.extension}')
            with open(self.checker, 'w') as f:
                print(self.task.checker.code, file=f)
            self.__compile_code(self.EXECUTABLE_CHECKER_NAME, self.checker)
            self.checker_executable = Path(self.dir.name, f'checker')

    def __del__(self):
        ''' Cleaning all files after testing tasks '''
        self.dir.cleanup()

    @ThetaAbstract._logging("COMPILE")
    def __compile_code(self, name: str, file: Path):
        ''' Method for compilation code '''

        match self.compiler:
            case '.cpp20':
                res = os.system(f"g++ -x c++ -std=c++20 -O0 -DCONTEST {file} -o {self.dir.name}/{name} -v")
                if res != 0:
                    self.test_result = ThetaCode.TaskResultVerdict.CE
            case '.py':
                return

    @ThetaAbstract._logging("PARSE")
    def __parse_verdict_from_xml(self, verdict_xml) -> str:
        ''' Method for parse verdict from runexe XML file '''
        tree = ET.parse(verdict_xml)
        for result in tree.findall("invocationResult"):
            if result.get('id') == 'program':
                res = result.find("invocationVerdict").text
                exit_code = result.find("exitCode").text
                match res:
                    case "SUCCEEDED":
                        if exit_code != '0':
                            return ThetaCode.TaskResultVerdict.ERR
                        return ThetaCode.TaskResultVerdict.OK
                    case "TIME_LIMIT_EXCEEDED":
                        return ThetaCode.TaskResultVerdict.TL
                    case "MEMORY_LIMIT_EXCEEDED":
                        return ThetaCode.TaskResultVerdict.ML
                    case "CRASH":
                        return ThetaCode.TaskResultVerdict.FAIL
                    case _:
                        return ThetaCode.TaskResultVerdict.ERR

    @ThetaAbstract._logging("RUN")
    def run(self) -> TaskResultVerdict:
        ''' Method for running code on test '''
        cmd = ''

        match self.compiler:
            case '.cpp20':
                cmd = str(Path(self.dir.name, self.EXECUTABLE_CODE_NAME))
            case ".py":
                return

        file_in = Path(self.test_dir.name, 'input.txt')
        file_out = Path(self.test_dir.name, 'output.txt')
        verdict = Path(self.test_dir.name, 'verdict.xml')

        run = (
            f'{RUNEXE} -xml -m {self.task.memory_limit}M '
            f'-t {self.task.time_limit}ms -i {str(file_in)} '
            f'-o {str(file_out)} {cmd} > {str(verdict)}'
        )

        res = os.system(run)
        if res != 0:
            return ThetaCode.TaskResultVerdict.RE
        verdict = self.__parse_verdict_from_xml(verdict)
        if res != 0:
            return ThetaCode.TaskResultVerdict.RE
        return verdict

    def is_valid(self) -> __CheckerResult:
        '''  '''
        file_in = Path(self.test_dir.name, 'input.txt')
        file_out = Path(self.test_dir.name, 'output.txt')
        file_answer = Path(self.test_dir.name, 'expected.txt')
        real_output = None
        expected_output = None

        with open(file_out, 'r') as f:
            real_output = f.read()
        with open(file_answer, 'r') as f:
            expected_output = f.read()

        if self.task.checker is None:
            return expected_output.strip() == real_output.strip()

        res = os.system(f"{self.checker_executable} {file_in} {file_out} {file_answer}")
        check_result = self.__CheckerResult(res)
        return check_result

    @ThetaAbstract._logging("TEST")
    def test(self, input, expected_output):
        self.count += 1
        if self.test_result is not None or self.test_result == ThetaCode.TaskResultVerdict.CE:
            return self.test_result

        self.test_dir = tempfile.TemporaryDirectory(delete=settings.TEMP_DIR_DELETE)
        with open(Path(self.test_dir.name, 'input.txt'), 'w') as f:
            print(input, file=f)
        with open(Path(self.test_dir.name, 'expected.txt'), 'w') as f:
            print(expected_output, file=f)

        run_result = self.run()

        if run_result != ThetaCode.TaskResultVerdict.OK:
            self.test_result = run_result.value
            return

        is_valid = self.is_valid()
        if is_valid != ThetaCode.__CheckerResult.OK:
            self.test_result = ThetaCode.TaskResultVerdict(is_valid.name)

        if self.task.test_set.all().count() == self.count:
            self.test_result = ThetaCode.TaskResultVerdict.OK if self.test_result is None else self.test_result

        self.test_dir.cleanup()
