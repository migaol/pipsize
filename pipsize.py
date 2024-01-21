# Short Python script to find the size of python modules
# Attribution: https://stackoverflow.com/a/67914559/16063921

import os, pkg_resources, argparse

def calc_container(path: os.PathLike) -> int:
    """Find the bytes size of a package"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def format_bytes(nbytes: int) -> str:
    """Convert bytes to shorthand formatted string"""
    units = ['B','KB','MB','GB']
    base = 1024

    idx = 0
    size = float(nbytes)

    while size >= base and idx < len(units) - 1:
        size /= base
        idx += 1

    return f"{size:.3f} {units[idx]}"

def main(args: argparse.Namespace) -> None:
    dists = [d for d in pkg_resources.working_set]
    sizes = [(dist, calc_container(os.path.join(dist.location, dist.project_name))) for dist in dists]
    
    if args.sortby == 'size':
        sizes.sort(key=lambda x: x[1], reverse=(args.order == 'desc'))
    elif args.sortby == 'name':
        sizes.sort(key=lambda x: x[0].project_name.lower(), reverse=(args.order == 'desc'))

    max_name_length = max(len(dist.project_name) for dist,size in sizes if size > 1.0)
    max_name_length = max(len("Package"), max_name_length)
    max_version_length = max(len(str(dist.version)) for dist,size in sizes if size > 1.0)
    max_version_length = max(len("Version"), max_version_length)

    print(f"{'Package'.ljust(max_name_length)} {'Version'.ljust(max_version_length)} Size")
    print('-'*(max_name_length+max_version_length+15))
    for dist, size in sizes:
        if size > 1.0:
            print(f"{dist.project_name.ljust(max_name_length)} {dist.version.ljust(max_version_length)} {format_bytes(size)}")

    print('-'*(max_name_length+max_version_length+15))
    total_size = sum(size for _,size in sizes if size > 1.0)
    print(f"SUMMARY: {len([s for _,s in sizes if s>1.0])} packages, totaling {format_bytes(total_size)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='View Python package sizes')
    parser.add_argument('--sortby', choices=['size', 'name'], default='size', help='Sort by size/name (default: size)')
    parser.add_argument('--order', choices=['asc', 'desc'], default='desc', help='Sort order (default: desc)')
    args = parser.parse_args()
    main(args)