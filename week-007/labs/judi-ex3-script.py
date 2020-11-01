def output_html(*arg):
    print("<body>",*arg,"</body>")
#     return output_html

if __name__ == "__main__":
    import sys
    print(output_html(sys.argv[1],sys.argv[2],sys.argv[3]))
