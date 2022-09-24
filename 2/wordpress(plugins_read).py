import csv


def main():
    with open('plugins.csv', 'r') as f:

        reader = csv.reader(f)

        for row in reader:
            for e in row:
                print(e)


if __name__ == '__main__':
    main()
