#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import math
import bitarray
import binascii
import base64

def random_bitstring(length):
  key = ""
  for _ in range(length):
    key += str(random.randint(0,1))
  return key

def bits2readable(b):
  b = bitarray.bitarray(b).tobytes()
  readable = base64.b64encode(b).decode()
  return readable

def readable2bits(readable):
  b = base64.b64decode(readable.encode())
  c = bitarray.bitarray()
  c.frombytes(b)
  c = c.tolist()
  output = ""
  for x in c:
    if x==False: output+='0'
    if x==True: output+='1'
  return output

def string2bits(string):
    c = bitarray.bitarray()
    c.frombytes(string.encode())
    bits = c.tolist()
    bits = ''.join(map(str,list(map(int,bits))))
    return bits

def bits2string(bits):
    string = ""
    c = bitarray.bitarray(bits)
    string = c.tobytes().decode()
    return string

def xor_bitstrings(x,y):
    z = ""
    for c in range(len(x)):
        z += str(int(int(x[c])^int(y[c])))
    return z

def xor_bitlist(bitlist):
    XOR = 0
    for bit in bitlist:
        XOR += bit
    XOR = XOR % 2
    return XOR

def and_bitstrings(x,y):
    z = ""
    for c in range(len(x)):
        z += str(int(int(x[c])&int(y[c])))
    return z

def not_bitstring(x):
    o = ""
    for bit in x:
        o += str(1-int(bit))
    return o

def shift_chain(chain, feedback):
    shifted = [feedback]
    for x in chain[:-1]:
        shifted.append(x)
    return shifted

def bitstring_rotation_R(x,k):
    rot = -int(k,2) % len(x)
    output = x[rot:]+x[:rot]
    return output

def bitstring_rotation_L(x,k):
    rot = int(k,2) % len(x)
    output = x[rot:]+x[:rot]
    return output

def split_chunks(x, length, padding=True, padstring="0"):
    if len(x)==0:
        x = padstring*length
    a = [x[i:i+length] for i in range(0, len(x), length)]
    last = a[-1]
    missing = length-len(last)
    if padding:
        a[-1] = last+padstring*missing
        padding_length = missing
        return a, padding_length
    else:
        return a

def split_half(bits):
  l = len(bits)
  half = int(l/2)
  output = []
  output.append(''.join(bits[:half]))
  output.append(''.join(bits[half:]))
  return output

def swap_list(l, x, y):
    a = l[x]
    b = l[y]
    l[x] = b
    l[y] = a
    return l

def bits2cube(i,x_size,y_size,z_size):
    cube = [[[0 for _ in range(z_size)] for _ in range(y_size)] for _ in range(x_size)]
    count = 0
    for x in range(len(cube)):
        for y in range(len(cube[x])):
            for z in range(len(cube[x][y])):
                  cube[x][y][z] = i[count]
                  count += 1
    return cube

def cube_selector(cube, x_pos, y_pos, z_pos, x_size, y_size, z_size):
    xor = 0
    selection = [[2, 1, -3],
                 [-4, -3, -3],
                 [0, 2, -1],
                 [0, 3, -1],
                 [-2, 0, -2],
                 [1, -4, 1],
                 [-1, -1, 3],
                 [-4, -4, -2]]
    for coord in selection:
        xor += int(cube[(x_pos+coord[0]) % x_size][(y_pos+coord[1]) % y_size][(z_pos+coord[2]) % z_size])
    final = xor % 2
    return final

def transform_cube(cube,x_size,y_size,z_size):
    cube_transformed = [[[0 for _ in range(z_size)] for _ in range(y_size)] for _ in range(x_size)]
    for x in range(len(cube)):
        for y in range(len(cube[x])):
            for z in range(len(cube[x][y])):
                selector_sum = cube_selector(cube, x, y, z, x_size, y_size, z_size)
                new = (int(cube[x][y][z])+selector_sum) % 2
                cube_transformed[x][y][z] = str(new)
    return cube_transformed

def cube2list(cube,x_size,y_size):
    Array_2D = [[0 for _ in range(y_size)] for _ in range(x_size)]
    for x in range(len(cube)):
        for y in range(len(cube[x])):
            Array_2D[x][y] = ''.join(cube[x][y])
    return Array_2D

def rotation_offset(array):
    offset_array = [[36, 11, 41, 31, 64, 62, 27, 49],
                    [63, 30, 30, 57, 15, 47, 21, 64],
                    [55, 50, 36, 61, 10, 44, 24, 36],
                    [61, 35, 38, 2, 13, 37, 18, 37],
                    [62, 11, 51, 32, 41, 4, 18, 19],
                    [13, 58, 27, 3, 42, 62, 29, 14],
                    [21, 29, 3, 37, 8, 30, 60, 29],
                    [34, 14, 60, 28, 6, 56, 4, 39]]
    for x in range(len(array)):
        for y in range(len(array[x])):
            offset = offset_array[x][y]
            bitoffset = "{0:b}".format(offset)
            array[x][y] = bitstring_rotation_R(array[x][y], bitoffset)
    return array

def permutation(array, x_size, y_size):
    permuted = [[0 for _ in range(y_size)] for _ in range(x_size)]
    for x in range(x_size):
        for y in range(y_size):
            permuted[y%x_size][(2*x+3*y)%y_size] = array[x][y]
    return permuted

def logical_operations(array, x_size, y_size):
    operated = [[0 for _ in range(y_size)] for _ in range(x_size)]
    for x in range(len(operated)):
        for y in range(len(operated[x])):
            operated[x][y] = xor_bitstrings(array[x][y],and_bitstrings(not_bitstring(array[(x+1)%x_size][y]),array[(x+2)%x_size][y]))
    return operated

def list2bits(array):
    i = ""
    for x in range(len(array)):
        for y in range(len(array)):
            i += array[x][y]
    return i

def f_function(i):
    xs = 8
    ys = 8
    zs = 32
    RC = ['10001101000011001101000000101101',
          '00001110001111111001111100001110',
          '10011011110101001101100001100100',
          '11101111010110001100001100110011',
          '00100101000000101001110010000010',
          '10110110110001101111010010011110',
          '10111011111110100001000111000110',
          '11001000100110110010010011010111',
          '01110011001110011001101111100110',
          '01110111111111101100001010110001',
          '10010010110111000000110110110011',
          '00100100110111000110010000111111',
          '01110101010100001110000110100001',
          '01010100100100100010011000000010',
          '01010100110100011010111111000000',
          '00000110011001100000000001101000',
          '01010101101001000100101001110111',
          '10000100110100011111100101010100',
          '00011100110110000000111101110100',
          '01100001011110000001001100101000',
          '11101100111011011111111111001011',
          '00000110110101100001001100100000',
          '01110110001011010101001100000100',
          '01101010010001111011101111110100',
          '11001101001011111110001100010001',
          '00001110111000010000101100011001',
          '01010000010110111111100111000000',
          '11100101000101101010010111001010',
          '11001110010101101000111001000110',
          '00011110101011000110001100111100',
          '00011100011010100001111110001010',
          '11101100011110110111101100000001']
    for q in range(32):
        cube = bits2cube(i,xs,ys,zs)
        cube = transform_cube(cube,xs,ys,zs)
        array = cube2list(cube,xs,ys)
        array = rotation_offset(array)
        arrray = permutation(array,xs,ys)
        array = logical_operations(array,xs,ys)
        array[0][0] = xor_bitstrings(array[0][0], RC[q])
        i = list2bits(array)
    return i

class sponge_construction(object):
    def __init__(self, round_function, block_length):
        self.roundfunc = round_function
        self.blocklength = block_length
        self.flength = 2048
    def hash(self, inputbits):
        bit_blocks, padding = split_chunks(inputbits, self.blocklength, padding=True)
        iv = "11110111010000101111011011010100011011101101101010100110000100001111111110101101001111100101010011110010101101100010111111011000110111001110000111001010110001011111111001010100011000011111100010100101110001011001110001000111001001110100010000011111010011100011110011111101101010010010000101110000111001111010101011011010111100101011101111110101111100110101100111000011111100001000110101101101000000101000111011000000001100001101000110100111100010011001000010110011010011011110101000000010011010110011100101001101110100111111111111011001110111000000100100001100101101100001000111000010010101010001001100111011001001101110011000110101001111000101111100010100000100101111000100000100111000111101111011110000100001001011111110111100100010110010001100100010111100010101000010000000011011110110010111010100100001111010100000001001101111000010010111110011100111100101010101001111001110101111000001010100010000111110110110111110010010000101001010010111100101110001010111010010111001110011111010110101001011000101100100010111101011000010110100001011101010001101100001101111011011110001111100110010010101000101111111101001110110100101011001110100001001111010111101011101111110110010110001001010101100111001011001111101000111011100011010100110110010001001011000100010101101111001001011010001100111010100110110100110001000011001001001000010101101000011010100100101011011100101101010111110001100101011011001111101001010010001010011010110110110100100111000010000011001111011101010110001101100010100000101010111110111100110100010100101000010111001010100010000011111000010011000111001101111111111001101110001101011101000100100111111101100011111010010000011001101000101000111011000100011101010101110111011111011011101110000000001001000010110101100011001000011001000011011110011001011001010001001100110000110101011100110101011111111011101001011010010011010101001000001111000010100111111111111111001110100100100101100100110101010010100000100101111111100000101001010101000011010001100111100011101101011011011001110001110011011100101001010100011100000000010001011011111"
        r = iv[:self.blocklength]
        c = iv[self.blocklength:]
        # absorbtion
        for block in bit_blocks:
            r = xor_bitstrings(r,block)
            i = r+c
            f = self.roundfunc(i)
            r = f[:self.blocklength]
            c = f[self.blocklength:]
        # output
        return r[:self.blocklength]
    def pseudorandom(self, seed, bitcount):
        bit_blocks, padding = split_chunks(seed, self.blocklength, padding=True)
        iv = "11110111010000101111011011010100011011101101101010100110000100001111111110101101001111100101010011110010101101100010111111011000110111001110000111001010110001011111111001010100011000011111100010100101110001011001110001000111001001110100010000011111010011100011110011111101101010010010000101110000111001111010101011011010111100101011101111110101111100110101100111000011111100001000110101101101000000101000111011000000001100001101000110100111100010011001000010110011010011011110101000000010011010110011100101001101110100111111111111011001110111000000100100001100101101100001000111000010010101010001001100111011001001101110011000110101001111000101111100010100000100101111000100000100111000111101111011110000100001001011111110111100100010110010001100100010111100010101000010000000011011110110010111010100100001111010100000001001101111000010010111110011100111100101010101001111001110101111000001010100010000111110110110111110010010000101001010010111100101110001010111010010111001110011111010110101001011000101100100010111101011000010110100001011101010001101100001101111011011110001111100110010010101000101111111101001110110100101011001110100001001111010111101011101111110110010110001001010101100111001011001111101000111011100011010100110110010001001011000100010101101111001001011010001100111010100110110100110001000011001001001000010101101000011010100100101011011100101101010111110001100101011011001111101001010010001010011010110110110100100111000010000011001111011101010110001101100010100000101010111110111100110100010100101000010111001010100010000011111000010011000111001101111111111001101110001101011101000100100111111101100011111010010000011001101000101000111011000100011101010101110111011111011011101110000000001001000010110101100011001000011001000011011110011001011001010001001100110000110101011100110101011111111011101001011010010011010101001000001111000010100111111111111111001110100100100101100100110101010010100000100101111111100000101001010101000011010001100111100011101101011011011001110001110011011100101001010100011100000000010001011011111"
        r = iv[:self.blocklength]
        c = iv[self.blocklength:]
        # absorbtion
        for block in bit_blocks:
            r = xor_bitstrings(r,block)
            i = r+c
            f = self.roundfunc(i)
            r = f[:self.blocklength]
            c = f[self.blocklength:]
        # squeezing
        count = math.ceil(bitcount/self.blocklength)
        output = ""
        for q in range(count):
            output += r
            i = r+c
            f = self.roundfunc(i)
            r = f[:self.blocklength]
            c = f[self.blocklength:]
        return output[:self.blocklength]

class hmac_construction(object):
    def __init__(self, hash_function):
        self.hashfunction = hash_function
    def authenticate(self, inputbits, key):
        ipad = ("00110110"*math.ceil(len(key)/4))[:len(key)]
        opad = ("01011100"*math.ceil(len(key)/4))[:len(key)]
        inner_hash = self.hashfunction.hash(xor_bitstrings(key,ipad)+inputbits)
        outer_hash = self.hashfunction.hash(xor_bitstrings(key,opad)+inner_hash)
        return outer_hash

hashfunction = sponge_construction(f_function, 512)
authenticationcode = hmac_construction(hashfunction)
