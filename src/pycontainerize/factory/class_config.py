import os


from constants import (
    OBJ_ATTR_PARENTS,
    OBJ_ATTR_CONFIG_TEMPLATE,
    OBJ_ATTR_NAME,
    BASE_CLASS_NAME,
    CLASSES_DIR,
    CONFIG_TEMPLATES_DIR,
    TYPES_DIR,
    RE_LIST_OF_TYPES,
    INBUILT_TYPES,
    ATTR_EXTENDS,
    ATTR_DEFINITION,
    ATTR_TEMPLATES,
    OBJ_ATTR_TEMPLATES,
    ATTR_NAME,
    ATTR_TYPE,
    ATTR_PERM,
    ATTR_SRC,
)
from object_config import (
    ObjectConfig,
)


class ClassConfig(ObjectConfig):
    '''Configuration object for service and application classes'''

    def __init__(self, class_name, typedef_search_paths=[]):
        config_template_dir = os.path.join(
            CONFIG_TEMPLATES_DIR,
            CLASSES_DIR,
            class_name,
        )
        self.config_template_file = '.'.join((class_name, 'json'))
        self.class_name = class_name
        super(ClassConfig, self).__init__(
            typedef_search_paths=typedef_search_paths + [config_template_dir]
        )

    def initialize(self, obj=None):
        '''Load and parse the configuration template for this object'''
        super(ClassConfig, self).initialize(obj)

    def get_typedef_search_paths(self):
        config_template_dir = os.path.join(
            CONFIG_TEMPLATES_DIR,
            CLASSES_DIR,
            self.class_name,
        )
        return [
            os.path.join(config_template_dir, TYPES_DIR),
            os.path.join(CONFIG_TEMPLATES_DIR, TYPES_DIR)
        ]

    def add_templates(self, templates):
        '''Copies over class template files into the project's directory'''
        config_template_dir = os.path.dirname(self.config_template_path)
        templates_list = getattr(self.obj, OBJ_ATTR_TEMPLATES)
        for template in templates:
            template_file = os.path.join(
                config_template_dir,
                template[ATTR_SRC]
            )
            try:
                template_perm = template[ATTR_PERM]
            except Exception:
                raise
            templates_list.append({
                ATTR_SRC: template_file,
                ATTR_PERM: template_perm,
            })
        setattr(self.obj, OBJ_ATTR_TEMPLATES, templates_list)

    def parse_config_template(self, config_template, obj=None):
        if obj is not None:
            self.obj = obj
        if ATTR_NAME in config_template:
            setattr(self.obj, OBJ_ATTR_NAME, config_template[ATTR_NAME])
        if ATTR_EXTENDS in config_template:
            base_classes = config_template[ATTR_EXTENDS]
        else:
            raise Exception('config_template does not have ATTR_EXTENDS')
        if ATTR_DEFINITION in config_template:
            type_definitions = config_template[ATTR_DEFINITION]
        if ATTR_TEMPLATES in config_template:
            templates = config_template[ATTR_TEMPLATES]
        # Every class config object annotates the self.obj object
        # with attributes it has defined. Attributes are overriden
        # in the order in which classes are specified.
        parents = getattr(self.obj, OBJ_ATTR_PARENTS)
        if self.class_name != BASE_CLASS_NAME and \
                BASE_CLASS_NAME not in parents:
            class_search_path = os.path.join(
                CLASSES_DIR,
                BASE_CLASS_NAME,
            )
            base_class_config = ClassConfig(
                BASE_CLASS_NAME,
                [class_search_path]
            )
            base_class_config.initialize(self.obj)
            parents = getattr(self.obj, OBJ_ATTR_PARENTS)
            parents = parents | set([BASE_CLASS_NAME])
            setattr(self.obj, OBJ_ATTR_PARENTS, parents)
        for base_class in base_classes:
            if base_class in parents:
                continue
            class_search_path = os.path.join(
                CLASSES_DIR,
                base_class,
            )
            base_class_config = ClassConfig(
                base_class,
                [class_search_path]
            )
            base_class_config.initialize(self.obj)
            parents = getattr(self.obj, OBJ_ATTR_PARENTS)
            parents = parents | set([base_class])
            setattr(self.obj, OBJ_ATTR_PARENTS, parents)
        self.add_templates(templates)
        super(ClassConfig, self).parse_config_template(type_definitions)
        config_template = getattr(self.obj, OBJ_ATTR_CONFIG_TEMPLATE)
        setattr(
            self.obj,
            OBJ_ATTR_CONFIG_TEMPLATE,
            config_template + type_definitions,
        )

    def to_python(self):
        '''Traverse the object tree and generate a python representation'''
        json_rep = {}
        for attrib in self.config_template[ATTR_DEFINITION]:
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
