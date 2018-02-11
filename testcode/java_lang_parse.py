#!/usr/bin/python
# coding=utf-8

import os
import re
import sys

import javalang
from repoze.lru import lru_cache

full_class_name_2_path_dict = {}


class Modifier:
    def __init__(self, value):
        self.value = value

    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'

    def is_public(self, value):
        return self.PUBLIC == value

    def is_private(self, value):
        return self.PRIVATE == value

    def is_protected(self, value):
        return self.PROTECTED == value


class Method:
    def __init__(self, name, modifier, method_invocations, parameters):
        self.name = name
        self.parameters = parameters
        self.modifier = modifier
        self.method_invocations = method_invocations

    # def __str__(self):
    #     return str(self.__dict__)
    #
    # def __eq__(self, other):
    #     return self.__dict__ == other.__dict__

    def is_the_same(self, another):
        # if self.name == another.name and len(self.parameters) ==
        pass

    @staticmethod
    def get_parameters(tree):
        parameters = []
        for path, node in tree.filter(javalang.tree.FormalParameter):
            parameters.append(Parameter.build_from_tree(node))
        return parameters if parameters else None

    @staticmethod
    def get_method_invocation(tree):
        method_invocations = []
        for path, node in tree.filter(javalang.tree.MethodInvocation):
            method_invocations.append(MethodInvocation.build_from_tree(node))
        return method_invocations if method_invocations else None

    @classmethod
    def build_from_tree(cls, tree):
        return cls(tree.name, tree.modifiers, cls.get_method_invocation(tree), cls.get_parameters(tree))


class MethodInvocation:

    def __init__(self, qualifier, member):
        self.qualifier = qualifier
        self.member = member

    @classmethod
    def build_from_tree(cls, tree):
        return cls(tree.qualifier, tree.member)


class Parameter:

    def __init__(self, name, parameter_type):
        self.name = name
        self.parameter_type = parameter_type

    @classmethod
    def build_from_tree(cls, tree):
        return cls(tree.name, tree.type.name)


class Field:

    def __init__(self, modifiers, name, field_type):
        self.modifiers = modifiers
        self.name = name
        self.field_type = field_type

    @classmethod
    def build_from_tree(cls, tree):
        return cls(tree.modifiers, tree.declarators[0].name, tree.type.name)


class Import:

    def __init__(self, path, static, wildcard):
        self.path = path
        self.static = static
        self.wildcard = wildcard


class Class:

    def __init__(self, name, package, imports, extend, implements, methods, fields):
        self.name = name
        self.package = package
        self.imports = imports
        self.extend = extend
        self.implements = implements
        self.methods = methods
        self.fields = fields

    @staticmethod
    def get_name(tree):
        class_name = None
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            class_name = node.name
            break
        for path, node in tree.filter(javalang.tree.EnumDeclaration):
            class_name = node.name
            break
        for path, node in tree.filter(javalang.tree.InterfaceDeclaration):
            class_name = node.name
            break
        if not class_name:
            raise Exception("can not find class name")
        return class_name

    @staticmethod
    def get_methods(tree):
        method_list = []
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            method_list.append(Method.build_from_tree(node))
        return method_list if method_list else None

    def find_methods(self, another=None):
        if not another:
            return self.methods
        return [method for method in self.methods if method == another]

    @staticmethod
    def get_package(tree):
        for path, node in tree.filter(javalang.tree.PackageDeclaration):
            return node.name

    @staticmethod
    def get_imports(tree):
        imports = []
        for path, node in tree.filter(javalang.tree.Import):
            imports.append(Import(node.path, node.static, node.wildcard))
        return imports if imports else None

    @staticmethod
    def get_extend(tree):
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            return node.extends.name if node.extends else None

    @staticmethod
    def get_fields(tree):
        fields = []
        for path, node in tree.filter(javalang.tree.FieldDeclaration):
            fields.append(Field.build_from_tree(node))
        return fields if fields else None

    @staticmethod
    def get_implements(tree):
        implements = []
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            if node.implements:
                for implement in node.implements:
                    implements.append(implement.name)
        return implements if implements else None

    def full_class_name(self):
        return "%s.%s" % (self.package, self.name)

    @classmethod
    def build_from_tree(cls, tree):
        return cls(cls.get_name(tree), cls.get_package(tree), cls.get_imports(tree), cls.get_extend(tree),
                   cls.get_implements(tree),
                   cls.get_methods(tree),
                   cls.get_fields(tree))

    @classmethod
    def build_from_path(cls, java_file_path):
        return Class.build_from_tree(parse_file(java_file_path))


class MethodUsage:
    def __init__(self, clazz, methods, nest_times=0):
        self.clazz = clazz
        self.methods = methods
        self.nest_times = nest_times

    def find(self):
        if not self.methods:
            return
        for method in self.methods:
            print "    " * self.nest_times + self.clazz.full_class_name() + "." + method.name
            self.find_method_usage(method)

    def find_method_usage(self, method):
        for full_class_name, path in class_cache.full_class_name_2_path_dict.iteritems():
            clazz = class_cache.get_class_by_full_class_name(full_class_name)
            method_usage_list = self.do_find_method_usage(clazz, method)
            method_usage = MethodUsage(clazz, method_usage_list, self.nest_times + 1)
            method_usage.find()

    def do_find_method_usage(self, clazz, method):
        if not self.check_import(clazz):
            return
        field_name = self.find_field_name(clazz)
        if not field_name:
            return
        return self.find_method_invoke(field_name, method, clazz)

    # check maybe import
    def check_import(self, clazz):
        new_full_class_name = clazz.full_class_name()
        old_clazz_full_class = self.clazz.full_class_name()
        # same class
        if new_full_class_name == old_clazz_full_class:
            return True
        # same package
        if clazz.package == self.clazz.package:
            return True
        # import directly or import wildcard match
        # todo distinguish static import
        if not clazz.imports:
            return False
        for import_item in clazz.imports:
            if new_full_class_name != import_item.path and not re.search(import_item.path.replace("*", "\*"),
                                                                         old_clazz_full_class):
                continue
            return True

    def find_field_name(self, clazz):
        class_name = self.clazz.name
        fields = clazz.fields
        if fields:
            for field in fields:
                if field.field_type == class_name:
                    return field.name
                return class_name

    def find_method_invoke(self, qualifier, method, clazz):
        method_list = []
        for inner_method in clazz.methods:
            for method_invocation in inner_method.method_invocations:
                # variable name not equal
                if method_invocation.qualifier:
                    if method_invocation.qualifier != qualifier:
                        continue
                # 直接调用方法，没有使用变量名称，有可能是继承、同一个类的方法、静态导入的静态方法
                # todo 暂时只判断是否是内部调用（同一个类的方式）
                elif clazz.name != self.clazz.name:
                    continue
                # todo 只判断方法名称是否相等，后面再细化
                if method_invocation.member != method.name:
                    continue
            method_list.append(inner_method)
        return method_list

    @classmethod
    def build_from_full_class_name(cls, full_class_name):
        clazz = class_cache.get_class_by_full_class_name(full_class_name)
        return cls(clazz, clazz.methods)


class ClassCache:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.full_class_name_2_path_dict = {}

    def load(self):
        for dir_name, dir_names, file_names in os.walk(self.project_dir):
            for file_name in file_names:
                if not file_name.endswith('.java'):
                    continue
                java_file_path = os.path.join(dir_name, file_name)
                self.get_class_from_cache(java_file_path)

    @lru_cache(maxsize=5000)
    def get_class_from_cache(self, path):
        clazz = Class.build_from_path(path)
        full_class_name = clazz.full_class_name()
        if full_class_name not in self.full_class_name_2_path_dict:
            self.full_class_name_2_path_dict[full_class_name] = path
        return clazz

    def get_class_by_full_class_name(self, full_class_name):
        java_file_path = self.full_class_name_2_path_dict[full_class_name]
        return self.get_class_from_cache(java_file_path)


def parse_file(file_path):
    return javalang.parse.parse("\n".join(open(file_path, "r").readlines()))


def main(project_dir, full_class_name):
    # clazz = Class.build_from_tree(parse_file(
    #     "/Users/leo/work/bgp-pack/core/src/main/java/com/aliyun/yundun/bp/core/service/impl/ResourcePackServiceImpl" \
    #     ".java"))
    # print clazz.name
    # load_all_class(project_dir)
    global class_cache
    class_cache = ClassCache(project_dir)
    class_cache.load()
    # methods = find_declare_method_by_class_name(full_class_name)
    # clazz = get_class_by_clazz(full_class_name)
    usage = MethodUsage.build_from_full_class_name(full_class_name)
    usage.find()
    # print_method_invoke_dependency(full_class_name, methods, 0)
    # print dir(1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
