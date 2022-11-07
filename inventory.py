from tabulate import tabulate


def main():
    shoes_list = []

    class Shoes:
        def __init__(self, country, code, product, cost, quantity):
            self.country = country
            self.code = code
            self.product = product
            self.cost = cost
            self.quantity = quantity

        def get_cost(self, name_shoe):
            '''return cost of shoe'''
            counter = 0
            for shoe in shoes_list:
                counter += 1
                if name_shoe.lower() == str(shoe.product).lower():
                    print(f'Cost of {shoe.product} is R {shoe.cost}\n')
                    return ""
                if counter == len(shoes_list):
                    print('Cannot Find item in the inventory. Check spelling and try again.\n')
                    return ""

        def get_quantity(self, high_or_low):
            '''return quantity of shoes
            returns lowest and highest quantities
            '''
            #global shoe
            line_num = 0
            quantityandproduct_list = []
            for shoe in shoes_list:
                line_num += 1
                if len(shoes_list)+1 > line_num > 1:
                    quantityandproduct_list.append(f'{int(shoe.quantity)},{shoe.product}')
                if line_num == len(shoes_list)+1:
                    break

            sorted_list = []
            for shoes in quantityandproduct_list:
                shoes = shoes.split(",")
                shoes[0] = int(shoes[0])
                sorted_list.append(shoes)
            sorted_list.sort()

            if high_or_low == 0:
                print(f'The product with the lowest quantity is:\t{sorted_list[0][1]}\nQTY:\t{sorted_list[0][0]}\n')
                re_stock(sorted_list)
            else:
                print(f'The {sorted_list[len(sorted_list)-1][1]} is now on SALE!!!')
                return ""

        def __str__(self):
            return""

    def read_shoes_data():
        '''
        open inventory.txt file
        read data from file and create shoe objects
        append objects to shoe list
        one line in file shows data to create on object
        try except for error handling
        '''

        try:
            shoes_list.clear()
            inventory = open("inventory.txt", 'r')
            lines = inventory.readlines()
            for line in lines:
                    line = line.split(",")
                    shoe = Shoes(line[0],line[1],line[2],line[3],line[4])
                    shoes_list.append(shoe)
            return ""

        except FileNotFoundError:
            print("Inventory.txt could not be located or does not exist!")
            main()

    def capture_shoes(country, code, product, cost, quantity):
        '''
        allow user to capture data about shoe
        use data to cread a shoe object
        append object inside shoe list
        '''
        new_shoe = f'{country},{code},{product},{cost},{quantity}'
        new_shoe = new_shoe.split(',')
        new_shoe_obj = Shoes(country,code,product,cost,quantity)
        shoes_list.append(new_shoe_obj)
        with open('inventory.txt', 'a') as inventory:
            inventory.write(f'\n{new_shoe[0]},{new_shoe[1]},{new_shoe[2]},{new_shoe[3]},{new_shoe[4]}')
        return ""

    def view_all():
        '''
        iterate over all shoes in shoe list
        print details of shoes that is returns from thee __str__ function
        can organise data in a table format using python tabulate
        '''
        shoe_list_4_display = []
        for shoe in shoes_list:
            b = f'{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}'
            a = b.split(',')
            shoe_list_4_display.append(a)
        print(tabulate(shoe_list_4_display, headers='firstrow', tablefmt='fancy_grid',
                       showindex=range(1, len(shoe_list_4_display))))

    def re_stock(sorted_list):
        '''
        find shoe object with the lowest quantity
        ask user if he wants to add to the quantity and then update it
        quantity should be updated in the file for this shoe
        '''
        shoe_num = 0
        quantity_update = input('Would you like to add more of this product into the inventory? (yes/no):\t')
        if quantity_update.lower() == 'yes':
            quantity_added = int(input('How many of the product would you like to add?:\t'))

            for shoe in shoes_list:
                shoe_num += 1
                if shoe.product == sorted_list[0][1]:
                    print(shoe.product)
                    new_quantity = int(shoes_list[shoe_num-1].quantity) + quantity_added
                    with open('inventory.txt', 'r') as read_inventory:
                        lines = read_inventory.readlines()
                    line_to_delete = 1
                    with open('inventory.txt', 'w') as write_inventory:
                        for line in lines:
                            line_to_delete +=1
                            if line != f'{shoes_list[shoe_num-1].country},{shoes_list[shoe_num-1].code},' \
                                       f'{shoes_list[shoe_num-1].product},{shoes_list[shoe_num-1].cost},' \
                                       f'{shoes_list[shoe_num-1].quantity}':
                                write_inventory.write(line)
                        quantity = new_quantity
                        write_inventory.write(f'\n{shoes_list[shoe_num-1].country},{shoes_list[shoe_num-1].code},'
                                            f'{shoes_list[shoe_num-1].product},'
                                            f'{shoes_list[shoe_num-1].cost},{quantity}')
            read_shoes_data()
            print('\nInventory has been updated!!\n')
            return ''

        if quantity_update.lower() == 'no':
            main()
            return ''

    def search_shoe(shoe_code):
        '''
        search for a shoe from the list using shoe code and return object
        print object
        '''
        single_item_display_list = []
        line_counter = 0
        header = 'Country,Code,Product,Cost,Quantity'
        header = header.split(',')
        single_item_display_list.append(header)

        for shoe in shoes_list:
            line_counter += 1
            if shoe.code == shoe_code:
                single_item_display_list.append((f'{shoe.country},{shoe.code},{shoe.product}'
                                                f',{shoe.cost},{shoe.quantity}'.split(',')))
                print(tabulate(single_item_display_list, headers='firstrow', tablefmt='fancy_grid'))
                return ""
            if line_counter == len(shoes_list):
                print("Shoe not inventory. Check for spelling Errors and try again")
                return""

    def value_per_item():
        '''
        calculate the total value of each item
        value = cost * quantity
        print in console
        replace headers of table
        '''
        list_with_stock_value = []
        total_stock_value = 0
        header = 'Country,Code,Product,Cost,Quantity,Stock Value'
        header = header.split(',')
        list_with_stock_value.append(header)

        item_counter = 0
        for shoe in shoes_list:
            item_counter += 1
            if item_counter > 1:
                shoe_value = int(shoe.cost) * int(shoe.quantity)
                line = f'{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity},R {shoe_value}'
                total_stock_value += shoe_value
                line = line.split(',')
                list_with_stock_value.append(line)

        footer = f'-,-,-,-,Total Stock Value,R {total_stock_value}'
        footer = footer.split(',')
        list_with_stock_value.append(footer)

        print(tabulate(list_with_stock_value, headers='firstrow', tablefmt='fancy_grid',
                      showindex=range(1, len(list_with_stock_value))))
        list_with_stock_value.remove(footer)

        return ""

    def highest_qty():
        '''
        determine product with highest quantity
        print item as being for sale
        '''
        print(Shoes.get_quantity(shoes_list,high_or_low=1))
        return ""

    while True:
        main_menu = input(f'what would you like to do:'
                          f'\n\nread\t-\treads data from inventory file(Recommended before any application use)'
                          f'\nadd\t\t-\tallows user to add item to inventory'
                          f'\nview\t-\tallows user to view all items in inventory'
                          f'\nrestock\t-\tallows user to restock on items that are running low'
                          f'\nsearch\t-\tallows user to search data of items in the inventory'
                          f'\nvalue\t-\tallows user to view stock value of all items'
                          f'\nsale\t-\tdisplays item that is on sale at the moment'
                          f'\ncost\t-\tdisplays cost of shoe\n\n:\t')

        if main_menu.lower() == 'read':
            print('\nDate from the inventory file has been successfully read!!')
            print(read_shoes_data())

        if main_menu.lower() == 'add':
            '''
            takes data from user
            split data into seprate attributes of an objects
            '''

            country, code, product, cost, quantity = input(f'\nFor capture to be successful please input the below data'
                                                           f' (Separate each value with a comma)'
                                                           f'\n\nCountry, Code, Product, Cost, quantity:\n:\t'
                                                           ).split(',')
            cost = int(cost)
            quantity = int(quantity)
            capture_shoes(country, code, product, cost, quantity)
            print("\nShoe successfully added to Inventory!!\n")

        if main_menu.lower() == 'view':
            '''
            Displays list of all the shoes in the inventory
            '''
            view_all()

        if main_menu.lower() == 'restock':
            '''
            allows user to add to the stock of the shoe with the lowest quantity
            '''
            Shoes.get_quantity(shoes_list,high_or_low=0)

        if main_menu.lower() == 'search':
            '''
            requests shoe code
            displays shoe related to code
            '''
            shoe_code = input('Enter the code of the shoe you would like to display(case-sensitive):\t')
            print(search_shoe(shoe_code))

        if main_menu.lower() == 'value':
            ''' value = cost * quantity
            Displays entire list of shoes along with stock value
            '''
            print(value_per_item())

        if main_menu.lower() == 'sale':
            '''
            displays the shoe with the highest quantity
            '''
            print(highest_qty())

        if main_menu.lower() == 'cost':
            '''
            displays cost of requested shoe
            '''
            name_shoe = input("Enter the name of the shoe you'd like to search the cost of\n\n:")
            print(Shoes.get_cost(shoes_list,name_shoe))

main()
