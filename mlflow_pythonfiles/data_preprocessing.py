import os
import polars as pl
def process_nans(df: pl.DataFrame, drop_thr: float = 0.95):
    for col in df.get_columns():
        nulls_prop = col.is_null().mean()
        print(f"{col.name} - {nulls_prop * 100}% missing")
        if nulls_prop >= drop_thr:
            print("Dropping", col.name)
            df = df.select([pl.exclude(col.name)])
        
        elif nulls_prop > 0:
            print("Imputing", col.name)
            
            if col.is_numeric():
                fill_value = col.median()
            else:
                
                fill_value = col.mode()
            df = df.select(
                [
                    pl.exclude(col.name),
                   
                    pl.col(col.name).fill_null(value=fill_value),
                ]
            )

    return df

def drop_static(df:pl.DataFrame):
    for col in df.get_columns():
        std = col.std()
        if std == 0:
            print("Dropping", col.name)
            df = df.select([pl.exclude(col.name)])
    
    return df

def train_val_test_split(df, test_size=0.2, val_size=0.2):
    df_train = df.filter(
        pl.col("month") < df['month'].quantile(0.8)
    )

    df_test = df.filter(
        pl.col("month") >= df['month'].quantile(0.8)
    )

    df_val = df_train.filter(
        pl.col("month") >= df_train['month'].quantile(0.8)
    )

    df_train = df_train.filter(
        pl.col("month") < df_train['month'].quantile(0.8)
    )

    return df_train, df_val, df_test

def preprocess_data(dset_path, missing_thr):
    df = pl.read_csv(dset_path)
    df = process_nans(df, missing_thr)
    df = drop_static(df) 
    train_df, val_df, test_df = train_val_test_split(df)
    
    split_destination_folder = './data/processed'
    if not os.path.exists(split_destination_folder):
        os.makedirs(split_destination_folder)

    train_df.write_parquet('./data/processed/train.parquet')
    val_df.write_parquet('./data/processed/validation.parquet')
    test_df.write_parquet('./data/processed/test.parquet')

    file_locations = {
        'train-data-dir': './data/processed/train.parquet',
        'val-data-dir': './data/processed/validation.parquet',
        'test-data-dir': './data/processed/test.parquet',
    }

    return file_locations