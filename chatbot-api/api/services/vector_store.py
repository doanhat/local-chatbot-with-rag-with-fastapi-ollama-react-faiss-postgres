from typing import List

import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension=384) -> None:  # Change default dimension to 384
        self.index = faiss.IndexFlatL2(dimension)
        self.document_ids: List[str] = []

    def add_document(self, document_id, embedding) -> None:
        if isinstance(embedding, list):
            embedding = np.array(embedding)
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        self.index.add(embedding)
        self.document_ids.append(document_id)

    def search(self, query_vector, k=5) -> list | list[tuple]:
        if not self.document_ids:  # Check if the store is empty
            return []  # Return an empty list if there are no documents

        if isinstance(query_vector, list):
            query_vector = np.array(query_vector)
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        distances, indices = self.index.search(query_vector, k)
        return [
            (self.document_ids[i], distances[0][j]) for j, i in enumerate(indices[0])
        ]


# No need to specify dimension, it will use 384 by default
vector_store = VectorStore()
