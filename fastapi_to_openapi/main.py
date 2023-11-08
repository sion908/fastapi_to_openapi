import json
import yaml
from importlib import import_module
import click


@click.command()
@click.option("-i","--input_file", default='main', help="input file include fastapi APP")
@click.option("-f","--func", default="app", help="fastAPI app")
@click.option("-o","--output_file", default="openapi.yaml", help="output file name")
@click.option("-t","--file_type", default='yaml', type=click.Choice(['yaml', 'json'], case_sensitive=False), help="output file type.  yaml or json")
def cli(input_file,func, output_file, file_type):
    app = getattr(import_module(input_file.replace("/",".")),func)
    
    d = app.openapi()
    # YAMLをファイルに保存
    with open(output_file, "w") as f:
        if file_type=="yaml":
            yaml.dump(d, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        else:
            json.dump(d, f, sort_keys=False, ensure_ascii=False)
