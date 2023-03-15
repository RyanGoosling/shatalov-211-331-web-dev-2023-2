# Класс Vector3D 
# Экземляр класса задается тройкой координат в трехмерном пространстве (x,y,z).
# Обязательно должны быть реализованы методы:
# – приведение вектора к строке с выводом координат (метод __str __),
# – сложение векторов оператором `+` (метод __add__),
# – вычитание векторов оператором `-` (метод __sub__),
# – скалярное произведение оператором `*` (метод __mul__),
# – умножение и деление на скаляр операторами `*` и `/` (метод __mul__ и __truediv__),
# – векторное произведение оператором `@` (метод __matmul__),
# – вычисление длины вектора методом `norm`.

# Пример
#  v1 = Vector3D(4, 1, 2)
#  print(v1)
#  v2 = Vector3D()
#  v2.read()
#  v3 = Vector3D(1, 2, 3)
#  v4 = v1 + v2
#  print(v4)
#  a = v4 * v3
#  print(a)
#  v4 = v1 * 10
#  print(v4)
#  v4 = v1 @ v3
#  print(v4) 

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, v2):
        return Vector3D(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def __sub__(self, v2):
        return Vector3D(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def __mul__(self, v2):
        if isinstance(v2, Vector3D):
            return self.x * v2.x + self.y * v2.y + self.z * v2.z
        else: 
            return Vector3D(self.x * v2, self.y * v2, self.z * v2)

    def __truediv__(self, n):
         return Vector3D(self.x / n, self.y / n, self.z / n)

    def __matmul__(self, v2):
        return Vector3D(self.y * v2.z - self.z*v2.y, self.z*v2.x - self.x*v2.z, self.x*v2.y - self.y*v2.x)

    def norm(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2)**0.5

v1 = Vector3D(4, 1, 2)
v2 = Vector3D(1, 2, 3)
print(v1 * v2)
print(v1 * 2)
print(v1 / 2)
v3 = v1 @ v2
print(v3)
print(v3 * v1)
print(v3 * v2)
print(v1.norm())

# i  j  k   
# a1 a2 a3  x y z
# b1 b2 b3

# i * (a2*b3 - a3*b2) + j * (a3*b1 - a1*b3) + k * (a1*b2 - a2*b1) 