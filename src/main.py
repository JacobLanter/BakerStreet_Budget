# Will contain main function to run the application
from YNAB import get_ynab_data

def main() -> None:
    ynab_data = get_ynab_data()
    print(ynab_data)


if __name__ == "__main__":
    main()

