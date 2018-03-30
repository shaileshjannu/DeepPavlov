"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from random import Random
from typing import List, Generator, Tuple, Any

from deeppavlov.core.common.registry import register
from deeppavlov.core.common.log import get_logger

logger = get_logger(__name__)


@register('data_fitting_iterator')
class DataFittingIterator:
    """
    Dataset iterator for fitting models, e. g. vocabs, kNN, vectorizers.
    Data is passed as a list of strings(documents).
    Generate batches (for large datasets).
    """

    def __init__(self, data: List[str], doc_ids: List[Any] = None,
                 seed: int = None, shuffle: bool = False, batch_size: int = 1000,
                 *args, **kwargs) -> None:

        self._batch_size = batch_size
        self._shuffle = shuffle
        self._random = Random(seed)
        self.data = data
        self.doc_index = doc_ids or self.get_doc_ids()
        self.data = data

    @property
    def shuffle(self):
        return self._shuffle

    @shuffle.setter
    def shuffle(self, shuffle: bool):
        self._shuffle = shuffle

    @property
    def random(self):
        return self._random

    @random.setter
    def random(self, seed: int):
        self._random = Random(seed)

    @property
    def batch_size(self):
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size):
        if batch_size < 0:
            raise ValueError("Batch size should be a positive number!")
        self._batch_size = batch_size

    def get_doc_ids(self):
        return list(range(len(self.data)))

    def gen_batches(self) -> Generator[Tuple[List[list], List[int]], Any, None]:

        if self._shuffle:
            self.random.shuffle(self.doc_index)

        batches = [self.doc_index[i:i + self._batch_size] for i in
                   range(0, len(self.doc_index), self._batch_size)]

        # DEBUG
        # len_batches = len(batches)

        for i, doc_ids in enumerate(batches):
            # DEBUG
            # logger.info(
            #     "Processing batch # {} of {} ({} documents)".format(i, len_batches, len(doc_ids)))
            docs = [self.data[j] for j in doc_ids]
            yield docs, doc_ids
