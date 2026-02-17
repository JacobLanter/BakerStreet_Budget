from YNAB import get_ynab_data, print_categories


def main() -> None:
    ynab_data = get_ynab_data()
    print_categories(ynab_data)

if __name__ == "__main__":
    main()

