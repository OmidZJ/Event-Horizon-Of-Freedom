from myproxy.core import main

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 6:
        print("Usage: myproxy <v2ray_file> <results_file> <last_line_file> <output_file>")
        sys.exit(1)

    v2ray_file = sys.argv[1]
    results_file = sys.argv[3]
    last_line_file = sys.argv[4]
    output_file = sys.argv[5]

    main(v2ray_file, results_file, last_line_file, output_file)
