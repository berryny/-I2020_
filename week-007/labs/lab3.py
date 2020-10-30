def series_of_ints(args):
    create_list = args.split(',')
    convert_2_int = [int(integer) for integer in create_list]
    return sum(convert_2_int)
    
if __name__ == "__main__":
    import sys
    print(series_of_ints(sys.argv[1]))
