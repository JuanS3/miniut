import miniut
from miniut import console

console.clear_screen()

@miniut.ttime
@console.block('Block Message')
def foo(message: str):
    console.println(message)
    return 'perfect'

console.println('Hola, probando todo')
console.println('Hola,', 'probando todo 2')
a = foo('Hello')

console.println('This is a', a)

console.warning('warning message', 'soy una advertencia jaj')
console.error('y', 'yo', 'soy', 'un', 'error')


console.println('Hola,', 'probando todo 2', color=console.MAGENTA)

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
console.start_block(m := 'TESTING INDENTATION MATRIX')

console.print_matrix(matrix,
                     header=['Prueba 1', 'Columna 2', 'three'],
                     indexes=['row1', 'row2', 'Filita 3'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.print_matrix(matrix,
                     header=['Prueba 1', 'Columna 2', 'three'],
                     indexes=None,
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.print_matrix(matrix,
                     header=None,
                     indexes=None,
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.print_matrix(matrix,
                     header=None,
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.print_matrix(matrix,
                     header=None,
                     indexes=['row1', 'row2', 'Filita 3'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.end_block(m)

console.print_matrix(matrix,
                     header=None,
                     indexes=['row1', 'row2', 'Filita 3'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.print_matrix(matrix,
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.print_matrix(matrix,
                     header=['Prueba 1', 'Columna 2', 'three'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.'
                     )

console.new_line()
console.line()
console.new_line()

console.print_matrix(matrix,
                     header=['Prueba 1', 'Columna 2', 'three'],
                     indexes=['row1', 'row2', 'Filita 3'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.',
                     style='semibox'
                     )

console.print_matrix(matrix,
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     style='semibox'
                     )

console.print_matrix(matrix,
                     header=['Prueba 1', 'Columna 2', 'three'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.',
                     style='semibox'
                     )

console.new_line()
console.line()
console.new_line()

console.print_matrix(matrix,
                     header=['Prueba 1', 'Columna 2', 'three'],
                     indexes=['row1', 'row2', 'Filita 3'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.',
                     style='numpy'
                     )
console.new_line()
console.print_matrix(matrix,
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.',
                     style='numpy'
                     )
console.new_line()
console.print_matrix(matrix,
                     header=None,
                     indexes=None,
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.',
                     style='numpy'
                     )
console.new_line()
console.print_matrix(matrix,
                     style='numpy'
                     )



matrix = [[None, None, 3], [4, None, 6], [7, 8, None]]
console.new_line()
console.print_matrix(matrix,
                     style='numpy'
                     )

console.new_line()
console.print_matrix(matrix)

console.new_line()
console.print_matrix(matrix,
                     header=None,
                     indexes=None,
                     style='numpy'
                     )
console.new_line()
console.line()
console.new_line()

console.print_matrix(matrix,
                     header=None,
                     indexes=None,
                     style=None
                     )
console.new_line()

console.print_matrix(matrix,
                     header=['Prueba 1', 'Columna 2', 'three'],
                     indexes=['row1', 'row2', 'Filita 3'],
                     color_style=console.BLUE,
                     color_index=console.GREEN,
                     color=console.MAGENTA,
                     nan_format='.',
                     style=None
                     )
console.new_line()

console.print_matrix(matrix,
                     indexes=None,
                     color_index=console.GREEN,
                     color=console.RED,
                     nan_format='Sin Elemento',
                     style=None
                     )
console.new_line()

# import io
# import sys

# def foo(inStr):
#     print ("hi"+inStr)

# def test_foo():
#     capturedOutput = io.StringIO()                  # Create StringIO object
#     sys.stdout = capturedOutput                     #  and redirect stdout.
#     foo(' test')                                     # Call function.
#     sys.stdout = sys.__stdout__                     # Reset redirect.
#     print ('Captured', capturedOutput.getvalue())   # Now works as before.

# test_foo()