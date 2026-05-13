import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit

def make_splits(df, strategy="group", seed=42, test_size=0.1, val_size=0.1):
    """
    Розділяє дані на train/val/test. 
    Для топонімів важливо не розривати групи (canonical_name),
    щоб уникнути витоку знань про один і той самий об'єкт.
    """
    # Спочатку відокремлюємо Test
    gss_test = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train_val_idx, test_idx = next(gss_test.split(df, groups=df['canonical_name']))
    
    df_train_val = df.iloc[train_val_idx]
    df_test = df.iloc[test_idx]
    
    # Тепер ділимо Train/Val
    # Коригуємо розмір val відносно залишку
    val_adj_size = val_size / (1 - test_size)
    gss_val = GroupShuffleSplit(n_splits=1, test_size=val_adj_size, random_state=seed)
    train_idx, val_idx = next(gss_val.split(df_train_val, groups=df_train_val['canonical_name']))
    
    df_train = df_train_val.iloc[train_idx]
    df_val = df_train_val.iloc[val_idx]
    
    return {
        "train": df_train,
        "val": df_val,
        "test": df_test
    }

def save_ids(splits, out_dir="lab1_submission/data/sample"):
    for name, df in splits.items():
        path = f"{out_dir}/splits_{name}_ids.txt"
        df['text_id'].to_csv(path, index=False, header=False)
    return f"IDs збережені у {out_dir}"
