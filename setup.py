from setuptools import setup

setup(
        name='Surface Friction Routing Problem',
        version='0.2.0',
        py_modules=['simple_case'],
        install_requires=[
            'sympy'
        ],
        entry_points='''
            [console_scripts]
            solve_case=simple_case:solve_case
        ''',
    )
