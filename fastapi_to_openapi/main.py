import json
import yaml
from importlib import import_module
import click
import sys
import os
sys.path.append(os.getcwd())


@click.command()
@click.option("-i","--input_file", default='main', help="input file include fastapi APP")
@click.option("-f","--func", default="app", help="fastAPI app")
@click.option("-o","--output_file", default="openapi.default", help="output file name")
@click.option("-t","--file_type", default='yaml', type=click.Choice(['yaml', 'json'], case_sensitive=False), help="output file type.  yaml or json")
def cli(input_file,func, output_file, file_type):

    if "/" in input_file:
        sys.path.append(os.path.join(os.getcwd(),input_file.replace(f"/{input_file.split('/')[-1]}","")))

    try:
        module = import_module(input_file.replace("/","."))
        app = getattr(module,func)
    except (ModuleNotFoundError, AttributeError):
        modulenotfound_msg = getattr(ModuleNotFoundError, "msg","")
        attribute_msg = getattr(AttributeError, "msg","")
        
        import pdb; pdb.set_trace()
        if modulenotfound_msg:
            print(modulenotfound_msg)
            return None
        elif attribute_msg:
            print(attribute_msg)
            return None

    d = app.openapi()
    # YAMLをファイルに保存
    if output_file.split(".")[-1]=="default":
        output_file = output_file.replace("default", file_type)
    with open(output_file, "w") as f:
        if file_type=="yaml":
            yaml.dump(d, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        else:
            json.dump(d, f, sort_keys=False, ensure_ascii=False)
