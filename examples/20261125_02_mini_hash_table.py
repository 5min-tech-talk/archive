DUMMY = object()  # 삭제된 자리에 남기는 '묘비석(Tombstone)'


class MiniHashTable:
    """Open Addressing + Tombstone(DUMMY) + 2/3 Load Factor 리사이징 구현"""

    def __init__(self, size: int = 8):
        self.size = size
        self.count = 0
        self.buckets: list = [None] * self.size

    def _index(self, key) -> int:
        return hash(key) % self.size

    def put(self, key, value) -> None:
        if (self.count + 1) / self.size > 0.66:
            self._resize()

        idx = self._index(key)
        first_dummy = None

        while self.buckets[idx] is not None:
            if self.buckets[idx] is DUMMY:
                if first_dummy is None:
                    first_dummy = idx
            elif self.buckets[idx][0] == key:
                self.buckets[idx] = (key, value)
                return
            idx = (idx + 1) % self.size

        target = first_dummy if first_dummy is not None else idx
        self.buckets[target] = (key, value)
        self.count += 1

    def get(self, key):
        idx = self._index(key)
        while self.buckets[idx] is not None:
            if self.buckets[idx] is not DUMMY and self.buckets[idx][0] == key:
                return self.buckets[idx][1]
            idx = (idx + 1) % self.size
        raise KeyError(key)

    def delete(self, key) -> None:
        idx = self._index(key)
        while self.buckets[idx] is not None:
            if self.buckets[idx] is not DUMMY and self.buckets[idx][0] == key:
                self.buckets[idx] = DUMMY
                self.count -= 1
                return
            idx = (idx + 1) % self.size
        raise KeyError(key)

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.size *= 2
        self.count = 0
        self.buckets = [None] * self.size
        for item in old_buckets:
            if item is not None and item is not DUMMY:
                self.put(item[0], item[1])


if __name__ == "__main__":
    ht = MiniHashTable()
    ht.put("apple", 1000)
    ht.put("melon", 5000)
    ht.delete("apple")
    print("apple 삭제 후 melon 조회:", ht.get("melon"))