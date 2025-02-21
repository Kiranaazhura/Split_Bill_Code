from tabulate import tabulate

bill = {
    'Nama menu' : [],
    'Jumlah'    : [],
    'Harga' : [],
    'Sub_Total' : []
}

header = ['Nama menu', 'Jumlah', 'Harga (Rp)', 'Sub_Total (Rp)']

def bills():
    print('Silakan masukkan sesuai dengan struk Anda')
    while True:
        nama = input('Masukkan nama: ') # input nama menu/belanjaan

        while True:
            try:
                jml = int(input('Masukkan jumlahnya: ')) # input jumlahnya dalam angka
            except ValueError:
                print('Masukkan angka!')
                continue
            break
            
        while True:
            try:
                hrg = int(input('Masukkan harganya (tanpa titik): ')) #input harga per item
            except ValueError:
                print('Masukkan angka!')
                continue
            break
            
        # memasukkan semua inputan ke dalam list dalam dict
        bill['Nama menu'].append(nama)
        bill['Jumlah'].append(jml)
        bill['Harga'].append(hrg)
        bill['Sub_Total'].append(jml*hrg)

        print('Bills Anda')
        print(tabulate(bill, headers=header, tablefmt='grid').title())
        
        # validasi apakah masih ada menu/belanjaan yang ingin dimasukkan
        while True:
            tambah = input('Ada lagi? [Y/N]: ' ).upper() 
            if tambah == 'Y':
                break
            elif tambah == 'N':
                return
            else:
                print('Inputan tidak valid, silakan input Y/N')
                print()
                continue


def split():
    while True:
        try:
            layanan = float(input('Masukkan biaya layanan (dalam persen, jika tidak ada input 0): ')) /100 # input biaya layanan 
        except ValueError:
            print('Masukkan angka!')
            continue
        break
    
    while True:
        try:
            tax = float(input('Masukkan pajak(dalam persen, jika tidak ada input 0): ')) / 100 # input pajak 
        except ValueError:
            print('Masukkan angka!')
            continue
        break
    
    while True:
        try:
            dc = float(input('Masukkan discount jika ada (dalam persen, jika tidak ada input 0): ')) / 100 # input diskon
        except ValueError:
            print('Masukkan angka!')
            continue
        break

    b_ly = sum(bill['Sub_Total']) * layanan # menghitung biaya layanan

    # menghitung pajak
    if b_ly == 0:
        pjk = (sum(bill['Sub_Total']) * tax)
    else:
        pjk = (sum(bill['Sub_Total']) + b_ly) * tax

    # menghitung total belanja
    total = sum(bill['Sub_Total']) + b_ly + pjk - dc

    print()
    print('Bills Anda')
    print(tabulate(bill, headers=header, tablefmt='grid').title())
    print(f'Biaya layanan\t: {b_ly}')
    print(f'Pajak\t\t: {pjk}')
    print(f'Total belanja\t: {total}')
    print()

    while True:
        # pilihan menu split bill
        print("\t\nPilihan Split Bills: \n"
              "\t1. Bagi Merata\n"
              "\t2. Bagi Proporsi\n"
            "\t3. Kembali ke Menu utama\n")
        
        try: # agar disaat input menu selain angka yang ada dipilihan/input str program tidak eror
            input_pilih = int(input('Masukkan Menu yang ingin dipilih: '))
        except ValueError:
            print('Inputan tidak valid, silakan masukkan angka (1-3)')
            continue
        print()

        if input_pilih == 1: # jika memilih split bill bagi merata
            try:
                org = int(input('Masukkan jumlah orang: ')) # input jumlah orangnya
                if org <= 0:
                    print('Jumlah orang tidak boleh 0')
                    return
            except ValueError:
                print('Masukkan angka')
                continue
            print()
            print(f'Setiap orang membayar {total/org}') # jumlah yang harus dibayarkan setiap orang

        
        if input_pilih == 2: # jika memilih split bill proporsi
            try:
                org = int(input('Masukkan jumlah orang: ')) # input jumlah orangnya
                if org <= 0:
                    print('Jumlah orang tidak boleh 0')
                    return
            except ValueError:
                print('Masukkan angka')
                continue

            print()
            print('Bills Anda')
            print(tabulate(bill, headers=header, tablefmt='grid', showindex='always').title())
            print(f'Biaya layanan\t: {b_ly}')
            print(f'Pajak\t\t: {pjk}')
            print(f'Total belanja\t: {total}')
            print()

            pesanan = {} # dict kosong untuk menyimpan pesanan per orang

            for i in range(len(bill['Nama menu'])):
                pesanan[i] = {'Total_Pesanan' : 0, 'Pemesan' : []}

            for i in range(org):
                print(f"\nOrang ke-{i+1}:")
                while True:
                    try:
                        mp = int(input('Masukkan index menu yang dibeli (99 untuk selesai): '))
                        if mp == 99:
                            break  # Keluar dari loop input menu

                        if mp in range(len(bill['Nama menu'])):  # Validasi index menu
                            pesanan[mp]['Total_Pesanan'] += 1
                            pesanan[mp]['Pemesan'].append(i)  # Simpan siapa yang memesan menu ini
                        
                        else:
                            print('Menu tidak ada di bills, silakan masukkan index yang benar')

                    except ValueError:
                        print('Masukkan angka yang valid')

            total_per_orang = [0] * org  # Mulai dengan diskon dibagi rata
            total_tagihan = 0

            for index, data in pesanan.items():
                if data['Total_Pesanan'] > 0:
                    harga_per_pemesan = bill['Sub_Total'][index] / data['Total_Pesanan']

                    for pemesan in data['Pemesan']:
                        total_per_orang[pemesan] += harga_per_pemesan 

                    total_tagihan = sum(total_per_orang)
                
            if total_tagihan > 0:
                for i in range(org):
                    total_per_orang[i] += (total_per_orang[i] / total_tagihan) * layanan * total_tagihan
                    total_per_orang[i] += (total_per_orang[i] / total_tagihan) * tax * total_tagihan
                    total_per_orang[i] -= (total_per_orang[i] / total_tagihan) * dc * total_tagihan


            # Membuat list untuk ditampilkan dengan tabulate
            per_org_list = [{'Orang': i + 1, 'Total (Rp)': round(total_per_orang[i], 2)} for i in range(org)]

            # Tampilkan pembagian tagihan
            print("\nPembagian Tagihan per Orang:")
            print(tabulate(per_org_list, headers="keys", tablefmt='grid'))
        
        if input_pilih == 3:
            break

def menu_utama():

    while True:
        print('Program Split Bill')
        print("\tList Menu: \n"
                "\t1. Menginput Struk Menu/Belanja\n"
                "\t2. Split Bill\n"
                "\t3. Exit Program\n")
        
        try:
            main = int(input('Masukkan angka Menu yang ingin dijalankan: '))
        except ValueError:
            print('Input tidak valid, silakan masukkan angka')
            continue

        if main == 1:
            bills()
        
        elif main == 2:
            split()
        
        elif main == 3:
            print('Terimakasih sudah menggunakan program Split Bill ini, Anda sudah keluar')
            break
        
        else:
            print('Pilihan Menu tidak valid')
            continue

menu_utama()
