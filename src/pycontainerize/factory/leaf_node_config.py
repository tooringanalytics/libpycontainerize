import os


from constants import (
    BASE_CLASS_NAME,
    CLASSES_DIR,
    CONFIG_TEMPLATES_DIR,
    TYPES_DIR,
    RE_LIST_OF_TYPES,
    INBUILT_TYPES,
    ATTR_NAME,
    ATTR_EXTENDS,
    ATTR_DEFINITION,
    ATTR_TEMPLATES,
    ATTR_TYPE,
)
from object_config import (
    ObjectProto,
)
from class_config import (
    ClassConfig,
)


class LeafNodeConfig(ClassConfig):
    def __init__(self, name, extends=[], typedef_search_paths=[]):
        if not typedef_search_paths:
            self.typedef_search_paths = [
                os.path.join(CONFIG_TEMPLATES_DIR, TYPES_DIR),
                os.path.join(CONFIG_TEMPLATES_DIR, CLASSES_DIR),
                CONFIG_TEMPLATES_DIR,
            ]
        else:
            self.typedef_search_paths = typedef_search_paths
        self.class_name = name
        self.obj = ObjectProto()
        self.obj.name = self.class_name
        self.extends = extends
        self.config_template = {
            ATTR_NAME: self.class_name,
            ATTR_EXTENDS: self.extends,
            ATTR_DEFINITION: [],
            ATTR_TEMPLATES: [],
        }

    def parse_config_template(self, config_template, obj=None):
        if obj is not None:
            self.obj = obj
        setattr(self.obj, ATTR_NAME, self.class_name)
        base_classes = self.extends
        # Every class config object annotates the self.obj object
        # with attributes it has defined. Attributes are overriden
        # in the order in which classes are specified.
        if self.class_name != BASE_CLASS_NAME:
            class_search_path = os.path.join(
                CONFIG_TEMPLATES_DIR,
                CLASSES_DIR,
                BASE_CLASS_NAME,
            )
            base_class_config = ClassConfig(
                BASE_CLASS_NAME,
                [class_search_path]
            )
            base_class_config.initialize(self.obj)
        for base_class in base_classes:
            class_search_path = os.path.join(
                CONFIG_TEMPLATES_DIR,
                CLASSES_DIR,
                base_class,
            )
            base_class_config = ClassConfig(
                base_class,
                [class_search_path]
            )
            base_class_config.initialize(self.obj)
        self.parse_attributes(config_template)
        setattr(self.obj, ATTR_DEFINITION, [])
        setattr(self.obj, ATTR_EXTENDS, base_classes)

    def to_python(self):
        json_rep = {}
        for attrib in self.config_template:
            if hasattr(self.obj, attrib[ATTR_NAME]):
                if attrib[ATTR_TYPE] in INBUILT_TYPES:
                    json_rep[attrib[ATTR_NAME]] = getattr(
                        self.obj,
                        attrib[ATTR_NAME]
                    )
                elif RE_LIST_OF_TYPES.match(attrib[ATTR_TYPE]):
                    lst = getattr(
                        self.obj,
                        attrib[ATTR_NAME]
                    )
                    json_rep[attrib[ATTR_NAME]] = [
                        obj.to_python()
                        for obj in lst
                    ]
                else:
                    json_rep[attrib[ATTR_NAME]] = getattr(
                        self.obj, attrib[ATTR_NAME]
                    ).to_python()
        return json_rep
