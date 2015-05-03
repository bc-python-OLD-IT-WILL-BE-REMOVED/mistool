from setuptools import setup, find_packages

print(find_packages())
print('---')
print(find_packages(exclude=["*.config"]))
