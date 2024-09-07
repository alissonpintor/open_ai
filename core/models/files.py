import PIL.Image as img
from typing import Iterator


class Files:
    def __init__(self) -> None:
        self.__base64_files: list[str] = []
        self.__image: img.Image | None = None

    def add(self, file: str | list[str]):
        is_list: bool = isinstance(file, list)
        self.__base64_files.extend(file) if is_list else self.__base64_files.append(file)
    
    def get_image(self) -> img.Image | None:
        return self.__image
    
    def set_image(self, image: img.Image) -> None:
        self.__image = image
    
    def get_first(self) -> str:
        return self.__base64_files[0]

    def has_files(self) -> bool:
        return True if len(self.__base64_files) > 0 else False
    
    def clear(self) -> None:
        self.__base64_files.clear()
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.__base64_files)