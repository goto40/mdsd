def get_packages(model):
    pkgs = []
    p = model
    while (p.package is not None):
        p = p.package
        pkgs.append(p)
    return pkgs

def get_package_names(model):
    return list(map(lambda x:x.name, get_packages(model)))
