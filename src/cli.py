import click
from .processors import csv_tools, cleaner
from .reporters import stats as stats_reporter, exporter


@click.group()
def cli():
    pass


@cli.group()
def process():
    pass


@process.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('-o', '--output', required=True, help='Output CSV file')
def merge(files, output):
    result = csv_tools.merge_csvs(list(files), output)
    click.echo(f'Merged {len(files)} files into {result}')


@process.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-f', '--format', 'fmt', type=click.Choice(['json', 'csv']), required=True)
@click.option('-o', '--output', default=None, help='Output file')
def convert(input_file, fmt, output):
    result = csv_tools.convert_file(input_file, fmt, output)
    click.echo(f'Converted {input_file} to {result}')


@cli.group()
def clean():
    pass


@clean.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', required=True, help='Output CSV file')
def deduplicate(input_file, output):
    result = cleaner.deduplicate(input_file, output)
    click.echo(f'Deduplicated data saved to {result}')


@clean.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--strategy', type=click.Choice(['mean', 'median', 'mode']), required=True)
@click.option('--column', default=None, help='Column to fill (default: all numeric)')
@click.option('-o', '--output', required=True, help='Output CSV file')
def fillna(input_file, strategy, column, output):
    result = cleaner.fillna(input_file, strategy, column, output)
    click.echo(f'Filled missing values saved to {result}')


@clean.command('filter')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--column', required=True, help='Column to filter on')
@click.option('--value', required=True, help='Value to filter for')
@click.option('-o', '--output', required=True, help='Output CSV file')
def filter_cmd(input_file, column, value, output):
    result = cleaner.filter_rows(input_file, column, value, output)
    click.echo(f'Filtered data saved to {result}')


@cli.group()
def report():
    pass


@report.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', required=True, help='Output JSON file')
def stats(input_file, output):
    result = stats_reporter.generate_stats(input_file, output)
    click.echo(f'Statistics saved to {result}')


@report.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', required=True, help='Output Excel file')
def excel(input_file, output):
    result = exporter.export_excel(input_file, output)
    click.echo(f'Excel report saved to {result}')


if __name__ == '__main__':
    cli()
