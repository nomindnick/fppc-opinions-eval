"""Random baseline search engine for establishing floor metrics."""

import os
import random

from src.interface import SearchEngine


class RandomBaseline(SearchEngine):
    """Returns random opinion IDs. Useful as a lower-bound baseline."""

    def __init__(self, data_dir: str = "data/extracted", seed: int | None = None):
        self._rng = random.Random(seed)
        self._opinion_ids = []
        if os.path.isdir(data_dir):
            for year_dir in os.listdir(data_dir):
                year_path = os.path.join(data_dir, year_dir)
                if not os.path.isdir(year_path):
                    continue
                for fname in os.listdir(year_path):
                    if fname.endswith(".json"):
                        self._opinion_ids.append(fname[:-5])
        if not self._opinion_ids:
            raise RuntimeError(
                f"No opinion files found in '{data_dir}'. "
                "Ensure data/extracted/ contains year subdirectories with .json files."
            )

    def search(self, query: str, top_k: int = 20) -> list[str]:
        return self._rng.sample(self._opinion_ids, min(top_k, len(self._opinion_ids)))

    def name(self) -> str:
        return "RandomBaseline"
