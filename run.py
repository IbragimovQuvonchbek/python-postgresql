from functions import read_from_db, read_category_table, write_to_db, update_table, delete_from_table, signup, login, is_superuser

while True:
    print("Exit | Log in | Sign up [0|1|2]")
    option = int(input("option: "))
    current_user = -1
    if option == 0:
        break
    elif option == 2:
        print("==========Sign up==========")
        current_user = signup()
        if current_user != -1:
            option = 1
    if option == 1:
        print("==========Log in==========")
        current_user = login()

    while current_user != -1:
        superuser = is_superuser(current_user)
        if superuser:
            print("Log out | Read | Create | Update | Delete [0|1|2|3|4] ")
        else:
            print("Log out | Read [0|1] ")
        option = int(input("option: "))
        if option == 0:
            break
        elif option == 2 and superuser:
            print("Category table:")
            print(read_category_table())
            name_product = input("name: ")
            price_product = float(input("price: "))
            category_product = int(input("category: "))
            write_to_db(name=name_product, price=price_product, category=category_product)
        elif option == 1:
            print(read_from_db())
        elif option == 3 and superuser:
            print(read_from_db())
            product_id = int(input("id_product: "))
            name_product = input("name: ")
            price_product = float(input("price: "))
            print("Category table:")
            print(read_category_table())
            category_product = int(input("category: "))
            update_table(id_product=product_id, name=name_product, price=price_product, category=category_product)
        elif option == 4 and superuser:
            print(read_from_db())
            product_id = int(input("id_product: "))
            delete_from_table(id_product=product_id)
        else:
            print("incorrect option")
