from enum import Enum, unique

extension_enum_dict_map = None


@unique
class AllowedExtension(Enum):
    JPEG = ("jpeg", "image/jpeg")
    PNG = ("png", "image/png")

    @staticmethod
    def get_supported_extension():
        return [e.value[0] for e in AllowedExtension]

    @staticmethod
    def get_extension_enum_map():
        return dict((e.value[0], e) for e in AllowedExtension)


def get_enum_by_extension(extension):
    global extension_enum_dict_map
    if extension_enum_dict_map is None:
        extension_enum_dict_map = AllowedExtension.get_extension_enum_map()
    return extension_enum_dict_map.get(extension, None)
