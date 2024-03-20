# unsplash-iterable-dataset

An iterable dataset that downloads image-text pairs from Unsplash.

## Installation

Install with pip.

```sh
pip install git+https://github.com/oelin/unsplash-iterable-dataset
```

## Usage

```python
import torch
from unsplash_iterable_dataset import UnsplashIterableDataset


dataset = UnsplashIterableDataset(topics=['animals', 'people'], limit=6_000_000)

dataloder = torch.utils.data.DataLoader(dataset=dataset, batch_size=4, shuffle=False)
```
