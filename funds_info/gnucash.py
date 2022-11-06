import re
import subprocess


def get_value_by_instrument(report_name: str, datafile: str) -> dict[str, float]:
    cmd = ['gnucash-cli', '--report', 'run', '--name=' + report_name, datafile]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return parse_value_by_instrument(proc.stdout.read().decode('utf-8'))


def parse_value_by_instrument(html_report: str) -> dict[str, float]:
    labels = re.split('"\\s*,\\s*"', re.search('"labels"\\s*:\\s*\\[\\s*"(.*)"\\s*],', html_report).group(1))
    instruments = [re.split('\\s*-\\s*', label)[0] for label in labels]
    volumes = list(
        map(float, re.split('\\s*,\\s*', re.search('"data"\\s*:\\s*\\[\\s*(.*)\\s*],', html_report).group(1))))
    return dict(zip(instruments, volumes))
