# Lớp Equipment đóng vai trò là một Interface chuẩn chung cho toàn bộ các trang bị trong game, định hình khung xương cho các lớp con
# Việc sử dụng @abstractmethod giúp ngăn chặn lỗi TypeError, ép buộc các lớp con kế thừa phải tự ghi đè công thức tính sát thương của riêng mình
# Thứ tự MRO của MagicSword: MagicSword -> Weapon -> MagicMixin -> Equipment -> object
# Ở Chức năng 1, vòng lặp duyệt qua từng món đồ trong danh sách và gọi cú pháp item.calculate_total_damage(), dù mảng này chứa cả Weapon và MagicSword

from abc import ABC, abstractmethod


def get_positive_int(num_input):
    while True:
        try:
            val = int(input(num_input))
            if val <= 0:
                print("Giá trị phải lớn hơn 0! Vui lòng nhập lại.")
                continue
            return val
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ!")


class Equipment(ABC):
    @abstractmethod
    def calculate_total_damage(self):
        pass


class Weapon(Equipment):
    def __init__(self, name, base_damage, upgrade_level=0):
        self.name = name
        self.base_damage = base_damage
        self.upgrade_level = upgrade_level

    def calculate_total_damage(self):
        return self.base_damage + (self.upgrade_level * 10)

    def __gt__(self, other):
        if not isinstance(other, Equipment):
            raise TypeError("Chỉ có thể so sánh giữa các trang bị!")
        return self.calculate_total_damage() > other.calculate_total_damage()

    def __add__(self, other):
        if not isinstance(other, Equipment):
            raise TypeError("Chỉ có thể dung hợp giữa các trang bị!")

        new_name = f"Fusion({self.name} + {other.name})"
        new_base_damage = self.base_damage + other.base_damage
        new_upgrade_level = self.upgrade_level + other.upgrade_level

        return Weapon(new_name, new_base_damage, new_upgrade_level)


class MagicMixin:
    def __init__(self, magic_power):
        self.magic_power = magic_power

    def cast_glow(self):
        return f"{self.name} đang phát ra luồng ánh sáng huyền bí!"


class MagicSword(Weapon, MagicMixin):
    def __init__(self, name, base_damage, upgrade_level, magic_power):
        Weapon.__init__(self, name, base_damage, upgrade_level)
        MagicMixin.__init__(self, magic_power)

    def calculate_total_damage(self):
        return Weapon.calculate_total_damage(self) + self.magic_power


def show_inventory(inventory):
    if len(inventory) == 0:
        print("Kho vũ khí hiện đang trống.")
        print("Vui lòng rèn vũ khí bằng Chức năng 2 hoặc Chức năng 3.")
        return

    print("\n--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---")
    print(f"{'STT':<6} | {'Tên vũ khí':<25} | {'Loại':<15} | {'Cấp':<8} | Sát thương tổng")
    print("-" * 80)
    for idx, item in enumerate(inventory, start=1):
        weapon_type = item.__class__.__name__
        damage = item.calculate_total_damage()
        print(
            f"{idx:<6} | {item.name:<25} | {weapon_type:<15} | {item.upgrade_level:<8} | {damage}")


def craft_weapon(inventory):
    print("\n--- RÈN VŨ KHÍ VẬT LÝ ---")
    name = input("Nhập tên vũ khí: ").strip().title()
    base_damage = get_positive_int("Nhập sát thương gốc: ")
    upgrade_level = get_positive_int("Nhập cấp cường hóa: ")

    new_wp = Weapon(name, base_damage, upgrade_level)
    inventory.append(new_wp)

    print("\n>> Rèn vũ khí vật lý thành công!")
    print(f"Tên vũ khí: {new_wp.name}")
    print("Loại: Weapon")
    print(f"Cấp cường hóa: {new_wp.upgrade_level}")
    print(f"Sát thương tổng: {new_wp.calculate_total_damage()}")


def craft_magic_sword(inventory):
    print("\n--- RÈN KIẾM MA THUẬT ---")
    name = input("Nhập tên kiếm ma thuật: ").strip().title()
    base_damage = get_positive_int("Nhập sát thương gốc: ")
    upgrade_level = get_positive_int("Nhập cấp cường hóa: ")
    magic_power = get_positive_int("Nhập sức mạnh phép thuật: ")

    new_ms = MagicSword(name, base_damage, upgrade_level, magic_power)
    inventory.append(new_ms)

    print("\n>> Rèn kiếm ma thuật thành công!")
    print(f"{new_ms.cast_glow()}")
    print(f"Tên vũ khí: {new_ms.name}")
    print("Loại: MagicSword")
    print(f"Cấp cường hóa: {new_ms.upgrade_level}")
    print(f"Sát thương gốc: {new_ms.base_damage}")
    print(f"Sức mạnh phép thuật: {new_ms.magic_power}")
    print(f"Sát thương tổng: {new_ms.calculate_total_damage()}")


def compare_weapons(inventory):
    print("\n--- THẨM ĐỊNH VŨ KHÍ ---")
    if len(inventory) < 2:
        print("Cần ít nhất 2 vũ khí trong kho để thẩm định!")
        return

    wp1 = inventory[0]
    wp2 = inventory[1]
    print(
        f"Vũ khí thứ nhất:\n{wp1.name} | Loại: {wp1.__class__.__name__} | Sát thương: {wp1.calculate_total_damage()}\n")
    print(
        f"Vũ khí thứ hai:\n{wp2.name} | Loại: {wp2.__class__.__name__} | Sát thương: {wp2.calculate_total_damage()}\n")

    if wp1 > wp2:
        print(f"Kết quả: {wp1.name} mạnh hơn {wp2.name}.")
    elif wp2 > wp1:
        print(f"Kết quả: {wp2.name} mạnh hơn {wp1.name}.")
    else:
        print("Kết quả: Hai vũ khí có sức mạnh ngang nhau.")


def fuse_weapons(inventory):
    print("\n--- DUNG HỢP VŨ KHÍ ---")
    if len(inventory) < 2:
        print("Cần ít nhất 2 vũ khí trong kho để dung hợp!")
        return

    print("Đang dung hợp 2 vũ khí đầu tiên trong kho...\n")
    wp1 = inventory[0]
    wp2 = inventory[1]
    print(
        f"Vũ khí 1: {wp1.name} | Cấp: {wp1.upgrade_level} | Sát thương: {wp1.calculate_total_damage()}")
    print(
        f"Vũ khí 2: {wp2.name} | Cấp: {wp2.upgrade_level} | Sát thương: {wp2.calculate_total_damage()}")

    new_weapon = wp1 + wp2

    inventory.pop(0)
    inventory.pop(0)
    inventory.append(new_weapon)

    print("\n>> Dung hợp vũ khí thành công!")
    print(f"Đã xóa khỏi kho: {wp1.name}")
    print(f"Đã xóa khỏi kho: {wp2.name}")
    print(f"\nVũ khí mới: {new_weapon.name}")
    print(f"Loại: {new_weapon.__class__.__name__}")
    print(f"Cấp cường hóa: {new_weapon.upgrade_level}")
    print(f"Sát thương tổng: {new_weapon.calculate_total_damage()}")


def main():
    inventory = []
    while True:
        print("\n===== LÒ RÈN VŨ KHÍ RIKKEI STUDIOS ===================")
        print("1. Xem kho vũ khí & Sát thương tổng")
        print("2. Rèn Vũ khí Vật lý (Tạo Weapon)")
        print("3. Rèn Kiếm Ma Thuật (Tạo MagicSword)")
        print("4. Thẩm định vũ khí (So sánh lớn hơn)")
        print("5. Dung hợp vũ khí (Cộng dồn cấp độ)")
        print("6. Thoát game")
        print("======================================================")
        choice = input("Chọn chức năng (1-6): ").strip()

        if choice == "1":
            show_inventory(inventory)
        elif choice == "2":
            craft_weapon(inventory)
        elif choice == "3":
            craft_magic_sword(inventory)
        elif choice == "4":
            compare_weapons(inventory)
        elif choice == "5":
            fuse_weapons(inventory)
        elif choice == "6":
            print("Thoát Lò Rèn. Hẹn gặp lại Anh hùng!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 6!")


if __name__ == "__main__":
    main()
