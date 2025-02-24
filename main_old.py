from fastapi import FastAPI
import math

app = FastAPI()

@app.get("/square/{number}")
def square_number(number: int):
    squared = number ** 2
    result = "even" if squared % 2 == 0 else "odd"
    return {"number": number, "squared": squared, "result": result}



# 📌 Formula:
# n!=n×(n−1)×(n−2)×...×2×1

# 📌 Examples:
# 5! = 5 × 4 × 3 × 2 × 1 = 120
# 4! = 4 × 3 × 2 × 1 = 24
# 3! = 3 × 2 × 1 = 6
# 2! = 2 × 1 = 2
# 1! = 1
# 0! = 1 (By definition)

# define a helper function to calculate factorial
def calculate_factorial(n: int) -> int:
    """Helper function to compute factorial using recursion"""
    if n == 0 or n == 1:
        return 1
    return n * calculate_factorial(n - 1)

@app.get("/factorialRecursion/{number}")
def factorial_recursion(number: int):
    if number < 0:
        return {"error": "Factorial is not defined for negative numbers"}
    
    result = calculate_factorial(number)
    return {"number": number, "factorial": result}


@app.get("/factorialMath/{number}")
def factorial_math(number: int):
    if number < 0:
        return {"error": "Factorial is not defined for negative numbers"}
    
    result = math.factorial(number)
    return {"number": number, "factorial": result}



# # Factorial of a Number
@app.get("/factorial/{number}")
def factorial(number: int):
    if number < 0:
        return {"error": "Factorial is not defined for negative numbers"}
    
    fact = 1
    for i in range(1, number + 1):
        fact *= i

    return {"number": number, "factorial": fact}



# Prime Number Checker
@app.get("/is_prime/{number}")
def is_prime(number: int):
    if number < 2:
        return {"number": number, "is_prime": False}
    
    if number in (2, 3):
        return {"number": number, "is_prime": True}
                
    if number % 2 == 0 or number % 3 == 0:
        return {"number": number, "is_prime": False}

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return {"number": number, "is_prime": False}
        i += 6  # Jump by 6 (only check numbers of the form 6k ± 1)

    return {"number": number, "is_prime": True}





# @app.get("/is_prime/{number}")
# def is_prime(number: int):
#     if number < 2:
#         return {"number": number, "is_prime": False}
    

#     for i in range(2, int(number ** 0.5) + 1):
#         if number % i == 0:
#             return {"number": number, "is_prime": False}

#     return {"number": number, "is_prime": True}




# "fibonacci_series": [0, 1, 1, 2, 3, 5, 8, 13]
# Why range(n - 2)? What does 2 mean?
# The range(n - 2) in your Fibonacci function ensures that the loop only generates the remaining terms of the sequence, since the first two terms (0 and 1) are already initialized.

# For example, if n = 5, the first two terms are [0, 1], and the loop generates the next 5 - 2 = 3 terms: [1, 2, 3].

# 4️⃣ Fibonacci Series Generator (Up to N Terms)
@app.get("/fibonacci/{n}")
def fibonacci(n: int):
    if n <= 0:
        return {"error": "Input should be a positive integer"}
    
    fib_series = [0, 1][:n]
    for i in range(n - 2):
        fib_series.append(fib_series[-1] + fib_series[-2])

    return {"terms": n, "fibonacci_series": fib_series[:n]}







# Let's find the GCD of 36 and 60:

# Factors of 36 → {1, 2, 3, 4, 6, 9, 12, 18, 36}
# Factors of 60 → {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}
# Common factors → {1, 2, 3, 4, 6, 12}
# Greatest Common Factor → 12 ✅
# So, GCD(36, 60) = 12.




# Example: GCD(48, 18)
# Initial values:
# a = 48, b = 18
# First iteration (b = 18):
# a % b = 48 % 18 = 12 (remainder)
# New values: a = 18, b = 12
# Second iteration (b = 12):
# a % b = 18 % 12 = 6
# New values: a = 12, b = 6
# Third iteration (b = 6):
# a % b = 12 % 6 = 0 (remainder is zero, so we stop)
# New values: a = 6, b = 0
# Result: The GCD of 48 and 18 is 6, which is the final value of a.
# Greatest Common Divisor (GCD)
@app.get("/gcd/{a}/{b}")
def gcd(a: int, b: int):
    while b:
        a, b = b, a % b
    return {"gcd": a}




# 153 is an Armstrong number because:
# 1³ + 5³ + 3³ = 153 (since 1³ = 1, 5³ = 125, and 3³ = 27).
# Armstrong Number Checker
@app.get("/is_armstrong/{number}")
def is_armstrong(number: int):
    num_str = str(number)
    power = len(num_str)
    sum_digits = sum(int(digit) ** power for digit in num_str)

    return {"number": number, "is_armstrong": sum_digits == number}




# ✅ 121 → Palindrome (reads the same as 121)
# ✅ 1221 → Palindrome (reads the same as 1221)
# ❌ 123 → Not a palindrome (reads 321 backward)
# ❌ 10 → Not a palindrome (reads 01 backward)
# Palindrome Number Checker
@app.get("/is_palindrome/{number}")
def is_palindrome(number: int):
    return {"number": number, "is_palindrome": str(number) == str(number)[::-1]}



# test
@app.get("/test/{number}")
def test (number: int):
    try:
        sqr = number ** 2
        result = "even" if sqr % 2 == 0 else "odd"
        return {"number": number, "squared": sqr, "result": result}
    except ValueError:
        return {"error": "Invalid input"}

# @app.get("/test/{number}")