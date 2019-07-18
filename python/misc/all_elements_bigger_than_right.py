'''
This problem finds all elements that are bigger than all elements
on its right

keep pushing the elements on the stack...
before pushing an element, check if there top of stack is smaller
than the current element
if smaller, then keep poping until you find an element bigger than
current and then push current element
at the end, the stack contains the elements we needed

'''

def find_elements_bigger_than_all_right(input_array):
    if type(input_array) != list:
        raise('Incorrect input')
    if not input_array or len(input_array) == 1:
        return input_array
    stack = []
    for element in input_array:
        while stack:
            head = stack.pop()
            if head <= element:
                continue
            stack.append(head)
            break
        stack.append(element)
    return stack

    
print find_elements_bigger_than_all_right([1,100,50,60,70, 30, 20, 5,6, 1])
print find_elements_bigger_than_all_right([1,2,3])
print find_elements_bigger_than_all_right([1,2,1])
print find_elements_bigger_than_all_right([])
print find_elements_bigger_than_all_right([1])
