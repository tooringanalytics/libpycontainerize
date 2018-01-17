import json
import os
import shutil

from class_config import ClassConfig
from constants import ATTR_CTX
from constants import ATTR_DEFINITION
from constants import ATTR_DST
from constants import ATTR_EXTENDS
from constants import ATTR_NAME
from constants import ATTR_PERM
from constants import ATTR_SRC
from constants import ATTR_TEMPLATES
from constants import ATTR_TYPE
from constants import BASE_CLASS_NAME
from constants import CLASSES_DIR
from constants import CONFIG_TEMPLATES_DIR
from constants import INBUILT_TYPES
from constants import OBJ_ATTR_CONFIG_TEMPLATE
from constants import OBJ_ATTR_NAME
from constants import OBJ_ATTR_PARENTS
from constants import OBJ_ATTR_TEMPLATES
from constants import RE_LIST_OF_TYPES
from constants import TYPES_DIR
from object_config import ObjectProto


class LeafNodeConfig(ClassConfig):
    def __init__(self,
                 name,
                 extends=[],
                 definitions=[],
                 templates=[],
                 typedef_search_paths=[]):
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
        setattr(self.obj, OBJ_ATTR_NAME, self.class_name)
        self.extends = extends
        self.type_definitions = definitions
        self.templates = templates
        self.config_template = {
            ATTR_NAME: self.class_name,
            ATTR_EXTENDS: self.extends,
            ATTR_DEFINITION: self.type_definitions,
            ATTR_TEMPLATES: self.templates,
        }

    def parse_config_template(self, config_template, obj=None):
        if obj is not None:
            self.obj = obj
        setattr(self.obj, OBJ_ATTR_NAME, self.class_name)
        setattr(self.obj, OBJ_ATTR_PARENTS, set([]))
        setattr(self.obj, OBJ_ATTR_CONFIG_TEMPLATE, [])
        base_classes = self.extends
        type_definitions = self.type_definitions
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
            parents = getattr(self.obj, OBJ_ATTR_PARENTS)
            parents = parents | set([BASE_CLASS_NAME])
            setattr(self.obj, OBJ_ATTR_PARENTS, parents)
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
            parents = getattr(self.obj, OBJ_ATTR_PARENTS)
            parents = parents | set([base_class])
            setattr(self.obj, OBJ_ATTR_PARENTS, parents)
        self.parse_attributes(type_definitions)
        config_template = getattr(self.obj, OBJ_ATTR_CONFIG_TEMPLATE)
        setattr(
            self.obj,
            OBJ_ATTR_CONFIG_TEMPLATE,
            config_template + type_definitions,
        )
        setattr(self.obj, OBJ_ATTR_NAME, self.class_name)

    def get_templates(self):
        return getattr(self.obj, OBJ_ATTR_TEMPLATES)

    def get_relative_path(self, abs_path):
        class_search_path = os.path.join(
            CONFIG_TEMPLATES_DIR,
            CLASSES_DIR,
        )
        common_prefix = os.path.commonprefix((class_search_path, abs_path))
        rel_path = abs_path[len(common_prefix):]
        # remove leading <class-name>/templates prefix
        rel_path = os.path.join(*(rel_path.split(os.path.sep)[3:]))
        return rel_path

    def copy_templates(self, node_root_dir):
        templates_dir = os.path.join(
            node_root_dir,
            ATTR_TEMPLATES,
        )
        templates_file = os.path.join(
            node_root_dir,
            '.'.join((ATTR_TEMPLATES, 'json'))
        )
        templates = self.get_templates()
        for template in templates:
            src = template[ATTR_SRC]
            src_relative_path = self.get_relative_path(src)
            dst = os.path.join(
                templates_dir,
                src_relative_path
            )
            dst_dirname = os.path.dirname(dst)
            if not os.path.exists(dst_dirname):
                os.makedirs(dst_dirname)
            shutil.copyfile(src, dst)
        new_templates = []
        for template in templates:
            new_template = {}
            new_template[ATTR_SRC] = os.path.join(
                ATTR_TEMPLATES,
                self.get_relative_path(src)
            )
            new_template[ATTR_PERM] = template[ATTR_PERM]
            if ATTR_DST in template:
                new_template[ATTR_DST] = template[ATTR_DST]
            if ATTR_CTX in template:
                new_template[ATTR_CTX] = template[ATTR_CTX]
            new_templates.append(new_template)
        with open(templates_file, 'w') as fp:
            json.dump(
                new_templates,
                fp,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )

    def to_python(self):
        json_rep = {}
        for attrib in getattr(self.obj, OBJ_ATTR_CONFIG_TEMPLATE):
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
