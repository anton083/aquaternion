
import math
import numpy as np

pi = math.pi

def validate_types(array, types):
    return (False not in [isinstance(x, types) for x in array])

class Quaternion:
    """
    Create a Quaternion number with a 4-dimensional vector [w, x, y, z]
    """
    
    def __init__(self, *args):
        
        match len(args):
            case 1:
                arg = args[0]
                if isinstance(arg, (np.ndarray, list, tuple)):
                    vector = arg
                    match len(vector):
                        case 3:
                            self.vector = np.array([0, *vector], dtype=np.float64)
                        case 4:
                            self.vector = np.array(vector, dtype=np.float64)
                elif isinstance(arg, self.__class__):
                    self.vector = np.array(arg.vector, dtype=np.float64)
            case 3:
                if validate_types(args, (float, int)):
                    self.vector = np.array([0, *args], dtype=np.float64)
            case 4:
                if validate_types(args, (float, int)):
                    self.vector = np.array(args, dtype=np.float64)
    
    
    def __repr__(self):
        return f'Q({self.vector})'

    def __str__(self):
        return f'({self.w:.3f} {self.x:+.3f}i {self.y:+.3f}j {self.z:+.3f}k)'
    
    @property
    def w(self) -> float:
        return self.vector[0]
    @w.setter
    def w(self, value):
        self.vector[0] = value

    @property
    def x(self) -> float:
        return self.vector[1]
    @x.setter
    def x(self, value):
        self.vector[1] = value

    @property
    def y(self) -> float:
        return self.vector[2]
    @y.setter
    def y(self, value):
        self.vector[2] = value

    @property
    def z(self) -> float:
        return self.vector[3]
    @z.setter
    def z(self, value):
        self.vector[3] = value


    @property
    def norm(self) -> float:
        return np.linalg.norm(self.vector)
    @norm.setter
    def norm(self, new_norm):
        self.vector = self.normalized.vector * new_norm
        
    @property
    def normalized(self):
        if (norm := self.norm) == 0:
            return self
        return self.__class__(self.vector/norm)
    
    def normalize(self):
        self.vector = self.normalized.vector
        return self
    
    @property
    def conjugate(self):
        return self.__class__(self.w, -self.x, -self.y, -self.z)
    
    @property
    def square_sum(self)  -> float:
        return sum((x**2 for x in self.vector))

    @property
    def inverse(self):
        return self.conjugate/self.square_sum
    
    reciprocal = inverse
        
    
    def __add__(self, other):
        
        if isinstance(other, (float, int)):
            return self.__class__(self.w+other, self.x, self.y, self.z)
        
        if isinstance(other, self.__class__):
            return self.__class__(self.w+other.w, self.x+other.x, self.y+other.y, self.z+other.z)

        return NotImplemented
    
    __radd__ = __add__
    
    def __neg__(self):
        return self.__class__(-self.w, -self.x, -self.y, -self.z)
    
    def __sub__(self, other):
        return self+(-other)
    
    def __rsub__(self, other):
        return (-self)+other
    
    def __mul__(self, other):
        
        if isinstance(other, self.__class__):
            return self.__class__(
                self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
                self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
                self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x,
                self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w,
            )
        
        try:
            return self.__class__(self.vector*other)
        except:
            return NotImplemented
    
    def __rmul__(self, other):
        
        try:
            return self.__class__(other*self.vector)
        except:
            return NotImplemented


    def __truediv__(self, other):
        
        if isinstance(other, (float, int)):
            return self.__class__(self.vector/other)
        
        if isinstance(other, self.__class__):
            return self * other.inverse
        
        return NotImplemented
        
    def __rtruediv__(self, other):
        
        if isinstance(other, (float, int)):
            return self.__class__(self.vector/other)
        
        if isinstance(other, self.__class__):
            return other.inverse * self
        
        return NotImplemented
    

    def __len__(self):
        return 4

    def __getitem__(self, index):
        return self.vector[index]
    
    def __setitem__(self, index, value):
        self.vector[int(index)] = float(value)


    def __iter__(self):
        return iter(self.vector)
    
    @property
    def components(self) -> list[float]:
        return [self.w, self.x, self.y, self.z]

    def copy(self):
        return self.__class__(self.components)
    
    @property
    def qvector(self):
        return self.__class__(0, self.x, self.y, self.z)
    
    @property
    def vector3(self):
        return self.vector[1:4]
    
    
    def rotated(self, axis, angle):
        q = math.cos(angle/2) + axis.normalized*math.sin(angle/2)
        vector = (q*self*q.conjugate).vector
        return self.__class__(vector)
    
    def rotate(self, axis, angle):
        self.vector = self.rotated(axis, angle).vector.copy()
        return self
    
    
    def morphed(self, i_prime, j_prime, k_prime):
        return self.__class__(
            self.x*i_prime.x + self.y*j_prime.x + self.z*k_prime.x,
            self.x*i_prime.y + self.y*j_prime.y + self.z*k_prime.y,
            self.x*i_prime.z + self.y*j_prime.z + self.z*k_prime.z,
        )
    
    def morph(self, i_prime, j_prime, k_prime):
        self.vector = self.morphed(i_prime, j_prime, k_prime).vector.copy()
        return self
    
    def unmorphed(self, i_prime, j_prime, k_prime):
        det = float(i_prime.x*(j_prime.y*k_prime.z-k_prime.y*j_prime.z) - j_prime.x*(i_prime.y*k_prime.z-k_prime.y*i_prime.z) + k_prime.x*(i_prime.y*j_prime.z-j_prime.y*i_prime.z))
        inverse_det = 1/det
        q1 = inverse_det*Q([(j_prime.y*k_prime.z-k_prime.y*j_prime.z), -(i_prime.y*k_prime.z-k_prime.y*i_prime.z), (i_prime.y*j_prime.z-j_prime.y*i_prime.z)])
        q2 = inverse_det*Q([-(j_prime.x*k_prime.z-k_prime.x*j_prime.z), (i_prime.x*k_prime.z-k_prime.x*i_prime.z), -(i_prime.x*j_prime.z-j_prime.x*i_prime.z)])
        q3 = inverse_det*Q([(j_prime.x*k_prime.y-k_prime.x*j_prime.y), -(i_prime.x*k_prime.y-k_prime.x*i_prime.y), (i_prime.x*j_prime.y-j_prime.x*i_prime.y)])
        return self.morphed(q1, q2, q3)
    
    def unmorph(self, i_prime, j_prime, k_prime):
        self.vector = self.unmorphed(i_prime, j_prime, k_prime)
        return self
    
    
    @classmethod
    def exp(cls, q):
        a = q.w
        v = q.qvector
        norm = v.norm
        return math.exp(a)*(math.cos(norm)+v/norm*math.sin(norm))

    @classmethod
    def cross(cls, q1, q2):
        return np.cross(q1.vector3, q2.vector3)

    @classmethod
    def dot(cls, q1, q2):
        return np.dot(q1.vector, q2.vector)

Q = Quaternion

# These are the unit quaternions.
qi = Q([1, 0, 0])
qj = Q([0, 1, 0])
qk = Q([0, 0, 1])
# (don't change them lol)