"""Merge two CSV tables based on values in a given column"""
import pandas as pd
import numpy as np
import click

import logging
import os

def merge_data_frames(left: pd.DataFrame, right: pd.DataFrame, column: str, keep: str, keep_missing: str):
    """
    Merges two Pandas DataFrames
    
    Not using pd.merge due to handling of rows with empty values

    Parameters:
    left (pd.DataFrame): Path to first file
    right (pd.DataFrame): Path to second file
    column (str): Name of column to merge files on 
    keep (str): Table to keep values from when no match is found. One of ['left', 'right', 'both', 'none']. Default is 'none'
    keep_missing (str): Table to keep values from when row contains no value in given oclumn. One of ['left', 'right', 'both', 'none']. Default is 'none'
    
    Returns:
    (pd.DataFrame): Merged DataFrame

    """
    log = logging.getLogger(__name__)
    
    validate_options(left, right, column, keep, keep_missing)

    copied_from_left = set()
    outRows = []
    for index, row in left.iterrows():
        value = row[column]
        if type(value) == float and np.isnan(value):
            log.debug(f"Missing value in: left, index: {index}")
            if keep_missing in ['left', 'both']:
                outRows.append(row)
                log.debug(f"Keeping row, index: {index}")
            continue
        
        match = right[right[column] == value]
        if len(match) > 0:
            log.debug(f"Match found, index: {index}, value: {value}")
            mergedRow = pd.concat([row, match.iloc[0]])
            mergedRow = mergedRow[~mergedRow.index.duplicated()]
            outRows.append(mergedRow)
            copied_from_left.add(match.index.values[0])
        
        else:
            log.debug(f"No match found in left, {index}, value: {value}")
            if keep in ['left', 'both']:
                log.debug(f"Keeping row, index: {index}")
                outRows.append(row)

    for index, row in right.iterrows():
        if index in copied_from_left:
            continue
        value = row[column]
        if type(value) == float and np.isnan(value):
            log.debug(f"Missing value in: right, index: {index}")
            if keep_missing in ['right', 'both']:
                outRows.append(row)
                log.debug(f"Keeping row, index: {index}")
            continue

        log.debug(f"No match found in right, {index}, value: {value}")
        if keep in ['right', 'both']:
            log.debug(f"Keeping row, index: {index}")
            outRows.append(row)

    df = pd.DataFrame(outRows)
    
    return df


def merge_files(left_file: str, right_file: str, column: str, keep: str = 'none', keep_missing: str = 'none') -> pd.DataFrame:
    """
    Merges two csv files 
    Parameters:
    left_file (str): Path to first file
    right_file (str): Path to second file
    column (str): Name of column to merge files on 
    keep (str): Table to keep values from when no match is found. One of ['left', 'right', 'both', 'none']. Default is 'none'
    keep_missing (str): Table to keep values from when row contains no value in given oclumn. One of ['left', 'right', 'both', 'none']. Default is 'none'
    
    Returns:
    (pd.DataFrame): Merged DataFrame

    """
    log = logging.getLogger(__name__)

    dfLeft = pd.read_csv(left_file)
    dfRight = pd.read_csv(right_file)
    
    validate_options(dfLeft, dfRight, column, keep, keep_missing)
    
    log.info("Starting Merge")
    return merge_data_frames(dfLeft, dfRight, column, keep, keep_missing)


def configure_logging(verbose):
    if verbose:
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    else:
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def validate_options(left: pd.DataFrame, right: pd.DataFrame, column: str, keep: str, keep_missing: str) -> bool:
    log = logging.getLogger(__name__)
    # Check if column in each file 
    if column not in left.columns:
        raise ValueError(f"Column: {column}, not found in left file")

    if column not in left.columns:
        raise ValueError(f"Column: {column}, not found in right file")
    
    valid_keep_values = ['left', 'right', 'both', 'none']
    if keep not in valid_keep_values:
        raise ValueError(f"Given value for keep: {keep}, not in {valid_keep_values}")
    
    if keep_missing not in valid_keep_values:
        raise ValueError(f"Given value for keep_missing: {keep_missing}, not in {valid_keep_values}")
    
    return True
    

@click.command()
@click.option("--left-file", "-l", help="One of two CSVs to be merged")
@click.option("--right-file", "-r", help="Two of two CSVs to be merged")
@click.option("--column", "-c", help="Name of column to match entries")
@click.option("--output", "-o", help="Output file path")
@click.option("--keep", "-k", help="Table to keep values from if no match is found", type=click.Choice(['left', 'right', 'both', 'none']), default="none")
@click.option("--keep-missing", help="Keep rows where value in named column is null", type=click.Choice(['left', 'right', 'both', 'none']), default="none")
@click.option("--verbose", "-v", is_flag=True, help="Output extra information")
def main(left_file, right_file, column, output, keep, keep_missing, verbose):
    configure_logging(verbose)
    log = logging.getLogger(__name__)
    
    df = merge_files(left_file, right_file, column, keep, keep_missing)
    log.debug(df)
    
    log.info("Complete")
    
    if output:
        log.debug(f"Outputting to {output}")
        df.to_csv(output, index=False)
    
if __name__ == "__main__":
    exit(main())