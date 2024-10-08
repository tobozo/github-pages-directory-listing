#!/usr/local/bin/python3
"""
use os package to iterate through files in a directory
"""
import os
import sys
# import time
import json
import base64
import datetime as dt

with open('/src/icons.json', encoding="utf-8") as json_file:
    data = json.load(json_file)


def main():
    """
    main function
    """
    if len(sys.argv) > 1:
        print("changing directory to " + sys.argv[1])
        # add error handling to chdir
        try:
            os.chdir(sys.argv[1])
        except OSError:
            print("Cannot change the current working Directory")
            sys.exit()
    else:
        print("no directory specified")
        sys.exit()

    for dirname, dirnames, filenames in os.walk('.'):
        if 'index.html' in filenames:
            print("index.html already exists, skipping...")
        else:
            print("index.html does not exist, generating")
            with open(os.path.join(dirname, 'index.html'), 'w', encoding="utf-8") as f:
                f.write("\n".join([
                    get_template_head(dirname),
                    "<tr><th scope=\"row\" ><img style=\"max-width:1rem; margin-right:.25rem\" src=\"" + get_icon_base64("o.folder-home") + "\"/>" +
                        "<a href=\"../\">../</a></th><td>-</td><td>-</td><td>-</td></tr>" if dirname != "." else "",
                        ]))
                #sort dirnames alphabetically
                # dirnames.sort()
                sorted_dirnames = sorted(dirnames, key=str.casefold)

                for subdirname in sorted_dirnames:
                    f.write("<tr><th scope=\"row\"><img style=\"max-width:1rem; margin-right:.25rem\" src=\"" + get_icon_base64("o.folder") + "\"/>" + "<a href=\"" + subdirname + "/\">" +
                            subdirname + "/</a></th><td>-</td><td>-</td><td>-</td></tr>\n")
                #sort filenames alphabetically
                filenames.sort()
                for filename in filenames:
                    path = (dirname == '.' and filename or dirname +
                            '/' + filename)
                    f.write("<tr><th scope=\"row\"><img style=\"max-width:1rem; margin-right:.25rem\" src=\"" + get_icon_base64(filename) + "\"/>" + "<a href=\"" + filename + "\">" + filename + "</a></th><td>" +
                            get_file_size(path) + "</td><td>" + get_file_modified_time(path) + "</td><td>-</td></tr>\n")

                f.write("\n".join([
                    get_template_foot(),
                ]))


def get_file_size(filepath):
    """
    get file size
    """
    size = os.path.getsize(filepath)
    if size < 1024:
        return str(size) + " B"
    elif size < 1024 * 1024:
        return str(round((size / 1024), 2)) + " KB"
    elif size < 1024 * 1024 * 1024:
        return str(round((size / 1024 / 1024), 2)) + " MB"
    else:
        return str(round((size / 1024 / 1024 / 1024), 2)) + " GB"
    return str(size)


def get_file_modified_time(filepath):
    """
    get file modified time
    """
    return dt.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
    # return time.ctime(os.path.getmtime(filepath)).strftime('%X %x')


def get_template_head(foldername):
    """
    get template head
    """
    with open("/src/template/head.html", "r", encoding="utf-8") as file:
        head = file.read()
    head = head.replace("{{foldername}}", foldername)
    return head


def get_template_foot():
    """
    get template foot
    """
    with open("/src/template/foot.html", "r", encoding="utf-8") as file:
        foot = file.read()
    foot = foot.replace("{{buildtime}}", "at " + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return foot

def get_icon_base64(filename):
    """
    get icon base64
    """
    with open("/src/png/" + get_icon_from_filename(filename), "rb") as file:
        return "data:image/png;base64, " + base64.b64encode(file.read()).decode('ascii')


def get_icon_from_filename(filename):
    """
    get icon from filename
    """
    extension = "." + filename.split(".")[-1]
    # extension = "." + extension
    # print(extension)
    for i in data:
        if extension in i["extension"]:
            # print(i["icon"])
            return i["icon"] + ".png"
    # print("no icon found")
    return "unknown.png"


if __name__ == "__main__":
    main()
    # get_icon_from_filename("test.txppt")
