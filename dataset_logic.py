import pandas as pd
import os
import random
import logging
import re

DATASET_DIR = "words_dataset"

logger = logging.getLogger(__name__)


def _first_translation(raw: str) -> str:
    """Extract the first clean translation from a comma/semicolon-separated string."""
    # Split on comma or semicolon, take first part, strip whitespace
    first = re.split(r'[,;]', str(raw))[0].strip()
    return first if first else str(raw).strip()


def _clean_stress(word: str) -> str:
    """Remove Unicode stress/accent marks from a Russian word (e.g. кото'рый -> который)."""
    return word.replace("\u0301", "").replace("'", "").strip()


def _load_all_datasets() -> pd.DataFrame:
    """Load and merge all CSV files in DATASET_DIR once at startup."""
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith('.csv')]
    frames = []
    for f in files:
        path = os.path.join(DATASET_DIR, f)
        try:
            df = pd.read_csv(path, sep='\t', on_bad_lines='skip', engine='python')
            frames.append(df)
        except Exception as e:
            logger.warning("Could not load %s: %s", f, e)
    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True)
    # Keep only rows that have both columns
    combined = combined.dropna(subset=['bare', 'translations_de'])
    # Produce clean single-value columns
    combined['word_de'] = combined['translations_de'].apply(_first_translation)
    combined['word_ru'] = combined['bare'].apply(lambda x: _clean_stress(str(x)))
    # Drop rows where cleaning produced empty strings
    combined = combined[(combined['word_de'] != '') & (combined['word_ru'] != '')]
    # Drop duplicates by German word so every quiz question is unique
    combined = combined.drop_duplicates(subset='word_de')
    return combined.reset_index(drop=True)


# Module-level cache — loaded once when the module is first imported
_DATASET: pd.DataFrame = _load_all_datasets()
logger.info("Dataset loaded: %d unique word pairs", len(_DATASET))


def get_random_dataset_word(exclude_words: list[str] | None = None) -> tuple[str, str] | None:
    """Return a random (german, russian) pair, optionally excluding recently seen words."""
    if _DATASET.empty:
        return None
    pool = _DATASET
    if exclude_words:
        pool = _DATASET[~_DATASET['word_de'].isin(exclude_words)]
        if pool.empty:  # all words were excluded — reset and use full pool
            pool = _DATASET
    row = pool.sample(n=1).iloc[0]
    return str(row['word_de']), str(row['word_ru'])


def get_multiple_dataset_translations(count: int = 3, exclude: str | None = None) -> list[str]:
    """Return `count` random Russian words from the dataset, excluding `exclude`."""
    if _DATASET.empty:
        return ["Собака", "Кошка", "Дом"][:count]

    translations = _DATASET['word_ru'].unique().tolist()
    if exclude:
        translations = [t for t in translations if t != str(exclude).strip()]

    if len(translations) < count:
        return translations
    return random.sample(translations, count)
