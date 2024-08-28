class Files:
    _files: list[bytes] = []

    def add(self, file: bytes | list[bytes]):
        is_list: bool = isinstance(file, list)
        self._files.extend(file) if is_list else self._files.append(file)
    
    def get_first(self) -> bytes:
        return self._files[0]

    def has_files(self) -> bool:
        return True if len(self._files) > 0 else False
    
    def clear(self) -> None:
        self._files.clear()
    
    def __iter__(self):
        return iter(self._files)