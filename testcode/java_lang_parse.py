#!/usr/bin/python

import os
import re

import javalang
import sys
from repoze.lru import lru_cache

full_class_name_2_path_dict = {}


def find_method_invoke_in_java_file(clazz, tree, qualifier, method):
    method_list = []
    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        for method_invocation_path, method_invocation_node in node.filter(javalang.tree.MethodInvocation):
            if clazz != find_full_class_name(tree) and not method_invocation_node.qualifier == qualifier:
                continue
            if method and method_invocation_node.member == method:
                method_list.append(node.name)
    return method_list


def find_package(tree):
    for path, node in tree.filter(javalang.tree.PackageDeclaration):
        return node.name


def get_path_from_cache(full_class_name):
    return full_class_name_2_path_dict[full_class_name]


@lru_cache(maxsize=5000)
def get_tree_from_cache(path):
    tree = parse_file(path)
    full_class_name = find_full_class_name(tree)
    if not full_class_name:
        return
    if full_class_name not in full_class_name_2_path_dict:
        full_class_name_2_path_dict[full_class_name] = path
    return tree


def find_class_name(tree):
    class_name = None
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        class_name = node.name
    if class_name:
        return class_name
    for path, node in tree.filter(javalang.tree.EnumDeclaration):
        class_name = node.name
    if class_name:
        return class_name
    for path, node in tree.filter(javalang.tree.InterfaceDeclaration):
        class_name = node.name
    return class_name


def find_import(tree, clazz):
    full_class_name = find_full_class_name(tree)
    if full_class_name == clazz:
        return True
    for path, node in tree.filter(javalang.tree.Import):
        if not clazz == node.path or not re.search(node.path, clazz):
            continue
        return True


def find_declare_method_by_file(java_file_path):
    tree = parse_file(java_file_path)
    return find_declare_method(tree)


def find_declare_method(tree):
    full_class_name = find_full_class_name(tree)
    if not full_class_name:
        return
    method_list = []
    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        method_list.append(node.name)
    return method_list


def find_full_class_name(tree):
    package = find_package(tree)
    if not package:
        return
    class_name = find_class_name(tree)
    if not class_name:
        return
    return package + "." + class_name


def find_full_class_name_by_method(tree, method):
    full_class_name = [find_full_class_name(tree)]
    for path, node in tree:
        for p, n in node.filter(javalang.tree.MethodDeclaration):
            pass
    return full_class_name


def find_field_name(tree, clazz):
    split = clazz.split(".")
    class_name = split[len(split) - 1]
    for path, node in tree.filter(javalang.tree.FieldDeclaration):
        if class_name == node.type.name:
            return node.declarators[0].name
    return class_name


def parse_file(file_path):
    print file_path
    return javalang.parse.parse("\n".join(open(file_path, "r").readlines()))


def find_method_usage(clazz, tree, method):
    if not find_import(tree, clazz):
        return
    qualifier = find_field_name(tree, clazz)
    if not qualifier:
        return
    method_list = find_method_invoke_in_java_file(clazz, tree, qualifier, method)
    if not method_list:
        return
    return method_list


def get_tree_by_clazz(clazz):
    java_file_path = full_class_name_2_path_dict[clazz]
    return get_tree_from_cache(java_file_path)


def find_declare_method_in_dir(clazz):
    tree = get_tree_by_clazz(clazz)
    return find_declare_method(tree)


def find_declare_method_usage(clazz, method):
    total_class_method_list = []
    for full_class_name, path in full_class_name_2_path_dict.iteritems():
        method_list = find_method_usage(clazz, get_tree_by_clazz(full_class_name), method)
        if method_list:
            total_class_method_list.append((full_class_name, method_list))
    return total_class_method_list


def print_method_invoke_dependency(clazz, methods, nest_times):
    for method in methods:
        print "    " * nest_times + clazz + "." + method
        class_methods_list = find_declare_method_usage(clazz, method)
        if not class_methods_list:
            continue
        for class_full_name in class_methods_list:
            print_method_invoke_dependency(class_full_name[0], class_full_name[1], nest_times + 1)


def load_all_class(project_dir):
    for dir_name, dir_names, file_names in os.walk(project_dir):
        for file_name in file_names:
            if not file_name.endswith('.java'):
                continue
            java_file_path = os.path.join(dir_name, file_name)
            get_tree_from_cache(java_file_path)


def main(project_dir, clazz):
    load_all_class(project_dir)
    methods = find_declare_method_in_dir(clazz)
    if not methods:
        print("can not find this class: %s" % clazz)
        return
    print_method_invoke_dependency(clazz, methods, 0)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
