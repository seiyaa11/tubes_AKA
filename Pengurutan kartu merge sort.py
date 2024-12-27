import timeit
import matplotlib.pyplot as plt

def measure_time(func, arr, iterations=10):
    test_array = arr[:]
    time = timeit.timeit(lambda: func(test_array), number=iterations) / iterations
    func(arr)  
    return time

def merge_sort_recursive(arr):
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    merge_sort_recursive(left_half)
    merge_sort_recursive(right_half)

    i = j = k = 0
    while i < len(left_half) and j < len(right_half):
        # Mengambil nilai dan jenis kartu
        _, (suit1, value1) = left_half[i]
        _, (suit2, value2) = right_half[j]
        
        # Membandingkan nilai terlebih dahulu, jika sama bandingkan jenis
        if value1 != value2:
            if value1 < value2:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
        else:  # Nilai sama, bandingkan jenis
            if suit1 < suit2:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1
    
    return arr

def merge_sort_iterative(arr):
    if len(arr) <= 1:
        return arr
        
    width = 1
    n = len(arr)
    
    while width < n:
        for i in range(0, n, 2 * width):
            left = arr[i:min(i + width, n)]
            right = arr[min(i + width, n):min(i + 2 * width, n)]
            
            merged = []
            i_left = i_right = 0
            
            while i_left < len(left) and i_right < len(right):
                # Mengambil nilai dan jenis kartu
                _, (suit1, value1) = left[i_left]
                _, (suit2, value2) = right[i_right]
                
                # Membandingkan nilai terlebih dahulu, jika sama bandingkan jenis
                if value1 != value2:
                    if value1 < value2:
                        merged.append(left[i_left])
                        i_left += 1
                    else:
                        merged.append(right[i_right])
                        i_right += 1
                else:  # Nilai sama, bandingkan jenis
                    if suit1 < suit2:
                        merged.append(left[i_left])
                        i_left += 1
                    else:
                        merged.append(right[i_right])
                        i_right += 1
            
            merged.extend(left[i_left:])
            merged.extend(right[i_right:])
            
            arr[i:i + len(merged)] = merged
            
        width *= 2
    
    return arr

def parse_cards(input_str):
    card_map = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 11, "Q": 12, "K": 13, "A": 14
    }
    suit_map = {
        "wajik": 0, "hati": 1, "keriting": 2, "sekop": 3
    }
    cards = []
    for card in input_str.split(","):
        value, suit = card.strip().split()
        cards.append(((value, suit), (suit_map[suit], card_map[value])))
    return cards

def stringify_cards(cards):
    return [" ".join(card[0]) for card in cards]

if _name_ == "_main_":
    inputs = []
    recursive_times = []
    iterative_times = []

    while True:
        user_input = input("Masukkan nilai dan jenis kartu yang diacak (contoh: '10 wajik, J hati, A sekop', atau ketik '0' untuk berhenti): ")
        if user_input.strip() == "0":
            print("Program dihentikan.")
            break

        cards = parse_cards(user_input)
        print("\nKumpulan kartu yang diacak:", stringify_cards(cards))

        print("\nPendekatan Rekursif:")
        recursive_cards = cards[:]
        recursive_time = measure_time(merge_sort_recursive, recursive_cards)
        print("Hasil setelah rekursif:", stringify_cards(recursive_cards))
        print(f"Waktu eksekusi rekursif: {recursive_time:.6f} detik")

        print("\nPendekatan Iteratif:")
        iterative_cards = cards[:]
        iterative_time = measure_time(merge_sort_iterative, iterative_cards)
        print("Hasil setelah iteratif:", stringify_cards(iterative_cards))
        print(f"Waktu eksekusi iteratif: {iterative_time:.6f} detik")

        inputs.append(len(cards))
        recursive_times.append(recursive_time)
        iterative_times.append(iterative_time)

    plt.figure(figsize=(10, 6))
    plt.plot(inputs, recursive_times, marker="o", label="Rekursif")
    plt.plot(inputs, iterative_times, marker="o", label="Iteratif")
    plt.title("Perbandingan Waktu Eksekusi Merge Sort Rekursif dan Iteratif")
    plt.xlabel("Jumlah Kartu")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.legend()
    plt.grid()
    plt.show()

    print("\nData Waktu Eksekusi:")
    print(f"{'Jumlah Kartu':<15}{'Rekursif (s)':<20}{'Iteratif (s)':<20}")
    for i, count in enumerate(inputs):
        print(f"{count:<15}{recursive_times[i]:<20.6f}{iterative_times[i]:<20.6f}")